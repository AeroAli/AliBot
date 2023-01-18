# cogs / actions.py

import csv
import random

from discord import Embed
from discord.ext import commands


class Actions(commands.Cog):
    """Action commands"""
    def __init__(self, client):
        self.client = client

    global_gif_dict = {}
    with open("gifs/hug_cog.csv", "r") as f:
        csv_rows = csv.reader(f, delimiter=",")
        rows = list(csv_rows)
        for row in rows:
            key = str(row[1])
            if key in global_gif_dict:
                global_gif_dict[key].append(row)
            else:
                global_gif_dict[key] = [row]

    # Rhea is disappointed in you
    @commands.hybrid_command()
    async def disappoint(self, ctx):
        """Rhea is disappointed in you"""
        gif = "https://media.tenor.com/YhrJ_-g-CYMAAAAC/rhea-ripley-annoyed.gif"

        quote = "Come on, really?"
        embed_var = Embed(title=quote)
        embed_var.set_image(url=gif)

        await ctx.reply(embed=embed_var)

    # Gay
    @commands.hybrid_command()
    async def gay(self, ctx):
        """gaaaaaaaaaaaaaay"""
        embed_var = Embed(title="gaaaaaaaaaay")
        chosen = random.choice(self.global_gif_dict["gay"])
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

    # Wave
    @commands.hybrid_command()
    async def wave(self, ctx):
        """friendly greeting"""
        embed_var = Embed(title="HI!!!!!!")
        chosen = random.choice(self.global_gif_dict["wave"])
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

    # Bot is alive
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def alive(self, ctx):
        """alive"""
        embed_var = Embed(title=f"IT'S ALIVE!!!")
        embed_var.set_image(url="https://media.tenor.com/SuADVxKkQ-AAAAAC/frankenstein-its-alive.gif")
        await ctx.reply(embed=embed_var)

    # Bot broke :'(
    @commands.hybrid_command()
    async def broke(self, ctx):
        """it broke :'("""
        embed_var = Embed(title="it broke :\'(")
        chosen = random.choice(self.global_gif_dict["broke"])
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

    # Google It
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def google(self, ctx):
        """google it moron"""
        chosen = random.choice(self.global_gif_dict["google"])
        hug_choice = chosen[2]
        message = [f"Google it",  # nice
                   f"Google it, bitch"]  # rude
        print(hug_choice)
        embed_var = Embed(title="GOOGLE IT", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Actions(client))
