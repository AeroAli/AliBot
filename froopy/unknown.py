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

#--
#-- Member modification event
#--
@bot.event
async def on_member_update(before, after):
  #-- Get data
  username = cbl.getDiscordUserName(after.nick, after.name)
  userid = after.id
  serverid = after.guild.id
  servername = after.guild.name
  #-- Check to make sure this is the platinum players guild
  if before.guild.id != 696024547870244915:
    return
  #-- Check for poop roles
  for i in range(0, 2):
    checkroles = []
    checkrolemode = ''
    if i == 0:
      #-- Poop roles
      checkrolemode = 'poop'
      checkroles = ['846747904059506700', '834162206747787314', '946443009409577000']
    elif i == 1:
      #-- Inked role
      checkrolemode = 'inked'
      checkroles = ['976145995941417020']
    #-- Check to see that before does not have the poop role
    rolecheck = False
    for urole in before.roles:
      if str(urole.id) in checkroles:
        rolecheck = True
        break
    if rolecheck == True:
      continue
    #-- Check to see that after does have the poop role
    rolecheck = False
    for urole in after.roles:
      if str(urole.id) in checkroles:
        rolecheck = True
        break
    if rolecheck == False:
      continue
    #-- Get data
    username = cbl.getDiscordUserName(after.nick, after.name)
    userid = after.id
    serverid = after.guild.id
    #-- User was just given the poop role.  Increment their score
    db = mysql.connector.connect(user=botconfig['db_username'], password=botconfig['db_password'], host=botconfig['db_server'], port=botconfig['db_port'], database=botconfig['db_main'])
    dbq = db.cursor()
    dbq.execute("SELECT id FROM poop_rep WHERE discord_server_id = %s AND discord_user_id = %s AND role_mode = %s", (serverid, userid, checkrolemode))
    userdb = dbq.fetchall()
    if len(userdb) == 0:
      dbq.execute("INSERT INTO poop_rep (discord_server_id, discord_user_id, last_user_name, count, role_mode) VALUES (%s, %s, %s, 1, %s)", (serverid, userid, username, checkrolemode))
    else:
      dbq.execute("UPDATE poop_rep SET last_user_name = %s, count = count + 1 WHERE discord_server_id = %s AND discord_user_id = %s AND role_mode = %s", (username, serverid, userid, checkrolemode))
    dbq.close()
    db.commit()
    db.close()