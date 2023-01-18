# cogs / assistance .py

from discord import Embed
from discord.ext import commands


class Assistance(commands.Cog):
    """least helpful cog"""
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    async def halp(self, ctx, command: str):
        """Lazy help command"""
        embed_var = Embed(description=f"{command} is really fucking hard to explain. soz")
        await ctx.reply(embed=embed_var)

async def setup(client):
    await client.add_cog(Assistance(client))
