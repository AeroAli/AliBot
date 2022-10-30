# cogs / hugs.py
import random
import discord
from discord.ext import commands


class Hug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, user: discord.User):
        hug_choice = random.choice(open("hugs").read().splitlines())
        message = f"{ctx.author.mention} hugs <@{user.id}>"
        await ctx.reply(message)
        await ctx.reply(content=hug_choice)


async def setup(client):
    await client.add_cog(Hug(client))
