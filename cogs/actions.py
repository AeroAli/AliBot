# cogs / actions.py

import csv
import random

import discord
from discord import Embed
from discord.ext import commands


class Actions(commands.Cog):
    """Action commands"""
    def __init__(self, client):
        self.client = client

    # friends = [
    #     158646501696864256,
    #     689522335119966258,
    #     453534487343792130,
    #     444564239911354368,
    #     702162355844284489,
    #     372667623269335042
    # ]

    hugging_table = "hug_cog"

    async def get_hugged(self, action):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT * FROM `{self.hugging_table}` where category_name='{action}' ORDER BY RAND() LIMIT 1")
                # print(cur.description)
                result = await cur.fetchone()
                return result


    # UwU time
    @commands.hybrid_command()
    async def uwuify(self, ctx, message: str):
        """UWU time"""
        emoji = random.choice(["<:bearplead:1089420946869329930>", "<:blobnervouspleading:1089651961562943589>",
                               "<:bls:1090293496704946308>", "<:isforme:1089420731248541699>",
                               "<:plead:1089655897728503918>", "<:pleading:1089420556656447498>",
                               "<a:pleadingpoint:1090292618665148448>", "<:pleadingtaco:1089650935275475005>",
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
            + f" UwU"#\n{emoji}"
        )
        await ctx.channel.send(f"{emoji}{emoji}")
        

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
        chosen = await self.get_hugged("gay")
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

    # Wave
    @commands.hybrid_command()
    async def wave(self, ctx):
        """friendly greeting"""
        embed_var = Embed(title="HI!!!!!!")
        chosen = await self.get_hugged("wave")
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
        chosen = await self.get_hugged("broke")
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(embed=embed_var)

    # Google It
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def google(self, ctx):
        """google it moron"""
        chosen = await self.get_hugged("google")
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
        # chosen = await self.get_hugged("google")
        # hug_choice = chosen[2]
        hug_choice = "https://media.tenor.com/LBkpAQ_lPzMAAAAC/sulk-mad.gif"
        message = [f"**huffs**"]  # pout
        print(hug_choice)
        embed_var = Embed(title="SULK", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(embed=embed_var)

    @commands.hybrid_command()
    async def quotation(self, ctx, user: discord.User, *, message: str):
        """Post a fake quote from someone else"""
        embed_var = Embed(description=message)
        author = user
        embed_var.set_author(name=author.display_name, icon_url=author.display_avatar)
        await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Actions(client))
