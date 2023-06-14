# main.py
import asyncio
from os import getenv, listdir
from os.path import abspath, dirname

import aiomysql
import discord
from aiohttp import ClientSession
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = getenv("TOKEN")
db_pwd = getenv("DB_PWD")
db_user = getenv("DB_USER")
db_host = getenv("DB_HOST")
db_port = getenv("DB_PORT")
db = getenv("DB")


class Client(commands.Bot):
    def __init__(
            self,
            db_pool: aiomysql.Pool,
            web_client: ClientSession,
    ):

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=discord.Intents.all(),
            help_command=commands.DefaultHelpCommand(dm_help=True)

        )
        self.db_pool = db_pool
        self.web_client = web_client

    async def setup_hook(self):  # overwriting a handler
        print(f"\033[31mLogged in as {self.user}\033[39m")
        cogs_folder = f"{abspath(dirname(__file__))}/cogs"
        for filename in listdir(cogs_folder):
            if filename.endswith(".py"):
                await self.load_extension(f"cogs.{filename[:-3]}")
        await self.tree.sync()
        print("Loaded cogs")


async def main():
    async with ClientSession() as our_client, aiomysql.create_pool(host=db_host, port=int(db_port),
                                                                   user=db_user, password=db_pwd, db=db, ) as pool:
        client = Client(web_client=our_client, db_pool=pool)
        await client.start(token)


if __name__ == "__main__":
    asyncio.run(main())
