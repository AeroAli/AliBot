#--
#-- Return correct username for discord
#--
def getDiscordUserName(nickname, username):
  if nickname is None:
    return username
  else:
    return nickname


        targetuser = discord.utils.find(lambda u: ((u.nick and targetpseudoname.lower() in u.nick.lower()) or (targetpseudoname.lower() in u.name.lower())), ctx.guild.members)
        targetuserid = targetuser.id
        targetusername = cbl.getDiscordUserName(targetuser.nick, targetuser.name)