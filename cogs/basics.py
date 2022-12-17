# cogs / basics.py

import random
import csv

import discord
from discord import Embed
from discord.ext import commands


class Basic(commands.Cog):
    def __init__(self, client):
        self.client = client

    with open("gifs/hug_cog.csv", "r") as f:
        # rows = csv.DictReader(f)
        csv_rows = csv.reader(f, delimiter=",")
        rows = list(csv_rows)
        # print(type(rows))
        gays = [row for row in rows if row[1] == 'gay']
        brokes = [row for row in rows if row[1] == 'broke']
        waves = [row for row in rows if row[1] == 'wave']

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

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def choose(self, ctx, choice_in: str):
        """Chooses between multiple choices, splits at "," """
        choices = choice_in.split(",")
        await ctx.reply(random.choice(choices))

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        await ctx.reply(left + right)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def poke(self, ctx, user: discord.User):
        """pokes"""
        embed_var = Embed(title=f"poke {user.display_name}")
        # embed_var.set_image(url="https://media.tenor.com/9bPsSkaKgVsAAAAC/poke-gif")
        embed_var.set_image(url="https://cdn.weeb.sh/images/rktSlkKvb.gif")
        await ctx.reply(f"<@!{user.id}>",embed=embed_var)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def alive(self, ctx):
        """alive"""
        embed_var = Embed(title=f"IT'S ALIVE!!!")
        embed_var.set_image(url="https://media.tenor.com/SuADVxKkQ-AAAAAC/frankenstein-its-alive.gif")
        await ctx.reply(embed=embed_var)

    
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def hello(self, ctx):
        await ctx.reply(f"Hello {ctx.author.mention}")

    @commands.hybrid_command()
    async def broke(self, ctx):
        embed_var = Embed(title="it broke :\'(")
        chosen = random.choice(self.brokes)
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)
        
    @commands.hybrid_command()
    async def gay(self, ctx):
        embed_var = Embed(title="gaaaaaaaaaay")
        chosen = random.choice(self.gays)
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)
        
    @commands.hybrid_command()
    async def wave(self, ctx):
        embed_var = Embed(title="HI!!!!!!")
        chosen = random.choice(self.waves)
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

async def setup(client):
    await client.add_cog(Basic(client))
