# cogs / vibes.py

import csv
import random

from discord import Embed
from discord.ext import commands


class Vibe(commands.Cog):
    """vibing commands"""
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

    # Rhea
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def queen(self, ctx):
        """Rhea Ripley my beloved"""
        message = ["All hail the queen of the ring",
                   "could snap me like a twig and i'd thank her",
                   "*fans myself*",
                   "step on my neck, *please*"]

        chosen = random.choice(self.global_gif_dict["rhea"])
        rhea_choice = chosen[2]
        print(rhea_choice)
        embed_var = Embed(title="Rhea Ripley", description=random.choice(message))
        embed_var.set_image(url=rhea_choice)

        await ctx.reply(embed=embed_var)

    # Dodie
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def dodie(self, ctx):
        """Dodie!!!"""
        message = ["is it dodie yellow tho"]

        chosen = random.choice(self.global_gif_dict["dodie"])
        rhea_choice = chosen[2]
        print(rhea_choice)
        embed_var = Embed(title="DODIE CLARKE!!!!!", description=random.choice(message))
        embed_var.set_image(url=rhea_choice)

        await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Vibe(client))
