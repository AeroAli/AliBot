# cogs / treehouse.py

from discord import Embed
from discord.ext import commands


class Treehouse(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gif(self, ctx):
        approved_users = [372667623269335042, 116378164229308421, 246456382352654342, 429808068294082561]
        if ctx.author.id in approved_users:
            embed_var = Embed(title="​")
            embed_var.set_image(url="https://cdn.discordapp.com/attachments/961683573079957594/1039978776018292736/Twisted_Sams_Fault.gif")
            await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Treehouse(client))
