# cogs / hugs.py
import random
import csv

import discord
from discord import Embed
from discord.ext import commands


class Hug(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    with open("gifs/hug_cog.csv", "r") as f:
        # rows = csv.DictReader(f)
        csv_rows = csv.reader(f, delimiter=",")
        rows = list(csv_rows)
        # print(type(rows))
        bakas = [row for row in rows if row[1] == 'baka']
        bites = [row for row in rows if row[1] == 'bite']
        boops = [row for row in rows if row[1] == 'boop']
        cuddles = [row for row in rows if row[1] == 'cuddle']
        hugs = [row for row in rows if row[1] == 'hug']
        kills = [row for row in rows if row[1] == 'kill']
        kicks = [row for row in rows if row[1] == 'kick']
        kisses = [row for row in rows if row[1] == 'kiss']
        nohornys = [row for row in rows if row[1] == 'nohorny']
        pats = [row for row in rows if row[1] == 'pat']
        punches = [row for row in rows if row[1] == 'punch']
        scritch = [row for row in rows if row[1] == 'scritch']
        slaps = [row for row in rows if row[1] == 'slap']
        noms = [row for row in rows if row[1] == 'nom' or row[1] == "bite"]
        tackles = [row for row in rows if row[1] == 'tackle']
        squishes = [row for row in rows if row[1] == 'squish']
        favs = [row for row in rows if row[1] == 'favs']
        rhea = [row for row in rows if row[1] == 'rhea']    
        dodies = [row for row in rows if row[1] == 'dodie']    
        headbutts = [row for row in rows if row[1] == 'headbutt']    
    

    
    # Cuddle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick_t(self, ctx, user: discord.User):
        chosen = random.choice(self.kicks)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} kicks <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} kicks {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="KICK",description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    # Cuddle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def bonk(self, ctx, user: discord.User):
        chosen = random.choice(self.nohornys)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} bonks <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} bonks {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="THWACK",description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)
   

    # Cuddle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def punch(self, ctx, user: discord.User):
        chosen = random.choice(self.punches)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} punches <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} punches {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="THWACK",description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)


    # Cuddle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def boop(self, ctx, user: discord.User):
        chosen = random.choice(self.boops)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} boops <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} boops {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="BOOPS",description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    # Cuddle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def cuddle(self, ctx, user: discord.User):
        chosen = random.choice(self.cuddles)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} cuddles <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} cuddles {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="CUDDLES",description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    # Hug
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, user: discord.User):
        chosen = random.choice(self.hugs)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} hugs <@{user.id}>",  # author hugs @user
                   f"{ctx.author.display_name} hugs {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="HUGS",description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    # Tackle
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def tackle(self, ctx, user: discord.User):
        chosen = random.choice(self.tackles)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} tackles <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} tackles {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="TACKLE TIME", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    @commands.Cog.listener()
    async def on_message(self, message):
        if "hugbot" in message.content.lower() and "love" in message.content.lower():
            # https://cdn.discordapp.com/emojis/1036757258006167703.gif?size=96&quality=lossless
            emoji = self.client.get_emoji(1036757258006167703)
            await message.add_reaction(emoji)

     
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def scritches(self, ctx, user: discord.User):
        chosen = random.choice(self.scritch)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} scritches <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} scritches {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="SCRITCHES", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)


     
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def pats(self, ctx, user: discord.User):
        chosen = random.choice(self.pats)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} pats <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} pats {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="*PATS*", description=random.choice(message))
        embed_var.set_image(url=hug_choice)

        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def squish(self, ctx, user: discord.User):
        chosen = random.choice(self.squishes)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} squishes <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} squishes {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="SQUISH", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(f"<@{user.id}>",embed=embed_var)
 
    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def fav(self, ctx, user: discord.User):
        chosen = random.choice(self.favs)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} attacks (affectionate) <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} attacks (affectionate) {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="HUG!!!!!!", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(f"<@{user.id}>",embed=embed_var)


    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def slap(self, ctx, user: discord.User):
        chosen = random.choice(self.slaps)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} slaps <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} slaps {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="SLAP!", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(f"<@{user.id}>",embed=embed_var)


    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def nom(self, ctx, user: discord.User):
        chosen = random.choice(self.noms)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} noms <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} noms {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="NOM!", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def kill(self, ctx, user: discord.User):
        chosen = random.choice(self.kills)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} kills <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} kills {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="RIP", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def revive(self, ctx, user: discord.User):
        hug_choice = "https://media.tenor.com/SuADVxKkQ-AAAAAC/frankenstein-its-alive.gif" 
        message = [f"{ctx.author.display_name} revives <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} revives {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="THEY LIVE", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def headbutt(self, ctx, user: discord.User):
        chosen = random.choice(self.headbutts)
        hug_choice = chosen[2]
        message = [f"{ctx.author.display_name} headbutts <@{user.id}>",  # author hugs @user3
                   f"{ctx.author.display_name} headbutts {user.display_name}"]  # author hugs user
        print(hug_choice)
        embed_var = Embed(title="THWACK", description=random.choice(message))
        embed_var.set_image(url=hug_choice)
        
        await ctx.reply(f"<@{user.id}>",embed=embed_var)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def queen(self, ctx):
        message = ["All hail the queen of the ring",  # author hugs @user3
                   "could snap me like a twig and i'd thank her",
                   "*fans myself*",
                   "step on my neck, *please*"]  # author hugs user
        
        chosen = random.choice(self.rhea)
        rhea_choice = chosen[2]
        print(rhea_choice)
        embed_var = Embed(title="Rhea Ripley",description=random.choice(message))
        embed_var.set_image(url=rhea_choice)
        
        await ctx.reply(embed=embed_var)

    @commands.hybrid_command()
    # @commands.cooldown(1, 10, commands.BucketType.user)
    async def dodie(self, ctx):
        message = ["is it dodie yellow tho"]  # author hugs user
        
        chosen = random.choice(self.dodies)
        rhea_choice = chosen[2]
        print(rhea_choice)
        embed_var = Embed(title="DODIE CLARKE!!!!!",description=random.choice(message))
        embed_var.set_image(url=rhea_choice)
        
        await ctx.reply(embed=embed_var)

    @commands.hybrid_command()
    async def disappoint(self, ctx):
        gif = "https://media.tenor.com/YhrJ_-g-CYMAAAAC/rhea-ripley-annoyed.gif"
        
        quote = "Come on, really?"
        embed_var = Embed(title=quote)
        embed_var.set_image(url=gif)

        await ctx.reply(embed=embed_var)
    # eldritch
    # flirt
    # Pat
    # Glomp
    # MemeHug
    # reaction - Y
    # embed - Y
    # debug?


async def setup(client):
    await client.add_cog(Hug(client))
