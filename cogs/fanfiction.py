# cogs / fanfiction.py

import json
import csv
import random

from discord import Embed
from discord.ext import commands


class Fanfiction(commands.Cog):
    """fnafiction cog"""
    def __init__(self, client):
        self.client = client


    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def librarian(self, ctx):
        """embeds of fanfiction libraries"""
        with open(r"gifs/libraries.json", "r") as k:
            libraries = json.load(k)
            for librarian in libraries:
                for key, value1 in librarian.items():
                    if key != "Darth":
                        embed_var = Embed(title=key)
                        for key2, value2 in value1.items():
                            if key2 == "User ID" and value2:
                                author = await self.client.fetch_user(int(value2))
                                embed_var.set_author(name=author, icon_url=author.avatar.url)
                            if value2 and key2 != "User ID":
                                #embed_var.add_field(name=key2, value=value2)
                                if type(value2) != list:
                                    print("\t",key2, " : \n\t\t", value2, "\n")
                                    embed_var.add_field(name=key2, value=value2, inline=False)
                                else:
                                    print("\t",key2," : ")
                                    [print("\t\t\t",x) for x in value2]
                                    embed_var.add_field(name=key2, value=",".join([f"`{server}`\n" for server in value2]), inline=False)
                        await ctx.reply(embed=embed_var)


async def setup(client):
  await client.add_cog(Fanfiction(client))