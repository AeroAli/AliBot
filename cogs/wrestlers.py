# cogs / template.py
import csv
import random

from discord import Embed
from discord.ext import commands


class Wrestlers(commands.Cog):
    """Wrestler gifs"""
    def __init__(self, client):
        self.client = client

    global_gif_dict = {}
    with open("gifs/wrestler_cog.csv", "r") as f:
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
                   "could snap me like a twig and i'd thank her *send tweet*",
                   "step on my neck,\n*please*"]

        chosen = random.choice(self.global_gif_dict["rhea"])
        rhea_choice = chosen[2]
        print(rhea_choice)
        embed_var = Embed(title="Rhea Ripley", description=random.choice(message))
        embed_var.set_image(url=rhea_choice)

        await ctx.reply(embed=embed_var)

    # Alba Fyre
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def fyre(self, ctx):
        """Alba Fyre"""
        message = ["*fans myself*"]

        chosen = random.choice(self.global_gif_dict["alba_fyre"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Alba Fyre", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Seth Rollins
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def freekin(self, ctx):
        """Seth Rollins"""
        message = ["Seth Freakin Rollins"]
        chosen = random.choice(self.global_gif_dict["seth_rollins"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Seth Rollins", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Drew  McIntyre
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def claymore(self, ctx):
        """Drew McIntyre"""
        message = [""]

        chosen = random.choice(self.global_gif_dict["drew_mcintyre"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Drew McIntyre")  # , description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # brock_lesnar
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def angyboi(self, ctx):
        """Brock Lesnar"""
        emoji = self.client.get_emoji(954431171247370240)
        message = [f"Someone's unhappy  {emoji}"]

        chosen = random.choice(self.global_gif_dict["brock_lesnar"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Brock Lesnar", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Bray Wyatt
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def wyatt(self, ctx):
        """Bray Wyatt"""
        message = []

        chosen = random.choice(self.global_gif_dict["bray_wyatt"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Bray Wyatt")  # , description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # nikki_cross
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def nikki(self, ctx):
        """Nikki Cross"""
        message = ["*fans myself*"]

        chosen = random.choice(self.global_gif_dict["nikki_cross"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Nikki Cross", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

        # asuka

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def hime(self, ctx):
        """asuka"""
        message = ["*fans myself*"]

        chosen = random.choice(self.global_gif_dict["asuka"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Asuka", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # cody_rhodes
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def cody(self, ctx):
        """Cody Rhodes"""
        message = []

        chosen = random.choice(self.global_gif_dict["cody_rhodes"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Cody Rhodes")  # , description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # liv_morgan
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def tiny(self, ctx):
        """Liv Morgan my beloved"""
        message = ["*fans myself*"]

        chosen = random.choice(self.global_gif_dict["liv_morgan"])
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Liv Morgan", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Wrestlers(client))
