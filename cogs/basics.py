# cogs / basics.py

import random

from discord.ext import commands


class Basic(commands.Cog):
    """Basic commands"""
    def __init__(self, client):
        self.client = client

        # Hello
        @commands.hybrid_command()
        # @commands.cooldown(1, 10, commands.BucketType.user)
        async def hello(self, ctx):
            await ctx.reply(f"Hello {ctx.author.mention}")

        # Roll
        @commands.hybrid_command()
        # @commands.cooldown(1, 10, commands.BucketType.user)
        async def roll(self, ctx, dice: str):
            """Rolls dice in NdN format."""
            try:
                rolls, limit = map(int, dice.split('d'))
            except Exception:
                await ctx.reply('Format has to be in NdN!')
                return
            result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
            await ctx.reply(result)

        # Choose
        @commands.hybrid_command()
        # @commands.cooldown(1, 10, commands.BucketType.user)
        async def choose(self, ctx, choice_in: str):
            """Chooses between multiple choices, splits at "," """
            choices = choice_in.split(",")
            await ctx.reply(random.choice(choices))

        # Addition
        @commands.hybrid_command()
        # @commands.cooldown(1, 10, commands.BucketType.user)
        async def add(self, ctx, left: int, right: int):
            """Adds two numbers together."""
            await ctx.reply(left + right)


async def setup(client):
    await client.add_cog(Basic(client))
