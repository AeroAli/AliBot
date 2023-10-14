# cogs / wrestlers.py
import asyncio
import random
import traceback

from discord import Embed
from discord import app_commands
from discord.ext import commands

from utils import checks


class Wrestlers(commands.Cog):
    """Wrestler gifs"""

    def __init__(self, client):
        self.client = client
        self.wrestling_table = "wrestling_cog"

    async def cog_command_error(self, ctx, error: Exception) -> None:
        traceback.print_exception(error)
        if ctx.guild.id == 1039953198359781446:
            error = getattr(error, "original", error)
            await ctx.send(embed=Embed(title=f"{type(error).__name__}", description=f"{error}", colour=0xC70039))

    async def get_wrastler(self, wrastler):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT * FROM `{self.wrestling_table}` where category_name='{wrastler}' ORDER BY RAND() LIMIT 1")
                result = await cur.fetchone()
                return result

    async def get_wrastler_all(self, wrastler):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"SELECT * FROM `{self.wrestling_table}` where category_name='{wrastler}'")
                result = await cur.fetchall()
                return result

    async def get_all_wrastlers(self):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"SELECT * FROM `{self.wrestling_table}`")
                result = await cur.fetchall()
                return result

    async def wrestler_count(self):
        async with self.client.db_pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    f"SELECT category_name, COUNT(*) AS `num` FROM wrestling_cog GROUP BY category_name ORDER BY category_name")
                result = await cur.fetchall()
                return result

    # Rhea
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def queen(self, ctx):
        """Rhea Ripley my beloved"""
        message = ["All hail the queen of the ring", "could snap me like a twig and i'd thank her", "*fans myself*",
                   "*fans myself*\n*a lot*", "could snap me like a twig and i'd thank her *send tweet*",
                   "step on my neck,\n*please*", "she could take me to the towel room and fold me like cheap laundry."]

        chosen = await self.get_wrastler("rhea")
        rhea_choice = chosen[2]
        print(rhea_choice)
        embed_var = Embed(title="Rhea Ripley", description=random.choice(message))
        embed_var.set_image(url=rhea_choice)

        await ctx.reply(embed=embed_var)

    # Alba Fyre
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def fyre(self, ctx):
        """Alba Fyre"""
        message = ["*fans myself*"]

        chosen = await self.get_wrastler("alba_fyre")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Alba Fyre", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Seth Rollins
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def freekin(self, ctx):
        """Seth Rollins"""
        message = ["Seth Freakin Rollins"]
        chosen = await self.get_wrastler("seth_rollins")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Seth Rollins", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Drew  McIntyre
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def claymore(self, ctx):
        """Drew McIntyre"""
        # message = [""]

        chosen = await self.get_wrastler("drew_mcintyre")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Drew McIntyre")  # , description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # brock_lesnar
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def angyboi(self, ctx):
        """Brock Lesnar"""
        emoji = self.client.get_emoji(954431171247370240)
        message = [f"Someone's unhappy  {emoji}"]

        chosen = await self.get_wrastler("brock_lesnar")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Brock Lesnar", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Bray Wyatt
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def wyatt(self, ctx):
        """Bray Wyatt"""
        message = ["Rest in Peace Bray", "Don't stop terrifying us from the afterlife, Bray."]

        chosen = await self.get_wrastler("bray_wyatt")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Bray Wyatt", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # nikki_cross
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def nikki(self, ctx):
        """Nikki Cross"""
        message = ["*fans myself*"]

        chosen = await self.get_wrastler("nikki_cross")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Nikki Cross", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # asuka
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def hime(self, ctx):
        """asuka"""
        message = ["*fans myself*"]

        chosen = await self.get_wrastler("asuka")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Asuka", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # cody_rhodes
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def cody(self, ctx):
        """Cody Rhodes"""
        # message = []

        chosen = await self.get_wrastler("cody_rhodes")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Cody Rhodes")  # , description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # liv_morgan
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def tiny(self, ctx):
        """Liv Morgan my beloved"""
        message = ["*fans myself*"]

        chosen = await self.get_wrastler("liv_morgan")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Liv Morgan", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # damien_priest
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def judgement_day(self, ctx):
        """Judgement Day my beloved"""
        message = ["Holy\nFucking\nShit", "Daaaaaaaaaaaamn"]

        chosen = await self.get_wrastler("judgement")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Judgement Day", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # liv_morgan
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def priest(self, ctx):
        """Damian Priest my beloved"""
        message = ["Holy\nFucking\nShit", "Daaaaaaaaaamn"]
        chosen = await self.get_wrastler("priest")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Damian Priest", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # charlotte_flair
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def charlotte(self, ctx):
        """charlotte flair"""
        message = ["Daaaaamn"]
        chosen = await self.get_wrastler("charlotte")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Charlotte Flair", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # finn_balor_demon
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def demon(self, ctx):
        """The Demon Finn Balor"""
        message = ["Daaaaaaaaamn"]
        chosen = await self.get_wrastler("demon")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="The Demon Finn Bálor", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # judgement_day
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def judgement_day(self, ctx):
        """Judgement Day"""
        message = ["Daaaaaaaaamn"]
        chosen = await self.get_wrastler("judgement")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Judgement Day", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # finn_balor
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def balor(self, ctx):
        """Finn Balor"""
        message = ["Daaaaaaaaamn"]
        chosen = await self.get_wrastler("balor")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Finn Bálor", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Becky_Lynch
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def becky(self, ctx):
        """Becky Lynch"""
        message = ["Daaaaaaaaamn"]
        chosen = await self.get_wrastler("becky")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Becky Lynch", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Sami_Zayn
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def sami(self, ctx):
        """Sami Zayn"""
        message = ["Daaaaaaaaamn"]
        chosen = await self.get_wrastler("sami")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Sami Zayn", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)

    # Sami_Zayn
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def ko(self, ctx):
        """Kevin Owens"""
        message = ["Daaaaaaaaamn"]
        chosen = await self.get_wrastler("ko")
        gif_choice = chosen[2]
        print(gif_choice)
        embed_var = Embed(title="Kevin Owe", description=random.choice(message))
        embed_var.set_image(url=gif_choice)

        await ctx.reply(embed=embed_var)



    @commands.hybrid_command()
    async def wrestlers(self, ctx, names: bool = False):
        """get all wrestling gifs"""
        wrastlers = await self.wrestler_count()
        if not names:
            embed_var = Embed(title="Wrestler", description=f"There are {len(wrastlers)} wrestlers in the bot")
        else:
            des = "\n".join(f"""***`{name:<15}`***| {'*' + str(gif_count):>3}*""" for name, gif_count in wrastlers)
            gif_sum = sum(gif_count for _, gif_count in wrastlers)
            des += f"""\n`-------------------`\n**__`Total         | {gif_sum}`__**"""
            embed_var = Embed(title="**__Wrestler | Count__**", description=des)
        await ctx.reply(embed=embed_var)


    @checks.is_owner()
    @checks.in_test_guild()
    @commands.hybrid_command()
    @app_commands.guilds(1039953198359781446)
    async def print_wrastler(self, ctx, wrastler: str | None = None):
        """returns a series of embeds of the wrestler"""
        if wrastler is not None:
            choices = await self.get_wrastler_all(wrastler)
        else:
            choices = await self.get_all_wrastlers()
        for chosen in choices:
            await asyncio.sleep(0.1)
            (title_var, description_var, gif) = chosen[0], chosen[1], chosen[2]
            print(chosen)
            embed_var = Embed(title=f"{title_var}", description=description_var)
            embed_var.set_image(url=gif)
            await ctx.reply(embed=embed_var)
            await asyncio.sleep(0.1)

        await ctx.reply("Done!")


async def setup(client):
    await client.add_cog(Wrestlers(client))
