# cogs / vibes.py

import csv
import random

import discord
from discord import Embed
from discord.ext import commands


class Vibe(commands.Cog):
    """vibing commands"""
    def __init__(self, client):
        self.client = client

    hugging_table = "hug_cog"


    async def get_hugged(self, action):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"SELECT * FROM `{self.hugging_table}` where category_name='{action}' ORDER BY RAND() LIMIT 1")
                # print(cur.description)
                result = await cur.fetchone()
                return result

    # Bahaj
    @commands.hybrid_command()
    async def blahaj(self, ctx):
        """SHAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAARK"""
        message = ["SHAAAAAAAAAAAAAAAAAAAAAAAAAAAARK",
                   "Blahaj",
                   "Blahaj, my beloved"]
        embed_var = Embed(title="BLAHAJ", description=random.choice(message))
        chosen = await self.get_hugged("shark")
        rhea_choice = chosen[2]
        print(rhea_choice)
        embed_var.set_image(url=rhea_choice)

        await ctx.reply(embed=embed_var)


    # Dodie
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def dodie(self, ctx):
        """Dodie!!!"""
        message = ["is it dodie yellow tho",
                   "Dodie <3"]

        chosen = await self.get_hugged("dodie")
        rhea_choice = chosen[2]
        print(rhea_choice)
        embed_var = Embed(title="DODIE CLARKE!!!!!", description=random.choice(message))
        embed_var.set_image(url=rhea_choice)

        await ctx.reply(embed=embed_var)


    # Bulli
    @commands.hybrid_command()
    async def bulli(self, ctx, user: discord.User):
        """Bulli Time"""
        image = "https://i.giphy.com/PjrXOMmxKtJTHmO6RG.gif"
        message = [f"{ctx.author.display_name} bullis <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} bullis {user.display_name}"]  # author hugs user
        print(image)
        embed_var = Embed(title="HUGS", description=random.choice(message))
        embed_var.set_image(url=image)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)


    # LoveThat
    @commands.hybrid_command()
    async def lovethat(self, ctx):
        """Love That"""
        image = "https://cdn.discordapp.com/attachments/1042563646309552199/1083429354803036321/Xt2CsC9.gif"
        message = [f"love that"]  # author hugs user
        print(image)
        embed_var = Embed(title="Love That", description=random.choice(message))
        embed_var.set_image(url=image)

        await ctx.reply(embed=embed_var)


    # Pina
    @commands.hybrid_command()
    async def bestest_girl(self, ctx):
        """Pina"""
        image = "https://media.tenor.com/dzq5zYUZB7IAAAAC/loli-bite.gif"
        message = [f"bestest girl", "adorable smol cute feral murder child"]  # author hugs user
        print(image)
        embed_var = Embed(title="Pina", description=random.choice(message))
        embed_var.set_image(url=image)

        await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Vibe(client))
