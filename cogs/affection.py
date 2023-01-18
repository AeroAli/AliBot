# cogs / affection.py
import csv
import random

import discord
from discord import Embed
from discord.ext import commands


class Affection(commands.Cog):
    """Affectionate commands"""
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


    # Boop
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def boop(self, ctx, user: discord.User):
        """boop @user"""
        chosen = random.choice(self.global_gif_dict["boop"])
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} boops <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} boops {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="BOOPS", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Cuddle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def cuddle(self, ctx, user: discord.User):
        """cuddle @user"""
        chosen = random.choice(self.global_gif_dict["cuddle"])
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} cuddles <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} cuddles {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="CUDDLES", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Hug
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, user: discord.User):
        """hug @user"""
        chosen = random.choice(self.global_gif_dict["hug"])
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} hugs <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} hugs {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="HUGS", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Tackle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def tackle(self, ctx, user: discord.User):
        """tackle @user"""
        chosen = random.choice(self.global_gif_dict["tackle"])
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} tackles <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} tackles {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="TACKLE TIME", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Scritches
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def scritches(self, ctx, user: discord.User):
        """scritch @user"""
        chosen = random.choice(self.global_gif_dict["scritch"])
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} scritches <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} scritches {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="SCRITCHES", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Pat
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def pat(self, ctx, user: discord.User):
        """punch @user"""
        chosen = random.choice(self.global_gif_dict["pat"])
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} pats <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} pats {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="*PATS*", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Squish
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def squish(self, ctx, user: discord.User):
        """squish @user"""
        chosen = random.choice(self.global_gif_dict["squish"])
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} squishes <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} squishes {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="SQUISH", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Fav
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def glomp(self, ctx, user: discord.User):
        """glomps @user"""
        chosen = random.choice(self.global_gif_dict["favs"])
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} attacks (affectionate) <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} attacks (affectionate) {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="HUG!!!!!!", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Poke
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def poke(self, ctx, user: discord.User):
        """pokes"""
        embed_var = Embed(title=f"poke {user.display_name}")
        # embed_var.set_image(url="https://media.tenor.com/9bPsSkaKgVsAAAAC/poke-gif")
        embed_var.set_image(url="https://cdn.weeb.sh/images/rktSlkKvb.gif")
        await ctx.reply(f"<@!{user.id}>", embed=embed_var)

    # Happy Bot
    @commands.Cog.listener()
    async def on_message(self, message):
        if "hugbot" in message.content.lower() and "love" in message.content.lower():
            # https://cdn.discordapp.com/emojis/1036757258006167703.gif?size=96&quality=lossless
            emoji = self.client.get_emoji(1036757258006167703)
            await message.add_reaction(emoji)

    # eldritch
    # flirt
    # MemeHug
    # reaction - Y
    # debug?
    # bOnk!

async def setup(client):
    await client.add_cog(Affection(client))