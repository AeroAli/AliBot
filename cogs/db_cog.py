# cogs / template.py
import traceback

from discord import Embed, app_commands
from discord.ext import commands

import utils.checks
import utils.db
from utils import checks


class DB_Cog(commands.Cog):
    def __init__(self, client):
        self.hugging_table = "wrestling_cog"
        self.wrestling_table = "hug_cog"
        self.user_table = "user_table"
        self.client = client

    async def cog_check(self, ctx) -> bool:
        original = commands.is_owner().predicate
        db_check = utils.checks.in_test_guild().predicate
        return await original(ctx) and await db_check(ctx)

    async def cog_command_error(self, ctx, error: Exception) -> None:
        traceback.print_exception(error)
        if ctx.guild.id == 1039953198359781446:
            error = getattr(error, "original", error)
            await ctx.send(embed=Embed(title=f"{type(error).__name__}", description=f"{error}", colour=0xC70039))


    # wrestling_table = "wrestling_cog"
    #

    async def user_statuses(self):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT * FROM `user_table`")
                result = await cur.fetchall()
                return result


    async def check_gif(self, wrastler, gif):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT * FROM `{self.wrestling_table}` where category_name='{wrastler}' and image_url='{gif}'")
                result = await cur.fetchall()
                return result

    @app_commands.guilds(1039953198359781446)
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def update_role(self, ctx, role_id, role_name, server_id, allowed):
        # insert_query = """
        # Insert into role_table (role_id, role_name, guild_id, allowed)
        # VALUES (%s, %s, %s, %s)
        # on duplicate key update allowed=%s
        # """
        col = ("role_id", "role_name", "guild_id", "allowed")
        values = [role_id, role_name, server_id, allowed, allowed]
        # await self.client.execute_query(insert_query, values)
        await self.client.insert_command("role_table", col, values, [allowed])
        embed_var = Embed(description="Updated `user_table`")

        await ctx.reply(embed=embed_var)


    @app_commands.guilds(1039953198359781446)
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def update_server(self, ctx, server_id, server_name):
        # insert_query = """
        # Insert into guild_table (guild_id, guild_name)
        # VALUES (%s, %s) 
        # """
        col = ("guild_id", "guild_name")
        values = [server_id, server_name]
        await self.client.insert_command("guild_table", col, values)

        embed_var = Embed(description="Updated `guild_table`")

        await ctx.reply(embed=embed_var)


    @app_commands.guilds(1039953198359781446)
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def update_user_db(self, ctx, user_id, user_name: str, is_babby: int=0, allowed: int=1):
        # insert_query = """
        # Insert into user_table (user_id, user_name, is_babby, allowed)
        # VALUES (%s, %s, %s, %s) 
        # on duplicate key update is_babby=%s, allowed=%s
        # """
        try:
            col = ("user_id", "user_name", "is_babby", "allowed")
            values = [user_id, user_name, is_babby, allowed, is_babby, allowed]
            await self.client.insert_command("user_table", col, values, [is_babby, allowed])

            embed_var = Embed(description="Updated `guild_table`")
            await ctx.reply(embed=embed_var)

        except Exception as E:
            await ctx.send(embed=Embed(title=f"Error", description=f"{E}", colour=0xC70039))



    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def user_status(self, ctx):
        results = await self.user_statuses()
        embed_var = Embed(title="**__User Status__**",
                          description="\n".join(f"<@{int(user)}> | {'Baby' if bool(baby) else 'Adult'} | {'Banned' if not bool(allowed) else 'Free'}"
                      for _, user, baby, allowed, _ in results)
        )
        try:
            await ctx.reply(embed=embed_var)
        except Exception as E:
            await ctx.send(embed=Embed(title=f"Error", description=f"{E}", colour=0xC70039))


    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def moar_hugs(self, ctx, action: str, gif: str):
        results = await self.check_gif(action, gif)
        if not results:
            cols = ("category_name", "image_url")
            values = [action, gif]
            await self.client.insert_command(self.hugging_table, cols, values)

            embed_var = Embed(description="Updated `hug_cog`")

            await ctx.reply(embed=embed_var)



    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def moar_wrastler(self, ctx, wrastler: str, gif: str):
        results = await self.check_gif(wrastler, gif)
        if not results:
            cols = ("category_name", "image_url")
            values = [wrastler, gif]
            await self.client.insert_command(self.wrestling_table, cols, values)

            embed_var = Embed(description="Updated `wrestling_cog`")

            await ctx.reply(embed=embed_var)

    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def check_wrastler(self, ctx, wrastler: str, gif: str):
        results = await self.check_gif(wrastler, gif)
        if not results:
            embed_var = Embed(description="gif does not exist")
        else:
            embed_var = Embed(description="gif exist!")
        await ctx.reply(embed=embed_var)


    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def replace_wrastler(self, ctx, wrastler: str, intial_gif: str, replacement_gif: str):
        results = await self.check_gif(wrastler, intial_gif)
        if not results:
            embed_var = Embed(description="gif does not exist, adding")
            await ctx.reply(embed=embed_var)

            cols = ("category_name", "image_url")
            values = [wrastler, replacement_gif]
            await self.client.insert_command(self.wrestling_table,cols, values)
        else:
            embed_var = Embed(description="gif exists, replacing")
            await ctx.reply(embed=embed_var)
            set_dict = {"image_url":replacement_gif}
            where = {"id":results[0]}
            await self.client.replace_command(self.wrestling_table, where, set_dict)
            embed_var = Embed(description="gif added!")
            await ctx.reply(embed=embed_var)

    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def update_category_name(self, ctx, old: str, new: str):
        where = {"category_name":old}
        replace = {"category_name":new}
        await self.client.update_command("wrestling_cog", where, replace)
        await ctx.reply(embed=Embed(title="Update Successful",description=f"changed all instances of *{old}* to *{new}*",colour=0x088F8F))

async def setup(client):
    await client.add_cog(DB_Cog(client))
