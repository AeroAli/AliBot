# cogs / starkid.py
import random
from os import listdir
from os.path import isfile, join

from discord.ext import commands


class Starkid(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def star_quote(self, ctx, show: str):
        try:
            show = show.lower()
            # if show == "test":
            #     lines = open(f"starkids/{show}").read().splitlines()
            #     quote = random.choice(lines)
            #     if "\\n" in quote:
            #         quote = quote.replace("\\n", "\n")
            if show != "random":
                lines = open(f"starkids/{show}_quotes").read().splitlines()
                quote = random.choice(lines)
                if "\\n" in quote:
                    quote = quote.replace("\\n", "\n")
            else:
                quote = random.choice([x for x in open(
                    f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y)) and 'quotes' in y])}"
                ).read().splitlines()])
                if "\\n" in quote:
                    quote = quote.replace("\\n", "\n")
            await ctx.reply(quote)
        except Exception:
            await ctx.reply("Source Not Available")

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def star_gif(self, ctx, show: str):
        try:
            if show != "random":
                lines = open(f"starkids/{show}_gifs").read().splitlines()
                gif = random.choice(lines)
            else:
                gif = random.choice([x for x in open(
                    f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y))])}"
                    ).read().splitlines() if x != ""]).split("\n")[0]
                print(gif)
            await ctx.reply(gif)
        except Exception:
            await ctx.reply("Source Not Available")

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def star_random(self, ctx):
        try:
            gif = random.choice([x for x in open(
                f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y))])}"
            ).read().splitlines() if x != ""])
            if "\\n" in gif:
                gif = gif.replace("\\n", "\n")
            await ctx.reply(gif)
        except Exception:
            await ctx.reply("Source Not Available")


async def setup(client):
    await client.add_cog(Starkid(client))
