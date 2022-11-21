# cogs / sleeps.py

from discord import Embed
from discord.ext import commands
import random


class Sleep(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    async def sleeps_me(self, ctx):
        embed_var = Embed(title="I sleeps now")
        embed_var.set_image(url=random.choice(open("gifs/sleep_me").read().splitlines()))
        await ctx.reply(embed=embed_var)


    @commands.hybrid_command()
    async def sleeps_you(self, ctx):
        embed_var = Embed(title="You sleep now")
        embed_var.set_image(url=random.choice(open("gifs/sleep_u").read().splitlines()))
        await ctx.reply(embed=embed_var)


    @commands.hybrid_command()
    async def sleeps_lyr(self, ctx):
        embed_var = Embed(title="BB sleep now", description="pls bb")
        embed_var.set_image(url="https://media.tenor.com/xvey88HHrSIAAAAC/pls-go-to-sleep-sleep-or-cry.gif")
        await ctx.reply(embed=embed_var)



async def setup(client):
    await client.add_cog(Sleep(client))
