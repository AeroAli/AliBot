# cogs / hugs.py
import random

import discord
from discord import Embed
from discord.ext import commands


class Hug(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Hug
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, user: discord.User):
        hug_choice = random.choice(open("gifs/hugs").read().splitlines())
        message = [f"{ctx.author.display_name} hugs <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} hugs {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="HUGS",description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)

    # Tackle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def tackle(self, ctx, user: discord.User):
        hug_choice = random.choice(open("gifs/tackles").read().splitlines())
        message = [f"{ctx.author.display_name} tackles <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} tackles {user.display_name}"]  # author hugs user
        embed_var = Embed(title="TACKLE TIME", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "hugbot" in message.content.lower() and "love" in message.content.lower():
            # https://cdn.discordapp.com/emojis/1036757258006167703.gif?size=96&quality=lossless
            emoji = self.client.get_emoji(1036757258006167703)
            await message.add_reaction(emoji)

     
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def scritches(self, ctx, user: discord.User):
        hug_choice = random.choice(open("gifs/scritches").read().splitlines())
        message = [f"{ctx.author.display_name} scritches <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} scritches {user.display_name}"]  # author hugs user
        embed_var = Embed(title="SCRITCHES", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def squish(self, ctx, user: discord.User):
        hug_choice = random.choice(open("gifs/squishes").read().splitlines())
        message = [f"{ctx.author.display_name} squishes <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} squishes {user.display_name}"]  # author hugs user
        embed_var = Embed(title="SQUISH", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(embed=embed_var)
 
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def fav(self, ctx, user: discord.User):
        hug_choice = random.choice(open("gifs/squishes").read().splitlines())
        message = [f"{ctx.author.display_name} attacks (affectionate) <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} attacks (affectionate) {user.display_name}"]  # author hugs user
        embed_var = Embed(title="HUG!!!!!!", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(embed=embed_var)
 
    # eldritch
    # flirt
    # Pat
    # Glomp
    # MemeHug
    # reaction - Y
    # embed - Y
    # debug?


async def setup(client):
    await client.add_cog(Hug(client))
