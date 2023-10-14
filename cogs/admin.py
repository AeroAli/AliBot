import traceback

from discord import Embed, app_commands
from discord.ext import commands
from utils import checks
import discord
import inspect
import utils.checks

# to expose to the eval command
import datetime
from collections import Counter

# Tuples with data for a parameter's choices in the sync command. Putting it all in the decorator is ugly.
SPEC_CHOICES: list[tuple[str, str]] = [
    ("[~] —— Sync current guild.", "~"),
    ("[*] —— Copy all global app commands to current guild and sync.", "*"),
    ("[^] —— Clear all commands from the current guild target and sync, thereby removing guild commands.", "^"),
    ("[-] —— (D-N-T!) Clear all global commands and sync, thereby removing all global commands.", "-"),
    ("[+] —— (D-N-T!) Clear all commands from all guilds and sync, thereby removing all guild commands.", "+"),
]

class Admin(commands.Cog):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, client: commands.Bot):
        self.client = client


    async def cog_command_error(self, ctx, error: Exception) -> None:
        traceback.print_exception(error)
        error = getattr(error, "original", error)
        await ctx.send(embed=Embed(title=f"{type(error).__name__}",description=f"{error}",colour=0xC70039 ))


    async def cog_check(self, ctx) -> bool:
        original = commands.is_owner().predicate
        db_check = utils.checks.in_test_guild().predicate
        return await original(ctx) and await db_check(ctx)

    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def load(self,ctx, *, module : str):
        """Loads a module."""
        await self.client.load_extension(module)
        embed_var = Embed(title="Loaded Module", description=f"Loaded {module}",colour=0x088F8F)
        await ctx.reply(embed=embed_var)

    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def unload(self,ctx, *, module : str):
        """Unloads a module."""
        await self.client.unload_extension(module)
        embed_var = Embed(title="Unloaded Module", description=f"Unloaded {module}",colour=0x088F8F)
        await ctx.reply(embed=embed_var)

    @commands.hybrid_command(name="reload")
    @app_commands.guilds(1039953198359781446)
    async def reload_(self,ctx, *, module : str):
        """Reloads a module."""
        await self.client.reload_extension(module)
        embed_var = Embed(title="Reloaded Module", description=f"Reloaded {module}",colour=0x088F8F)
        await ctx.reply(embed=embed_var)

    @commands.hybrid_command("sync")
    @app_commands.guilds(1039953198359781446)
    @app_commands.choices(spec=[app_commands.Choice(name=name, value=value) for name, value in SPEC_CHOICES])
    async def sync_(self,ctx,guilds: commands.Greedy[discord.Object] = None,  spec: app_commands.Choice[str] | None = None,) -> None:
        async with ctx.typing():
            if not guilds:
                if spec == "~":
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "*":
                    if ctx.guild:
                        ctx.bot.tree.copy_global_to(guild=ctx.guild)
                        synced = await ctx.bot.tree.sync(guild=ctx.guild)
                    else:
                        synced = []
                elif spec == "^":
                    ctx.bot.tree.clear_commands(guild=ctx.guild)
                    await ctx.bot.tree.sync(guild=ctx.guild)
                    synced = []
                elif spec == "-":
                    ctx.bot.tree.clear_commands(guild=None)
                    await ctx.bot.tree.sync()
                    synced = []
                elif spec == "+":
                    for guild in ctx.bot.guilds:
                        ctx.bot.tree.clear_commands(guild=guild)
                        await ctx.bot.tree.sync(guild=guild)
                    synced = []
                else:
                    synced = await ctx.bot.tree.sync()

                place = "globally" if spec is None else "to the current guild"
                await ctx.send(f"Synced {len(synced)} commands {place}.", ephemeral=True)
                return

            ret = 0
            for guild in guilds:
                try:
                    await ctx.bot.tree.sync(guild=guild)
                except discord.HTTPException:
                    pass
                else:
                    ret += 1

            await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.", ephemeral=True)

    @sync_.error
    async def sync_error(self, ctx, error: commands.CommandError) -> None:
        """A local error handler for the :meth:`sync_` command.

        Parameters
        ----------
        ctx : :class:`core.Context`
            The invocation context.
        error : :class:`commands.CommandError`
            The error thrown by the command.
        """

        embed = discord.Embed(title="/sync Error", description="Something went wrong with this command.")

        # Extract the original error.
        error = getattr(error, "original", error)
        if ctx.interaction:
            error = getattr(error, "original", error)

        # Respond to the error.
        if isinstance(error, app_commands.CommandSyncFailure):
            embed.description = (
                "Syncing the commands failed due to a user related error, typically because the command has invalid "
                "data. This is equivalent to an HTTP status code of 400."
            )
        elif isinstance(error, discord.Forbidden):
            embed.description = "The bot does not have the `applications.commands` scope in the guild."
        elif isinstance(error, app_commands.MissingApplicationID):
            embed.description = "The bot does not have an application ID."
        elif isinstance(error, app_commands.TranslationError):
            embed.description = "An error occurred while translating the commands."
        elif isinstance(error, discord.HTTPException):
            embed.description = "Generic HTTP error: Syncing the commands failed."
        else:
            embed.description = "Syncing the commands failed."

        await ctx.reply(embed=embed)


async def setup(client):
    await client.add_cog(Admin(client))