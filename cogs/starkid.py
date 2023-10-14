# cogs / starkid.py
import json
import random
import traceback
from os import listdir
from os.path import isfile, join

from discord import Embed
from discord.ext import commands


class Starkid(commands.Cog):
    """starkid commands"""
    def __init__(self, client):
        self.client = client

    ali_approved = [158646501696864256, 689522335119966258, 772210230971858955, 758054996586790974]
    #              [thanos,             ali,                theo,               matt]

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def star_quote(self, ctx, show: str):
        """random quote (and gif) from a starkid show - use /list to view the supported shows"""
        try:
            show = show.lower()
            show = show.strip()
            if " " in show:
                show = show.replace(" ", "_")
            if show != "random":
                with open(f"starkids/{show}.json", "r") as f:
                    data = json.load(f)
                    ran = random.choice(data)
                    gif = ran["gif"]
                    quote = ran["quote"]
                    if "\\n" in quote:
                        quote = str(quote).replace("\\n", "\n")
                    
                    if len(quote) >= 255:
                        var_title = "​"
                        var_description = quote
                    else:
                        var_title = quote
                        var_description = None
                    embed_var = Embed(title=var_title,description=var_description)
                    if gif != "​":
                        embed_var.set_image(url=gif)
                    await ctx.reply(embed=embed_var)
                    # print(gif)
            else:
                file = random.choice([y for y in listdir('starkids') if isfile(join('starkids', y))])
                with open(f"starkids/{file}", "r") as f:
                    data = json.load(f)
                    ran = random.choice(data)
                    gif = ran["gif"]
                    quote = ran["quote"]
                    if "\\n" in quote:
                        quote = str(quote).replace("\\n", "\n")
                    if len(quote) >= 255:
                        var_title = "​"
                        var_description = quote
                    else:
                        var_title = quote
                        var_description = None
                    embed_var = Embed(title=var_title,description=var_description)
                    if gif == "https://media.tenor.com/fhKONBs-ln4AAAAd/honor-to-honor.gif" and ctx.author.id not in self.ali_approved or ctx.guild.id == 801834790768082944:
                        gif = "https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif"
                    if gif == "​":
                        gif = "https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif"
                    embed_var.set_image(url=gif)
                    await ctx.reply(embed=embed_var)
        except Exception as e:
            traceback.print_exception(e)
            await ctx.reply("Source Not Available")

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def star_gif(self, ctx, show: str):
        """random gif and quote from a starkid show - use /list to view the supported shows"""
        try:
            show = show.lower()
            show = show.strip()
            if " " in show:
                show = show.replace(" ", "_")
            if show != "random":
                with open(f"starkids/{show}.json", "r") as f:
                    data = json.load(f)
                    ran = random.choice(data)
                    gif = ran["gif"]
                    quote = ran["quote"]
                    if "\\n" in quote:
                        quote = str(quote).replace("\\n", "\n")
                    if len(quote) >= 255:
                        var_title = "​"
                        var_description = quote
                    else:
                        var_title = quote
                        var_description = None
                    embed_var = Embed(title=var_title,description=var_description)
                    if gif == "​":
                        gif = "https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif"
                    embed_var.set_image(url=gif)
                    await ctx.reply(embed=embed_var)
                    # print(gif)
            else:
                file = random.choice([y for y in listdir('starkids') if isfile(join('starkids', y))])
                with open(f"starkids/{file}", "r") as f:
                    data = json.load(f)
                    ran = random.choice(data)
                    gif = ran["gif"]
                    quote = ran["quote"]
                    if "\\n" in quote:
                        quote = str(quote).replace("\\n", "\n")
                    #embed_var = Embed(title=quote)

                    if len(quote) >= 255:
                        var_title = "​"
                        var_description = quote
                    else:
                        var_title = quote
                        var_description = None
                    embed_var = Embed(title=var_title,description=var_description)
                    if gif == "https://media.tenor.com/fhKONBs-ln4AAAAd/honor-to-honor.gif" and ctx.author.id not in self.ali_approved or ctx.guild.id == 801834790768082944:
                        gif = "https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif"
                    if gif == "​":
                        gif = "https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif"
                    embed_var.set_image(url=gif)
                    await ctx.reply(embed=embed_var)
            # await ctx.reply(gif)
        except Exception as e:
            traceback.print_exception(e)
            await ctx.reply("Source Not Available")

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def star_random(self, ctx):
        """random gif and/or quote from a starkid show - use /list to view the supported shows"""
        try:
            print("under try")
            file = random.choice([y for y in listdir('starkids') if isfile(join('starkids', y))])
            with open(f"starkids/{file}", "r") as f:
                data = json.load(f)
                ran = random.choice(data)
                gif = ran["gif"]
                quote = ran["quote"]
                if "\\n" in quote:
                    quote = str(quote).replace("\\n", "\n")
                #embed_var = Embed(title=quote)

                if len(quote) >= 255:
                    var_title = "​"
                    var_description = quote
                else:
                    var_title = quote
                    var_description = None
                embed_var = Embed(title=var_title,description=var_description)
                if gif == "https://media.tenor.com/fhKONBs-ln4AAAAd/honor-to-honor.gif" and ctx.author.id not in self.ali_approved or ctx.guild.id == 801834790768082944:
                    gif = "https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif"
                if gif == "​":
                    gif = "https://media.tenor.com/RHqI2d3jobsAAAAC/tgwdlm-lauren-lopez.gif"
                embed_var.set_image(url=gif)
                await ctx.reply(embed=embed_var)
        except Exception as e:
            traceback.print_exception(e)
            await ctx.reply("Source Not Available")

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def star_thanos(self, ctx):
        """blame thanos - basically star_random but sometimes blames him"""
        if ctx.author.id in self.ali_approved:# and ctx.guild.id != 801834790768082944:
            try:
                print("try")
                file = random.choice([y for y in listdir('starkids') if isfile(join('starkids', y)) and "thanos" in y])
                print(file)
                with open(f"starkids/{file}", "r") as f:
                    data = json.load(f)
                    ran = random.choice(data)
                    gif = ran["gif"]
                    quote = ran["quote"]

                    if "\\n" in quote:
                        quote = str(quote).replace("\\n", "\n")
                    #embed_var = Embed(title=quote)
                    if len(quote) >= 255:
                        var_title = "​"
                        var_description = quote
                    else:
                        var_title = quote
                        var_description = None
                    embed_var = Embed(title=var_title,description=var_description)
                    if gif != "​":
                        embed_var.set_image(url=gif)


                    try:
                        print(ran["author"])
                        author = await self.client.fetch_user(ran["author"])
                        embed_var.set_author(name=author, icon_url=author.avatar.url)
                    except Exception as e:
                        traceback.print_exception(e)
                    await ctx.reply(embed=embed_var)
                    print(gif, quote)
            except Exception as e:
                traceback.print_exception(e)
                await ctx.reply("Source Not Available")

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def disapproval(self, ctx):
        """When you need to express your disapproval"""
        gif = "https://media.tenor.com/mUNcGoiwOLcAAAAM/brian-holden-starkid.gif"
        quote = "Brian does not approve"
        
        embed_var = Embed(title=quote)
        embed_var.set_image(url=gif)
        
        await ctx.reply(embed=embed_var)

    @commands.hybrid_command()
    async def list(self, ctx):
        """Lists shows"""
        command_description = "\n\n***Input is case-insensitive***\n\n" \
                              "A Very Potter Musical Trilogy - `avpm`\n" \
                              "Starship - `starship`\n" \
                              "Holy Musical B@man! - `hmb`\n" \
                              "Twisted: The Untold Story of a Royal Vizier - `twisted`\n" \
                              "The Trail To Oregon! - `oregon`\n" \
                              "Ani: A Parody - `ani`\n" \
                              "Firebringer - `firebringer`\n" \
                              "Assorted Hatchetfield - `hatchetfield`\n" \
                              "The Guy Who Doesn't Like Musicals - `tgwdlm`\n" \
                              "Black Friday - `black friday`"

        embed_var = Embed(
            color=0x1A2B3C,
            title="__Show - `command input`__",
            description=command_description
        )
        await ctx.reply(embed=embed_var)


async def setup(client):
    await client.add_cog(Starkid(client))

