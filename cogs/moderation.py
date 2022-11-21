# cogs / moderation.py
import random

import discord
from discord import Embed
from discord.ext import commands
import time


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    mod_channels = {"917901239306575902":1038967126091890719,"1039953198359781446":1040383695468634212}
    servers = [917901239306575902,1039953198359781446]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id in self.servers:
            mod_channels = self.mod_channels
            mod_channel = mod_channels[f"{message.guild.id}"]
    
    
            if "||​||||​||" * 20 in message.content.lower():
                time.sleep(1)
                await message.delete()
                await message.channel.send("Message deleted due to rule breaking")
                embed_var = Embed(title=f"Rule #420.69 Broken by {message.author.name}", color=0x5f1138)
                embed_var.set_author(name=message.author, icon_url=message.author.avatar.url)
                embed_var.add_field(name="Date",
                                    value=f"<t:{int(message.created_at.timestamp())}:F>",
                                    inline=False)
                embed_var.add_field(name="ID",
                                    value=f"```ini\nUser = {message.author.id}\nMessage = {message.id}```",
                                    inline=False)
                # for mod_channel in mod_channels:
                await self.client.get_channel(mod_channel).send(embed=embed_var)


async def setup(client):
    await client.add_cog(Moderation(client))
