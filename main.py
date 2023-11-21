# main.py
import asyncio
import sys
import traceback
from os import getenv, listdir
from os.path import abspath, dirname

import aiomysql
import discord
from aiohttp import ClientSession
from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

import utils.errors

load_dotenv()
token = getenv("TOKEN")
db_pwd = getenv("DB_PWD")
db_user = getenv("DB_USER")
db_host = getenv("DB_HOST")
db_port = getenv("DB_PORT")
db = getenv("DB")
er_wh = getenv("ER_WEBHOOK")
vc_wh = getenv("EVENT_WEBHOOK")
mes_wh = getenv("MESSAGE_WEBHOOK")


class Client(commands.Bot):
    def __init__(self, db_pool: aiomysql.Pool, web_client: ClientSession, ):

        super().__init__(command_prefix=commands.when_mentioned_or("&"), intents=discord.Intents.all(),
            help_command=commands.DefaultHelpCommand(dm_help=True)

        )
        self.db_pool = db_pool
        self.web_client = web_client
        self.error_webhook = discord.Webhook.from_url(url=er_wh, session=self.web_client, client=self)
        self.event_webhook = discord.Webhook.from_url(url=vc_wh, session=self.web_client, client=self)
        self.message_webhook = discord.Webhook.from_url(url=mes_wh, session=self.web_client, client=self)

    async def setup_hook(self):  # overwriting a handler
        print(f"\033[31mLogged in as {self.user}\033[39m")
        cogs_folder = f"{abspath(dirname(__file__))}/cogs"
        for filename in listdir(cogs_folder):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        await self.tree.sync()
        print("Loaded cogs")

    async def on_command_error(self, context, exception, /, *args: object, **kwargs: object) -> None:
        # print(self.error_webhook)
        # channel = self.get_channel(1156653571522174987)
        error = getattr(exception, "original", exception)
        time = discord.utils.utcnow()
        embed_var = (
            Embed(title=f"Command: {context.command} Failure", description=f"**{type(error).__name__}**```{error}```", colour=0xC70039, timestamp=time)
            .add_field(name="Server", value=f"{context.guild.name}", inline=True)
            .add_field(name="​", value="​", inline=True)
            .add_field(name="Channel", value=f"{context.channel.name}", inline=True)
            .set_author(name=context.author, icon_url=context.author.avatar.url)
        )
        if args:
            embed_var.add_field(
                name="Args",
                value="```py\n" + "\n".join(f"{i}: {arg!r}" for i, arg in enumerate(args)) + "\n```",
                inline=False,
            )
        if kwargs:
            embed_var.add_field(
                name="Kwargs",
                value="```py\n" + "\n".join(f"{name}: {kwarg!r}" for name, kwarg in kwargs.items()) + "\n```",
                inline=False,
            )
        await self.error_webhook.send(embed=embed_var)
        if isinstance(exception, utils.errors.BadRole):
            await context.send(str(exception.args[0]))
            return
        if isinstance(exception, utils.errors.UserIsBlocked):
            await context.send(str(exception.args[0]))
            return
        if isinstance(exception, utils.errors.BabbyProofing):
            embed_var = discord.Embed(title="You're on timeout")
            embed_var.set_image(url="https://media.tenor.com/e_9c6yedKCQAAAAd/cat-kitten.gif")
            await context.reply(embed=embed_var)
            return
        traceback.print_exception(exception)


    async def on_error(self, event_method: str, /, *args: object, **kwargs: object) -> None:
        exc_type, exception, tb = sys.exc_info()
        tb_text = "".join(traceback.format_exception(exc_type, exception, tb, chain=False))
        embed_var = discord.Embed(
            title="Event Error",
            description=f"```py\n{tb_text}\n```",
            colour=discord.Colour.dark_gold(),
            timestamp=discord.utils.utcnow(),
        ).add_field(name="Event", value=event_method, inline=False)
        if args:
            embed_var.add_field(
                name="Args",
                value="```py\n" + "\n".join(f"{i}: {arg!r}" for i, arg in enumerate(args)) + "\n```",
                inline=False,
            )
        if kwargs:
            embed_var.add_field(
                name="Kwargs",
                value="```py\n" + "\n".join(f"{name}: {kwarg!r}" for name, kwarg in kwargs.items()) + "\n```",
                inline=False,
            )
        await self.error_webhook.send(embed=embed_var)
        traceback.print_exception(exception)

    async def execute_query(self, query: str, values: list):
        try:
            async with self.db_pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query, values)
                # await conn.commit()
                print("query executed")
        except Exception as e1:
            traceback.print_exception(e1)


    async def insert_command(self, table: str, columns: tuple, values:list, updates: list | None = None):
        """
        command to generate and execute insert queries

        Parameters
        ----------
        table : :class:`str`
            the table that data is being inserted into
        columns : :class:`tuple`
            the columns that the data is being inserted into
        values : :class:`list`
            the data that is being inserted into the table
        updates : :class:`list`
            the columns that are updated on duplicate
        """
        value_s = ", ".join("%s" for _ in columns)
        insert_query = f"""Insert into `{table}` {columns}
                           VALUES ({value_s})
                        """
        if updates:
            up_s = ", ".join(f"{u}=%s" for u in updates)
            insert_query += f"""on duplicate key update {up_s}"""
        print(f"{insert_query!r}")
        await self.execute_query(insert_query, values)




    async def update_command(self, table: str, where: dict, replace: dict):
        """
        command to generate and execute insert queries

        Parameters
        ----------
        table : :class:`str`
            the table that data is being inserted into
        where : :class: dict
            dict containing column and value of the `where` clause
        replace : :class: dict
            dict containing column and value of the `set` clause
        """
        where_cols = ", ".join(f"`{u}`=%s" for u in where.keys())
        replace_cols = ", ".join(f"`{u}`=%s" for u in replace.keys())
        values = list(replace.values()) + list(where.values())
        update_query = f"""UPDATE `{table}`
                           SET {replace_cols}
                           WHERE {where_cols}
                        """
        await self.execute_query(update_query, values)


async def main():
    async with ClientSession() as our_client, aiomysql.create_pool(host=db_host, port=int(db_port), user=db_user,
                                                                   password=db_pwd, db=db, autocommit=True) as pool:
        client = Client(web_client=our_client, db_pool=pool)
        await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())
