# cogs / basics.py

import random
import traceback

from discord.ext import commands


class Basic(commands.Cog):
    """Action commands"""
    def __init__(self, client):

        self.client = client

    # Hello
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def hello(self, ctx):
        await ctx.reply(f"Hello {ctx.author.mention}")

    @commands.hybrid_command()
    async def roll(self, ctx, dice: str):
        """Rolls dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception as e:
            traceback.print_exception(e)
            await ctx.reply('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.reply(result)

    @commands.hybrid_command()
    async def roll1(self, ctx, dice: str, type: str):
        """Rolls dice in NdN format."""
        try:
            if "-" in dice or "+" in dice:
                try:
                    modifier = int(dice.split("-")[1])
                    dice = dice.split("-")[0]
                    print(modifier)
                    print(dice)
                except Exception as e:
                    traceback.print_exception(e)
                    modifier = int(dice.split("+")[1])
                    dice = dice.split("+")[0]
                    print(modifier)
                    print(dice)
            else:
                modifier = 0
                print(modifier)
                print(dice)
            rolls, limit = map(int, dice.split('d'))
            if type == "dis":
                result = ', '.join(str(random.randint(1, limit) + modifier) for _ in range(rolls))
            elif type == "sum":
                result = modifier
                for _ in range(rolls):
                    result += random.randint(1, limit)
            elif type == "both":
                result1 = ', '.join(str(random.randint(1, limit) + modifier) for _ in range(rolls))
                nums = result1.split(", ")
                sum = modifier
                for num in nums:
                    sum += (int(num)-modifier)
                result = f"rolls: {result1}\nresult: {sum}"
            await ctx.reply(result)
        except:
            await ctx.reply("Incorrectly formatted input. Please try again with the correct format")

    @commands.hybrid_command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, choices: str):
        """Chooses between multiple choices."""
        options = choices.split(",")
        await ctx.reply(random.choice(options))

    # Addition
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.reply(left + right)


async def setup(client):
    await client.add_cog(Basic(client))
