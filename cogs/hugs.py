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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, user: discord.User):
        hug_choice = random.choice(open("hugs").read().splitlines())

        # random.choices()

        message = [f"{ctx.author.name} hugs <@{user.id}>",  # author hugs @user
                   f"{ctx.author.name} hugs {user.name}",  # author hugs user
                   f"{ctx.author.id} hugs <@{user.name}>",  # @author hugs user
                   f"{ctx.author.id} hugs <@{user.id}>"]  # @author hugs @user

        embed_var = Embed(title=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)

    # Tackle
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tackle(self, ctx, user: discord.User):
        hug_choice = random.choice(open("tackles").read().splitlines())
        message = [f"{ctx.author.name} hugs <@{user.id}>",  # author hugs @user
                   f"{ctx.author.name} hugs {user.name}",  # author hugs user
                   f"{ctx.author.id} hugs <@{user.name}>",  # @author hugs user
                   f"{ctx.author.id} hugs <@{user.id}>"]  # @author hugs @user
        embed_var = Embed(title=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "hugbot" in message.content.lower() and "love" in message.content.lower():
            # https://cdn.discordapp.com/emojis/1036757258006167703.gif?size=96&quality=lossless
            emoji = self.client.get_emoji(1036757258006167703)
            await message.add_reaction(emoji)

    # hug
    # tackle
    # scritches
    # squish
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
