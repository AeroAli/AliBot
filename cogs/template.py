# cogs / template.py
import csv
import random

from discord import Embed
from discord.ext import commands


class Template(commands.Cog):
    """template cogs"""
    def __init__(self, client):
        self.client = client

    global_gif_dict = {}
    with open("gifs/hug_cog.csv", "r") as f:
        csv_rows = csv.reader(f, delimiter=",")
        rows = list(csv_rows)
        for row in rows:
            key = str(row[1])
            if key in global_gif_dict:
                global_gif_dict[key].append(row)
            else:
                global_gif_dict[key] = [row]

    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def example(self, ctx):
        """example command and embed"""
        embed_var = Embed(title="​")
        chosen = random.choice(self.global_gif_dict["wave"])
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(f"Hello {ctx.author.mention}", embed=embed_var)

    @commands.Cog.listener()
    async def on_message(self, message):
        """egocentric on_message"""
        if "ALI IS THE GREATEST".lower() in message.content:
            emoji = self.client.get_emoji(1036757258006167703)
            await message.add_reaction(emoji)


async def setup(client):
    await client.add_cog(Template(client))
