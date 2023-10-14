# cogs / harassment.py
import traceback
from utils import checks
from discord import Embed
from discord.ext import commands, tasks


class Harassment(commands.Cog):
    """template cogs"""
    def __init__(self, client):
        self.client = client
        self.harassing_time.start()

    def cog_unload(self):
        self.harassing_time.cancel()

    async def cog_command_error(self, ctx, error: Exception) -> None:
        traceback.print_exception(error)

    harassing_table = "harassing_cog"


    async def get_harassed(self):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT user, message FROM `{self.harassing_table}`")
                # print(cur.description)
                result = await cur.fetchall()
                print(result)
                return result


    @commands.Cog.listener()
    async def on_message(self, message):
        """egocentric on_message"""
        if "ALI IS THE GREATEST".lower() in message.content.lower():
            emoji = self.client.get_emoji(1036757258006167703)
            await message.add_reaction(emoji)


    @tasks.loop(hours=48)
    async def harassing_time(self):
        for result in await self.get_harassed():
            user = int(result[0])
            message = str(result[1])
            user = await self.client.fetch_user(user)
            print(user, message)
            await user.send(f"{message}")


    @commands.hybrid_command()
    @checks.is_owner()
    @checks.in_test_guild()
    async def add_victims(self, ctx, user, message):
        # insert_query = """
        #   Insert into harassing_cog (user, message)
        #   VALUES (%s, %s)
        #   on duplicate key update message=%s
        # """
        cols = ("user", "message")
        values = [user, message, message]
        # await self.client.execute_query(insert_query, values)
        await self.client.insert_command("harassing_cog",cols, values,[message])
        embed_var = Embed(description="Updated `harassing_cog`")

        await ctx.reply(embed=embed_var)


    @commands.hybrid_command()
    @checks.is_owner()
    @checks.in_test_guild()
    async def remove_victims(self, ctx, user):
        insert_query = """
          DELETE from harassing_cog WHERE user=%s
        """
        values = [user]
        await self.client.execute_query(insert_query, values)
        embed_var = Embed(description="Updated `harassing_cog`")

        await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Harassment(client))
