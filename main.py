# main.py
import discord
from discord.ext import commands
from os import getenv, listdir
from dotenv import load_dotenv
from os.path import abspath, dirname

load_dotenv()
token = getenv("TOKEN")


class Client(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("&"),
            intents=discord.Intents.all(),
            help_command=commands.DefaultHelpCommand(dm_help=True)
        )

    async def setup_hook(self):  # overwriting a handler
        print(f"\033[31mLogged in as {client.user}\033[39m")
        cogs_folder = f"{abspath(dirname(__file__))}/cogs"
        for filename in listdir(cogs_folder):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
        await client.tree.sync()
        print("Loaded cogs")


client = Client()
client.run(token)
