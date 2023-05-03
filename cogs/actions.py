# cogs / actions.py

import csv
import random

from discord import Embed
from discord.ext import commands


class Actions(commands.Cog):
    """Action commands"""
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


        # UwU time
        @commands.hybrid_command()
        async def uwuify(self, ctx, message: str):
            """UWU time"""
            emoji = random.choice(["<:bearplead:1089420946869329930>", "<:blobnervouspleading:1089651961562943589>",
                                   "<:bls:1090293496704946308>", "<:isforme:1089420731248541699>",
                                   "<:plead:1089655897728503918>", "<:pleading:1089420556656447498>",
                                   "< a:pleadingpoint:1090292618665148448>", "<:pleadingtaco:1089650935275475005>",
                                   "<:please:1089651526789767300>", "<:please:1090293064360263751>",
                                   "<:please:1090293312512082021>", "<a:please:1090293872380362893>",
                                   "<:please:1090294316171284660>", "<a:please:1090294795617960026>",
                                   "<a:pleadingpoint:1089415562158952540>", "<:isforme:1089417637915791390>"])

            await ctx.reply(
                 "OwO " +
                message
                .replace("u", "uwu")
                .replace("o", "owo")
                .replace("U", "Uwu")
                .replace("O", "Owo")
                .replace("l", "w")
                .replace("att", "awatt")
                # .replace("t", "w")
                # .replace("T", "W")
                .replace("L", "W")
                .replace("r", "w")
                .replace("R", "W")
                .replace("uwuwuwu", "uwu")
                .replace("wuwuw", "wuw")
                .replace("owowowo", "owo")
                .replace("wowow", "wow")
                .replace("ww", "w")
                # .replace("wa", "awa")
                + f" UwU\n{emoji}"
            )
            await ctx.channel.send(f"{emoji}")
        

    # Rhea is disappointed in you
    @commands.hybrid_command()
    async def disappoint(self, ctx):
        """Rhea is disappointed in you"""
        gif = "https://media.tenor.com/YhrJ_-g-CYMAAAAC/rhea-ripley-annoyed.gif"

        quote = "Come on, really?"
        embed_var = Embed(title=quote)
        embed_var.set_image(url=gif)

        await ctx.reply(embed=embed_var)

    # Liv is confused
    @commands.hybrid_command()
    async def what(self, ctx):
        """Liv is confused"""
        gif = "https://media.tenor.com/bjSe9759nMEAAAAd/liv-morgan-liv.gif"

        quote = "Excuse me, WHAT?"
        embed_var = Embed(title=quote)
        embed_var.set_image(url=gif)

        await ctx.reply(embed=embed_var)

    # Gay
    @commands.hybrid_command()
    async def gay(self, ctx):
        """gaaaaaaaaaaaaaay"""
        embed_var = Embed(title="gaaaaaaaaaay")
        chosen = random.choice(self.global_gif_dict["gay"])
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

    # Wave
    @commands.hybrid_command()
    async def wave(self, ctx):
        """friendly greeting"""
        embed_var = Embed(title="HI!!!!!!")
        chosen = random.choice(self.global_gif_dict["wave"])
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

    # Bot is alive
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def alive(self, ctx):
        """alive"""
        embed_var = Embed(title=f"IT'S ALIVE!!!")
        embed_var.set_image(url="https://media.tenor.com/SuADVxKkQ-AAAAAC/frankenstein-its-alive.gif")
        await ctx.reply(embed=embed_var)

    # Bot broke :'(
    @commands.hybrid_command()
    async def broke(self, ctx):
        """it broke :'("""
        embed_var = Embed(title="it broke :\'(")
        chosen = random.choice(self.global_gif_dict["broke"])
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

    # Google It
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def google(self, ctx):
        """google it moron"""
        chosen = random.choice(self.global_gif_dict["google"])
        hug_choice = chosen[2]
        message = [f"Google it",  # nice
                   f"Google it, bitch"]  # rude
        print(hug_choice)
        embed_var = Embed(title="GOOGLE IT", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)

    # SULK
    @commands.hybrid_command()
    async def sulk(self, ctx):
        """me mad, me sulk"""
        # chosen = random.choice(self.global_gif_dict["google"])
        # hug_choice = chosen[2]
        hug_choice = "https://media.tenor.com/LBkpAQ_lPzMAAAAC/sulk-mad.gif"
        message = [f"me mad, me sulk"]  # pout
        print(hug_choice)
        embed_var = Embed(title="SULK", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Actions(client))
