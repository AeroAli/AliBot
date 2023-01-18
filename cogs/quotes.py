# cogs / quotes.py
import random
from os import listdir
from os.path import isfile, join

from discord.ext import commands


class Quote(commands.Cog):
    """quote commands"""
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def quote(self, ctx, source: str):
        """outputs quotes from file"""
        try:
            if source != "random":
                lines = open(f"quotes/{source}").read().splitlines()
                quote = random.choice(lines)
            else:
                quote = random.choice([x for x in open(
                    f"quotes/{random.choice([y for y in listdir('quotes') if isfile(join('quotes', y))])}").read().splitlines()])
            await ctx.reply(quote)
        except Exception:
            await ctx.reply("Source Not Available")


async def setup(client):
    await client.add_cog(Quote(client))
