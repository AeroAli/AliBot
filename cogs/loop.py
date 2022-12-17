# cogs / loop.py
import time
from discord.ext import commands
from discord import Embed
import os
from os import listdir
from os.path import join
import json
import csv


class Loop(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command()
    #@commands.cooldown(1, 10, commands.BucketType.user)
    async def loop(self, ctx):
        if ctx.author.id == 689522335119966258 and ctx.guild.id == 1039953198359781446:
            await ctx.reply("Loop Start")
            # for file in listdir("starkids"):
            # for file in listdir("gifs"):
            file = "gifs/hug"
            await ctx.reply(f"file: {file.split('.')[0]}")
            # file = join("gifs", file)
            for line in open(f"{file}").read().splitlines():
                # line in open(f"{file}").read().splitlines():
                if line != "":
                    try:
                        # await ctx.reply(str(file).split("/")[-1].split(".")[0])
                        embed_var = Embed(title=f"gif {line}")
                        embed_var.set_image(url=line)
                        await ctx.reply(embed=embed_var)
                        time.sleep(0.1)
                    except Exception as e:
                        print("er",line)
                        print(e)
                        await ctx.reply("Source Not Available")
    
    @commands.hybrid_command()
    #@commands.cooldown(1, 10, commands.BucketType.user)
    async def loop_c(self, ctx):
        if ctx.author.id == 689522335119966258 and ctx.guild.id == 1039953198359781446:
            await ctx.reply("Loop Start")
            # for file in listdir("starkids"):
            # for file in listdir("gifs"):
            file = "gifs/hug_cog.csv"
            await ctx.reply(f"file: {file.split('.')[0]}")
            # file = join("gifs", file)
            with open(file, "r") as f:
                lines = csv.reader(f, delimiter=",")
                for line in lines:
                    # line in open(f"{file}").read().splitlines():
                    if line != "":
                        try:
                            # await ctx.reply(str(file).split("/")[-1].split(".")[0])
                            embed_var = Embed(title=f"gif {line[0]}")
                            embed_var.set_image(url=line[2])
                            await ctx.reply(embed=embed_var)
                            time.sleep(0.1)
                        except Exception as e:
                            print("er",line)
                            print(e)
                            await ctx.reply("Source Not Available")
    
    @commands.hybrid_command()
    async def f_loop(self, ctx):
        try:
            if ctx.author.id == 689522335119966258 and ctx.guild.id == 1039953198359781446:
                await ctx.reply("Loop Start")
                with open("test/hugbox.csv","r") as file:
                    csvFile = csv.DictReader(file, delimiter=",")
                    for row in csvFile:
                        try:
                            embed_var=Embed(title=row["category_name"], description=row["id"])
                            embed_var.set_image(url=row["image_url"])
                            time.sleep(0.1)
                            await ctx.send(embed=embed_var)
                        except Exception as e:
                            print(row["id"])
                            print(e)
        except Exception as E:
            print(E)


    
    @commands.hybrid_command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def loop_j(self, ctx, show: str):
        try:
            show = show.lower()
            show = show.strip()
            if " " in show:
                show = show.replace(" ", "_")
            if ctx.author.id == 689522335119966258 and ctx.guild.id == 1039953198359781446:
                await ctx.reply("Loop Start")
                # for file in listdir("starkids"):
                # for file in listdir("gifs"):
                file = f"starkids/{show}.json"
                await ctx.reply(f"file: {file.split('.')[0]}")
                with open(f"starkids/{show}.json", "r") as f:
                    data = json.load(f)
                    for ran in data:
                        gif = ran["gif"]
                        quote = ran["quote"]
                        print(gif)
                        print(quote)
                        try:
                            if "\\n" in quote:
                                print("n")
                                quote = str(quote).replace("\\n", "\n")
                            if len(quote) >= 255:
                                var_title = "<200b>"
                                var_description = quote
                            else:
                                var_title = quote
                                var_description = None
                            embed_var = Embed(title=var_title,description=var_description)
                            if gif != "<200b>":
                                embed_var.set_image(url=gif)
                            else:
                                continue
                            time.sleep(1)
                            await ctx.reply(embed=embed_var)
                        except Exception as e:
                            print(e)
        except Exception as E:
            print(E)



async def setup(client):
    await client.add_cog(Loop(client))
