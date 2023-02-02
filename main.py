from consts import *

import disnake
from disnake.ext.commands import *
from admin_cog import Internal
from log_cog import Logger

client = Bot(command_prefix='!', intents=disnake.Intents(
    guilds=True,
    members=True,
    messages=True,
    message_content=True,
))

####################

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == Consts.GUILD:
            break
    loguru.logger.info(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )




####################
client.add_cog(Internal(client))
client.add_cog(Logger(client))
client.run(Consts.TOKEN)