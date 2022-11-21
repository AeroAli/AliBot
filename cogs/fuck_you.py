# cogs / template.py

from discord import Embed
from discord.ext import commands


class Fuck_U(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    async def fuck_u(self, ctx):
        if ctx.author.id == 689522335119966258 and ctx.guild.id == 1039953198359781446:
            try:
                gif = "https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif"
                quote = "Fuck You Thanos"
                # quote = "Fuck You"
                author = await self.client.fetch_user(158646501696864256)
                embed_var = Embed(title=quote)
                embed_var.set_author(name=author, icon_url=author.avatar.url)
                embed_var.set_image(url=gif)
                await ctx.send(embed=embed_var)
                print(gif, quote)
            except Exception as e:
                print(e)
                await ctx.reply("Source Not Available")


async def setup(client):
    await client.add_cog(Fuck_U(client))
