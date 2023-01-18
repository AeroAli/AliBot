# cogs / test.py
from discord.ext import commands


class Test(commands.Cog):
    """test cog"""
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def test(self, ctx):
        """Who's the coolest"""
        await ctx.reply(f"{ctx.author.mention} is the coolest")


async def setup(client):
    await client.add_cog(Test(client))