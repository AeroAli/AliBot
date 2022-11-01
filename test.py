# cogs / test.py
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def test(self, ctx):
        await ctx.reply(f"{ctx.author.mention} is the coolest")


async def setup(client):
    await client.add_cog(Test(client))



import random
from os import listdir
from os.path import isfile, join

# gif = random.choice([x for x in open(
#     f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y) and 'gifs' in y)])}"
# ).read().splitlines()])
# gif = random.choice([x for x in open(
#     f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y) and 'gifs' in y)])}"
# ).read().splitlines()])
# print(gif)

# for i in range(20):
#     print("\nSK")
#     quote = random.choice([x for x in open(
#         f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y)) and 'quotes' in y])}"
#     ).read().splitlines()]).split("\n")[0]
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)
#
#     quote = random.choice([x for x in open(
#         f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y)) and 'quotes' in y])}"
#     ).read().splitlines()])
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)
#
#     quote = random.choice([x for x in open(
#         f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y))])}"
#     ).read().splitlines()])
#     if "\\n" in quote:
#         quote = quote.replace("\\n", "\n")
#     print(quote)
#
# gif = random.choice([x for x in open(
#         f"starkids/{random.choice([y for y in listdir('starkids') if isfile(join('starkids', y) and 'gifs' in y)])}"
# ).read().splitlines()])

gifs = []
quotes = []
for file in listdir("starkids"):
    if isfile(join("starkids", file)):
        if "gif" in file:
            gifs.append(join("starkids", file))
        if "quote" in file:
            quotes.append(join("starkids", file))

with open(random.choice(gifs), "r") as f:
    gif = f.read().splitlines()

with open(random.choice(quotes), "r") as f:
    quote = f.read().splitlines()

print(random.choice(gif))
print(random.choice(quote))

