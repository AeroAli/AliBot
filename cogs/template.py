# cogs / template.py
import traceback
from utils import checks
from discord import Embed
from discord.ext import commands, tasks


class Template(commands.Cog):
    """template cogs"""
    def __init__(self, client):
        self.client = client

    async def cog_command_error(self, ctx, error: Exception) -> None:
        traceback.print_exception(error)

    hugging_table = "hug_cog"

    async def get_hugged(self, action):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT * FROM `{self.hugging_table}` where category_name='{action}' ORDER BY RAND() LIMIT 1")
                # print(cur.description)
                result = await cur.fetchone()
                print(result)
                return result


    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def example(self, ctx):
        """example command and embed"""
        embed_var = Embed(title="​")
        chosen = await self.get_hugged("wave")
        hug_choice = chosen[2]
        embed_var.set_image(url=hug_choice)
        await ctx.reply(f"Hello {ctx.author.mention}", embed=embed_var)


    @commands.Cog.listener()
    async def on_message(self, message):
        """egocentric on_message"""
        if "ALI IS THE GREATEST".lower() in message.content.lower():
            emoji = self.client.get_emoji(1036757258006167703)
            await message.add_reaction(emoji)



async def setup(client):
    await client.add_cog(Template(client))
