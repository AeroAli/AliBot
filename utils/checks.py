"""
checks.py: Custom checks used by the bot.
"""

from __future__ import annotations

import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import maybe_coroutine

from utils.errors import NotAdmin, NotInBotVoiceChannel, UserIsBlocked, BadRole, NotOwner, BabbyProofing

__all__ = ("is_admin", "in_bot_vc", "is_blocked", "check_any")


# def is_owner_or_friend():
#     """A :func:`.check` that checks if the person invoking this command is the
#     owner of the bot or on a special friends list.
#
#     This is partially powered by :meth:`.Bot.is_owner`.
#
#     This check raises a special exception, :exc:`.NotOwnerOrFriend` that is derived
#     from :exc:`commands.CheckFailure`.
#     """
#
#     async def predicate(ctx: commands.Context) -> bool:
#         if not (ctx.bot.owner_id == ctx.author.id or ctx.bot.is_special_friend(ctx.author)):
#             msg = "You do not own this bot, nor are you a friend of the owner."
#             raise NotOwnerOrFriend(msg)
#         return True
#
#     return commands.check(predicate)

def is_owner():
    async def predicate(ctx: commands.Context) -> bool:
        if not await ctx.bot.is_owner(ctx.author):
            msg = "You do not own this bot."
            raise NotOwner(msg)
        return True

    return commands.check(predicate)


async def get_allowed(db_pool, guild_id):
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT role_id FROM `role_table` where allowed=1 and guild_id={guild_id}")
            # print(type(cur))
            result = await cur.fetchall()
            result = [int(x[0]) for x in result]
            print(result)
            return result


async def get_not_allowed(db_pool, guild_id):
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT role_id FROM `role_table` where allowed=0 and guild_id={guild_id}")
            # print(type(cur))
            result = await cur.fetchall()

            result = [int(x[0]) for x in result]
            print(result)
            return result


async def get_guilds(ctx):
    async with ctx.client.db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT guild_id FROM `guild_table` where guild_id={ctx.guild.id}")
            # print(type(cur))
            result = await cur.fetchone()
            print(int(result[0]))
            return int(result[0])


# async def get_blocked_guilds(ctx):
#     async with ctx.client.db_pool.acquire() as conn:
#         async with conn.cursor() as cur:
#             await cur.execute(
#                 f"SELECT guild_id FROM `guild_table` where guild_id={ctx.guild.id} and allowed=0")
#             # print(type(cur))
#             result = await cur.fetchone()
#             print(int(result[0]))
#             return int(result[0])

async def get_blocked_users(db_pool):
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT user_id FROM `user_table` where allowed=0")
            # print(type(cur))
            result = await cur.fetchall()

            result = [int(x[0]) for x in result]
            print(result)
            return result


async def get_babbies(db_pool):
    async with db_pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT user_id FROM `user_table` where is_babby=1")
            # print(type(cur))
            result = await cur.fetchall()
            result = [int(x[0]) for x in result]
            return result


def has_roles():
    async def predicate(ctx: commands.Context) -> bool:
        yes = False
        no = False
        if not await ctx.bot.is_owner(ctx.author):
            if not (ctx.guild is None and ctx.author.roles is None):
                guild_ids = await get_guilds(ctx)
                if ctx.guild.id == guild_ids:
                    allowed = await get_allowed(ctx.bot.db_pool, ctx.guild.id)
                    not_allowed = await get_not_allowed(ctx.bot.db_pool, ctx.guild.id)
                    for role in ctx.author.roles:
                        if role.id in not_allowed:
                            no = True
                        if role.id in allowed:
                            yes = True
                if yes == False and no == True:
                    msg = "You are not allowed to run this command"
                    raise BadRole(msg)
        return True

    return commands.check(predicate)


def is_admin():
    """A :func:`.check` that checks if the person invoking this command is an
    administrator of the guild in the current context.

    This check raises a special exception, :exc:`NotAdmin` that is derived
    from :exc:`commands.CheckFailure`.
    """

    async def predicate(ctx: commands.Context) -> bool:
        if not (ctx.guild is not None and ctx.author.guild_permissions.administrator):
            msg = "Only someone with administrator permissions can do this."
            raise NotAdmin(msg)
        return True

    return commands.check(predicate)


def in_bot_vc():
    """A :func:`.check` that checks if the person invoking this command is in
    the same voice channel as the bot within a guild.

    This check raises a special exception, :exc:`NotInBotVoiceChannel` that is derived
    from :exc:`commands.CheckFailure`.
    """

    async def predicate(ctx: commands.Context) -> bool:
        vc: discord.VoiceProtocol | None = ctx.voice_client

        if not (
                ctx.author.guild_permissions.administrator or
                (vc and ctx.author.voice and ctx.author.voice.channel == vc.channel)
        ):
            msg = "You are not connected to the same voice channel as the bot."
            raise NotInBotVoiceChannel(msg)
        return True

    return commands.check(predicate)


def in_test_guild():
    """A :func:`.check` that checks if the person invoking this command is in
    the ACI100 guild.

    This check raises the exception :exc:`commands.CheckFailure`.
    """

    async def predicate(ctx: commands.Context) -> bool:
        if ctx.guild.id != 1039953198359781446:
            msg = "This command isn't active in this guild."
            raise commands.CheckFailure(msg)
        return True

    return commands.check(predicate)





def is_blocked():
    """A :func:`.check` that checks if the command is being invoked from a blocked user or guild.

    This check raises the exception :exc:`commands.CheckFailure`.
    """
    async def predicate(ctx: commands.Context) -> bool:
        if not await ctx.bot.is_owner(ctx.author):
            blocked_users = await get_blocked_users(ctx.bot.db_pool)
            if ctx.author.id in await get_babbies(ctx.bot.db_pool):
                raise BabbyProofing()
            if ctx.author.id in blocked_users:
                msg = "This user is prohibited from using bot commands."
                raise UserIsBlocked(msg)
            # if ctx.guild and (ctx.guild.id == await get_guilds(ctx)):
            #     msg = "This guild is prohibited from using bot commands."
            #     raise GuildIsBlocked(msg)
        return True

    return commands.check(predicate)


def check_any(*checks):
    """An attempt at making a :func:`check_any` decorator for application commands.

    Parameters
    ----------
    checks: :class:`app_Check`
        An argument list of checks that have been decorated with :func:`app_commands.check` decorator.

    Returns
    -------
    :class:`app_Check`
        A predicate that condenses all given checks with logical OR.
    """

    # TODO: Actually check if this works.
    async def predicate(interaction: discord.Interaction) -> bool:
        errors = []
        for check in checks:
            try:
                value = await maybe_coroutine(check, interaction)
            except app_commands.CheckFailure as err:
                errors.append(err)
            else:
                if value:
                    return True
        # If we're here, all checks failed.
        raise app_commands.CheckFailure(checks, errors)

    return app_commands.check(predicate)
