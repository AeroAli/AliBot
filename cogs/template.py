# cogs / template.py

from discord import Embed
from discord.ext import commands


class Template(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def example(self, ctx, input_var):
        embed_var = Embed
        await ctx.reply(f"Hello {ctx.author.mention}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if "ALI IS THE GREATEST".lower() in message.content:
            emoji = self.client.get_emoji(1036757258006167703)
            await message.add_reaction(emoji)


async def setup(client):
    await client.add_cog(Template(client))
