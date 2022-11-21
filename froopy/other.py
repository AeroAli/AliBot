from os import getenv

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

description = '''An example bot to showcase the discord.ext.commands extension module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)
token = getenv('TOKEN')


@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))


# Check Messages

# --
# -- Member modification event
# --
@bot.event
async def on_member_update(before, after):
    # -- Get data
    username = after.name
    userid = after.id
    servername = after.guild.name
    # -- Check for server booster role
    checkroles = ['814807473198333952']
    # -- Check first to see if user gained the role
    rolegained = False
    # -- Check to see that before does not have the booster role
    rolecheck = False
    for urole in before.roles:
        if str(urole.id) in checkroles:
            rolecheck = True
            break
    if rolecheck == False:
        # -- Check to see that after does have the booster role
        rolecheck = False
        for urole in after.roles:
            if str(urole.id) in checkroles:
                rolecheck = True
                break
        if rolecheck == True:
            rolegained = True
    # -- Check to see if user lost the role
    rolelost = True
    if rolegained == False:
        # -- Check to see that before does have the booster role
        rolecheck = False
        for urole in before.roles:
            if str(urole.id) in checkroles:
                rolecheck = True
                break
        if rolecheck == True:
            # -- Check to see that after does not have the booster role
            rolecheck = False
            for urole in after.roles:
                if str(urole.id) in checkroles:
                    rolecheck = True
                    break
            if rolecheck == False:
                rolelost = True
    if rolelost == True:
        # -- Role lost sql code goes here
        print("rip")
    elif rolegained == True:
        # -- Role gained sql code goes here
        print("yay")
