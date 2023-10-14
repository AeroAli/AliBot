# cogs / affection.py
import csv
import random
import traceback

import discord
from discord import Embed
from discord.ext import commands


class Affection(commands.Cog):
    """Affectionate commands"""
    def __init__(self, client):
        self.client = client

    hugging_table = "hug_cog"
    affection_list = ("boop","cuddle","hug","tackle","scritch","pat","squish","favs")


    async def cog_command_error(self, ctx, error: Exception) -> None:
        traceback.print_exception(error)

    async def get_hugged(self, action):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT * FROM `{self.hugging_table}` where category_name='{action}' ORDER BY RAND() LIMIT 1")
                # print(cur.description)
                result = await cur.fetchone()
                print(result)
                return result

    async def action_count(self):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT category_name, COUNT(*) AS `num` FROM hug_cog WHERE category_name IN {self.affection_list} GROUP BY category_name ORDER BY category_name")
                result = await cur.fetchall()
                return result



    # Boop
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def boop(self, ctx, user: discord.User):
        """boop @user"""
        chosen = await self.get_hugged("boop")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} boops <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} boops {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="BOOPS", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Cuddle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def cuddle(self, ctx, user: discord.User):
        """cuddle @user"""
        chosen = await self.get_hugged("cuddle")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} cuddles <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} cuddles {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="CUDDLES", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Hug
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, user: discord.User):
        """hug @user"""
        chosen = await self.get_hugged("hug")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} hugs <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} hugs {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="HUGS", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Tackle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def tackle(self, ctx, user: discord.User):
        """tackle @user"""
        chosen = await self.get_hugged("tackle")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} tackles <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} tackles {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="TACKLE TIME", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Scritches
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def scritches(self, ctx, user: discord.User):
        """scritch @user"""
        chosen = await self.get_hugged("scritch")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} scritches <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} scritches {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="SCRITCHES", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Pat
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def pat(self, ctx, user: discord.User):
        """pat @user"""
        chosen = await self.get_hugged("pat")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} pats <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} pats {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="*PATS*", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Squish
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def squish(self, ctx, user: discord.User):
        """squish @user"""
        chosen = await self.get_hugged("squish")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} squishes <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} squishes {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="SQUISH", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Fav
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def glomp(self, ctx, user: discord.User):
        """glomps @user"""
        chosen = await self.get_hugged("favs")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} attacks (affectionate) <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} attacks (affectionate) {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="HUG!!!!!!", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Poke
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def poke(self, ctx, user: discord.User):
        """pokes"""
        embed_var = Embed(title=f"poke {user.display_name}")
        # embed_var.set_image(url="https://media.tenor.com/9bPsSkaKgVsAAAAC/poke-gif")
        embed_var.set_image(url="https://cdn.weeb.sh/images/rktSlkKvb.gif")
        await ctx.reply(f"<@!{user.id}>", embed=embed_var)

    # # Happy Bot
    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     if "hugbot" in message.content.lower() and "love" in message.content.lower():
    #         # https://cdn.discordapp.com/emojis/1036757258006167703.gif?size=96&quality=lossless
    #         emoji = self.client.get_emoji(1036757258006167703)
    #         await message.add_reaction(emoji)


    @commands.hybrid_command()
    async def affection_gifs(self, ctx):
        """get all gifs used in this cog"""
        actions = await self.action_count()
        des = "\n".join(f"""***`{name:<15}`***| {'*' + str(gif_count):>3}*""" for name, gif_count in actions)
        gif_sum = sum(gif_count for _, gif_count in actions)
        des += f"""\n`-------------------`\n**__`Total         | {gif_sum}`__**"""
        embed_var = Embed(title="**__Action | Count__**", description=des)
        await ctx.reply(embed=embed_var)


    # eldritch
    # flirt
    # MemeHug
    # reaction - Y
    # debug?
    # bOnk!

async def setup(client):
    await client.add_cog(Affection(client))
