# cogs / template.py

import random

from discord import Embed
from discord.ext import commands


class Fuck_U(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    async def fuck_u(self, ctx):
        if ctx.author.id == 689522335119966258:
            try:
                gif = ["https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif",
                        "https://media.discordapp.net/attachments/804032059830960198/1043558047311732817/Hatchetfield_Fuck_You.gif",
                        "https://cdn.discordapp.com/attachments/1020759712590991423/1047618138553987232/fuck-you-lauren.gif"]
                quote = "Fuck You"
                # quote = "Fuck You"
                author = await self.client.fetch_user(158646501696864256)
                embed_var = Embed(title=quote)
                # embed_var.set_author(name=author, icon_url=author.avatar.url)
                embed_var.set_image(url=random.choice(gif))
                await ctx.send(embed=embed_var)
                print(gif, quote)
            except Exception as e:
                print(e)
                await ctx.reply("Source Not Available")


async def setup(client):
    await client.add_cog(Fuck_U(client))
