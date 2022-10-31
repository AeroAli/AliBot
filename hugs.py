# cogs / hugs.py
import random
import discord
from discord.ext import commands


class Hug(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Hug
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, user: discord.User):
        hug_choice = random.choice(open("hugs").read().splitlines())
        # message = f"{ctx.author.name} hugs <@{user.id}>"  # author hugs @user
        message = f"{ctx.author.name} hugs {user.name}" # author hugs user
        # message = f"{ctx.author.id} hugs <@{user.name}>" # @author hugs user
        # message = f"{ctx.author.id} hugs <@{user.id}>" # @author hugs @user
        await ctx.reply(message)
        await ctx.reply(content=hug_choice)

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
    # reaction
    # debug? - google


async def setup(client):
    await client.add_cog(Hug(client))
