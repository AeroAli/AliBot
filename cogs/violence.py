# cogs / violence.py
import csv
import random

import discord
from discord import Embed
from discord.ext import commands


class Violence(commands.Cog):
    """violent commands"""
    def __init__(self, client):
        self.client = client

    imprisoned = [959480822988161095]

    hugging_table = "hug_cog"


    async def get_hugged(self, action):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"SELECT * FROM `{self.hugging_table}` where category_name='{action}' ORDER BY RAND() LIMIT 1")
                # print(cur.description)
                result = await cur.fetchone()
                return result



    # Baka
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def baka(self, ctx, user: discord.User):
        """bakaaaaaaaa @user"""
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
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
        if ctx.author.id in self.imprisoned:
            embed_var = Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await ctx.reply(embed=embed_var)
        else:
            chosen = await self.get_hugged("headbutt")
            hug_choice = chosen[2]
            message = [f"{ctx.author.display_name} headbutts <@{user.id}>",  # author hugs @user3
                       f"{ctx.author.display_name} headbutts {user.display_name}"]  # author hugs user
            print(hug_choice)
            embed_var = Embed(title="THWACK", description=random.choice(message))
            embed_var.set_image(url=hug_choice)

            await ctx.reply(f"<@{user.id}>", embed=embed_var)


async def setup(client):
    await client.add_cog(Violence(client))
