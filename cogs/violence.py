# cogs / violence.py
import random
import traceback

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands._types import BotT

import utils.checks
from utils.errors import BabbyProofing


class Violence(commands.Cog):
    """violent commands"""
    def __init__(self, client):
        self.client = client

    imprisoned = [959480822988161095]

    hugging_table = "hug_cog"
    violence_list = ("baka", "kick", "tazer", "nohorny", "punch", "slap", "nom", "kill","headbutt") # ToDo have a de-lewder for nohonry


    async def cog_check(self, ctx: Context[BotT]) -> bool:
        not_babby = utils.checks.is_blocked().predicate
        return await not_babby(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: Exception) -> None:
        if isinstance(error, BabbyProofing):
            embed_var = discord.Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
            traceback.print_exception(error)
            if ctx.guild.id == 1039953198359781446:
                error = getattr(error, "original", error)
                await ctx.send(embed=Embed(title=f"{type(error).__name__}", description=f"{error}", colour=0xC70039))

    async def get_hugged(self, action):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"SELECT * FROM `{self.hugging_table}` where category_name='{action}' ORDER BY RAND() LIMIT 1")
                # print(cur.description)
                result = await cur.fetchone()
                return result


    async def action_count(self):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT category_name, COUNT(*) AS `num` FROM hug_cog WHERE category_name IN {self.violence_list} GROUP BY category_name ORDER BY category_name")
                result = await cur.fetchall()
                return result

    # Baka
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def baka(self, ctx, user: discord.User):
        """bakaaaaaaaa @user"""
        chosen = await self.get_hugged("baka")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} condemns <@{user.id}> for extreme dumbfuckery",  # author hugs @user
                   f"{ctx.author.display_name} condemns {user.display_name} for extreme dumbfuckery"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="BAKAAAAAAAA", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Kick
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick_em(self, ctx, user: discord.User):
        """kick @user"""
        chosen = await self.get_hugged("kick")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} kicks <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} kicks {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="KICK", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Tazer
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def taze(self, ctx, user: discord.User):
        """taze @user"""
        chosen = await self.get_hugged("tazer")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} tazes <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} tazes {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="oops?", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Bonk
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def bonk(self, ctx, user: discord.User):
        """bonk @user"""
        chosen = await self.get_hugged("nohorny")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} bonks <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} bonks {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="THWACK", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Punch
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def punch(self, ctx, user: discord.User):
        """punch @user"""
        chosen = await self.get_hugged("punch")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} punches <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} punches {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="THWACK", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Slaps
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def slap(self, ctx, user: discord.User):
        """slap @user"""
        chosen = await self.get_hugged("slap")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} slaps <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} slaps {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="SLAP!", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Noms
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def nom(self, ctx, user: discord.User):
        """noms on @user"""
        chosen = await self.get_hugged("nom")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} noms <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} noms {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="NOM!", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Kill
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def kill(self, ctx, user: discord.User):
        """kills @user"""
        
        chosen = await self.get_hugged("kill")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} kills <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} kills {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="RIP", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Resurrection
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def revive(self, ctx, user: discord.User):
        """revives @user"""
        hug_choice = "https://media.tenor.com/SuADVxKkQ-AAAAAC/frankenstein-its-alive.gif"
        message = [f"{ctx.author.display_name} revives <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} revives {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="THEY LIVE", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)

    # Headbutt
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def headbutt(self, ctx, user: discord.User):
        """headbutt @user"""
        
        chosen = await self.get_hugged("headbutt")
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} headbutts <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} headbutts {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="THWACK", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>", embed=embed_var)


    @commands.hybrid_command()
    async def violent_gifs(self, ctx):
        actions = await self.action_count()
        des = "\n".join(f"""***`{name:<15}`***| {'*' + str(gif_count):>3}*""" for name, gif_count in actions)
        gif_sum = sum(gif_count for _, gif_count in actions)
        des += f"""\n`-------------------`\n**__`Total         | {gif_sum}`__**"""
        embed_var = Embed(title="**__Action | Count__**", description=des)
        await ctx.reply(embed=embed_var)



async def setup(client):
    await client.add_cog(Violence(client))
