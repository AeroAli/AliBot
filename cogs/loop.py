# cogs / loop.py

from discord.ext import commands


class Loop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def loop(self, ctx):
        await ctx.reply("Loop Start")
        # for file in listdir("starkids"):
        file = "hugs"
        for line in open(f"{file}").read().splitlines():
            if line != "":
                try:
                    # await ctx.reply(file)
                    await ctx.reply(line)
                except Exception:
                    print("er",line)
                    await ctx.reply("Source Not Available")


async def setup(client):
    await client.add_cog(Loop(client))
