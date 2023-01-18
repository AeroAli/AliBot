# cogs / sleeps.py

import csv
import random

import discord
from discord import Embed
from discord.ext import commands


class Sleep(commands.Cog):
    """Sleepy commands"""
    def __init__(self, client):
        self.client = client

    imprisoned = [959480822988161095]

    with open("gifs/hug_cog.csv", "r") as f:
        # rows = csv.DictReader(f)
        csv_rows = csv.reader(f, delimiter=",")
        rows = list(csv_rows)
        sleep_me = [row for row in rows if row[1] == 'sleep_me' or row[1] == 'sleep']
        sleep_u = [row for row in rows if row[1] == 'sleep_u' or row[1] == 'sleep']


    @commands.hybrid_command()
    async def sleeps_me(self, ctx):
        """Bed Time for me"""
        embed_var = Embed(title="Night")
        chosen = random.choice(self.sleep_me)
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)


    @commands.hybrid_command()
    async def sleeps_you(self, ctx, user: discord.User):
        """Tells inputted user to go to bed"""
        embed_var = Embed(title="You sleep now")
        chosen = random.choice(self.sleep_u)
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(f"<@{user.id}>", embed=embed_var)


    @commands.hybrid_command()
    async def sleeps_lyr(self, ctx):
        """Guilt Lyr into sleeping"""
        if ctx.author.id not in self.imprisoned:
            embed_var = Embed(title="BB sleep now", description="pls bb")
            embed_var.set_image(url="https://media.tenor.com/xvey88HHrSIAAAAC/pls-go-to-sleep-sleep-or-cry.gif")
            await ctx.reply(f"<@778387002004471829>",embed=embed_var)



async def setup(client):
    await client.add_cog(Sleep(client))
