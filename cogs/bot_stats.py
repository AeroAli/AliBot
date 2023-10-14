"""
bot_stats.py: A cog for tracking different bot metrics.
"""

from __future__ import annotations

import datetime
import logging
import traceback
from datetime import timedelta
from typing import Literal, Any

import discord
from discord.app_commands import Choice
from discord.ext import commands
from discord.utils import utcnow

from utils.db import *
from utils.embeds import StatsEmbed

LOGGER = logging.getLogger(__name__)


class BotStatsCog(commands.Cog, name="Bot Stats"):
    """A cog for tracking different bot metrics."""

    def __init__(self, client):
        self.client = client

    @property
    def cog_emoji(self) -> discord.PartialEmoji:
        """:class:`discord.PartialEmoji`: A partial emoji representing this cog."""

        return discord.PartialEmoji(name="\N{CHART WITH UPWARDS TREND}")

    async def cog_command_error(self, ctx, error: Exception) -> None:
        traceback.print_exception(error)

    async def track_command_use(self, ctx) -> None:
        """Stores records of command uses in the database after some processing."""

        print("track")
        # Make sure all possible involved users and guilds are in the database before using their ids as foreign keys.
        user_info, guild_info = [ctx.author], [ctx.guild]

        for arg in (ctx.args + list(ctx.kwargs.values())):
            if isinstance(arg, discord.User | discord.Member):
                user_info.append(arg)
                # print(user_info)
                print("user: ", arg)
            elif isinstance(arg, discord.Guild):
                guild_info.append(arg)
                print("guild: ", arg)
        guild_info = tuple(guild_info)
        user_info = tuple(user_info)
        print("guild: ",guild_info,"user: ", user_info)

        if user_info:
            async with self.client.db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    print("cur")
                    await upsert_users(cur, *user_info)
            print("user_info: ",user_info)

        if guild_info:
            print("guild_info: ",guild_info)
            async with self.client.db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await upsert_guilds(cur, *guild_info)

        # print(ctx.guild.id)#, ctx.channel.id, ctx.author.id,ctx.prefix,ctx.command.qualified_name,(ctx.interaction is not None),ctx.command_failed,self.client.user)
        # Assemble the record to upsert.
        cmd = (
            ctx.guild.id,
            ctx.channel.id,
            ctx.author.id,
            utcnow(),
            ctx.prefix,
            ctx.command.qualified_name,
            (ctx.interaction is not None),
            ctx.command_failed,
            self.client.user
        )
        print("cmd", cmd)
        query = """
                INSERT into commands (guild_id, channel_id, user_id, date_time, prefix, command, app_command, failed, bot)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    print(query, cmd)
                    await cur.execute(query, cmd)
                    print("executed")
                except Exception as e:
                    traceback.print_exception(e)

    @commands.Cog.listener("on_command_completion")
    async def track_command_completion(self, ctx) -> None:
        """Record prefix and hybrid command usage."""
        await self.track_command_use(ctx)


    @commands.Cog.listener("on_interaction")
    async def track_interaction(self, ctx, interaction) -> None:
        """Record application command usage, ignoring hybrid or other interactions.

        References
        ----------
        https://github.com/AbstractUmbra/Mipha/blob/main/extensions/stats.py#L174
        """

        if (
                interaction.command is not None and
                interaction.type is discord.InteractionType.application_command and
                not isinstance(interaction.command, commands.hybrid.HybridAppCommand)
        ):
            ctx.command_failed = interaction.command_failed
            await self.track_command_use(ctx)

    @commands.Cog.listener("on_command_error")
    async def track_command_error(self, ctx, error: commands.CommandError) -> None:
        """Records prefix, hybrid, and application command usage, even if the result is an error."""

        if not isinstance(error, commands.CommandNotFound):
            await self.track_command_use(ctx)

    @commands.Cog.listener("on_guild_join")
    async def add_guild_to_db(self, guild: discord.Guild) -> None:
        """Upserts a guild - one that the bot just joined - to the database."""
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await upsert_guilds(cur, guild)

    @commands.hybrid_command(name="usage")
    async def check_usage(
            self,
            ctx,
            *,
            time_period: Literal["today", "last month", "last year", "all time"] = "all time",
            command: str = None,
            guilds: bool = False,
            universal: bool = False
    ) -> None:
        """Retrieve statistics about bot command usage.

        Parameters
        ----------
        ctx : :class:`core.Context`
            The invocation context.
        time_period : Literal["today", "last month", "last year", "all time"], default="all time"
            Whether to stay local or look among all guilds. Defaults to 'all time'.
        command : :class:`str`, optional
            The command to look up.
        guilds : :class:`bool`, default=False
            Whether to look at guilds or users. Defaults to False.
        universal : :class:`bool`, default=False
            Whether to look at users among all guilds. Defaults to False.
        """
        # print(time_period, command, guilds, universal)
        periods = {"today": 1, "last month": 30, "last year": 365}
        actual_time_pd = periods.get(time_period, 0)
        guild = None if guilds else ctx.guild
        records = await self.get_usage(actual_time_pd, command, guild, universal)
        ldbd_emojis = ["\N{FIRST PLACE MEDAL}", "\N{SECOND PLACE MEDAL}", "\N{THIRD PLACE MEDAL}"]
        ldbd_emojis.extend(["\N{SPORTS MEDAL}" for _ in range(6)])
        embed = StatsEmbed(color=0x193d2c, title="Commands Leaderboard", description="―――――――――――")
        if records:
            get_strat = self.client.get_user if guild else self.client.get_guild

            record_tuples = tuple(
                ((entity if (entity := get_strat(record[0])) else record[0]), record[1]) for record in records
            )

            embed.add_leaderboard_fields(ldbd_content=record_tuples, ldbd_emojis=ldbd_emojis)
        else:
            embed.description += "\nNo records found."

        await ctx.reply(embed=embed)

    async def get_usage(
            self,
            time_period: int = 0,
            command: str | None = None,
            guild: discord.Guild | None = None,
            universal: bool = False,
    ) -> list[Any]:
        """Queries the database for command usage."""

        query_args: list[Any] = []  # Holds the query args as objects.
        where_params: list[str] = []  # Holds the query param placeholders as formatted strings.

        # Create the base queries.
        if guild:
            query = """
                SELECT u.user_id, COUNT(*)
                FROM commands cmds INNER JOIN users u on cmds.user_id = u.user_id
                {where}
                GROUP BY u.user_id
                ORDER BY COUNT(*) DESC
                LIMIT 10;
            """

        else:
            query = """
                SELECT g.guild_id, COUNT(*)
                FROM commands cmds INNER JOIN guilds g on cmds.guild_id = g.guild_id
                {where}
                GROUP BY g.guild_id
                ORDER BY COUNT(*) DESC
                LIMIT 10;
            """

        # Create the WHERE clause for the query.
        if guild and not universal:
            query_args.append(guild.id)
            where_params.append(f"guild_id = %s")

        if time_period and (time_period > 0):
            query_args.append(utcnow() - timedelta(days=time_period))
            where_params.append(f"date_time >= %s")

        if command:
            query_args.append(command)
            where_params.append(f"command = %s")

        query_args.append(self.client.user)
        where_params.append(f"bot = %s")

        # Add the WHERE clause to the query if necessary.
        where_clause = ("WHERE " + " AND ".join(where_params) + "\n") if len(query_args) > 0 else ""
        query = query.format(where=where_clause)


        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                print(query, query_args)
                # According to the source code, aiomysql.Cursor can take a list, tuple, or dict as an args argument.
                await cur.execute(query, query_args)
                return await cur.fetchall()

    @check_usage.autocomplete("command")
    async def command_autocomplete(self, interaction, current: str) -> list[Choice[str]]:
        """Autocompletes with bot command names."""

        assert self.client.help_command
        ctx = await self.client.get_context(interaction)
        help_command = self.client.help_command.copy()
        help_command.context = ctx

        current = current.lower()
        return [
                   Choice(name=command.qualified_name, value=command.qualified_name)
                   for command in await help_command.filter_commands(self.client.walk_commands(), sort=True)
                   if current in command.qualified_name
               ][:25]


async def setup(client) -> None:
    """Connects cog to bot."""

    await client.add_cog(BotStatsCog(client))