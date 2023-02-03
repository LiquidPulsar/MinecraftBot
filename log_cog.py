from consts import *
from random import choice
from admin_cog import execute
from os import getenv
from disnake.ext import tasks, commands

def connected(fun):
    async def wrapped(self:"Logger", *args, **kwargs):
        if self.is_connected():
            return await fun(self, *args, **kwargs)
    return wrapped

class Logger(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.index = 0
        self.latest = None
        self.reader.start()

    def cog_unload(self):
        self.reader.cancel()

    @tasks.loop(seconds=6.0) #60.0
    @connected
    async def reader(self):
        with open(Consts.HOME/"logs"/"latest.log") as f:
            if self.latest is not None:
                for line in f:
                    if line == self.latest: break
            new = [*f]

        if not new: return
        loguru.logger.debug(f"Found {len(new)} new lines, parsing")

        self.latest = new[-1]
        for line in new:
            await self.process_line(line)
    
    async def process_line(self, line: str):
        match = re.search(r"\[(\d+:\d+:\d+)\] \[([^\]]+)\]: (.*)", line)
        if match is None:
            loguru.logger.warning(f"Failed to parse line: {line}")
            return
        time, typ, msg = match.groups()
        await self.parse_line(time, typ, msg)
    
    @connected
    async def parse_line(self, time: str, typ: str, msg: str):
        words = msg.split()
        if typ == "Server thread/INFO": #sourcery skip
            if words[0] in Consts.NAMES:
                if words[1] not in Consts.OTHER_MSG:
                    target = self.bot.get_user(Consts.NAMES[words[0]])
                    diss = choice(Consts.DISSES+Consts.CONSTS["specific"].get())
                    await self.callout(
                        f"{target.mention} {' '.join(words[1:])}\n{diss}"
                    )
                    execute(f'/say {words[0]}: {diss}')

    def is_connected(self):
        return self.bot.get_guild(int(getenv("GUILD_ID"))) is not None
    
    @connected
    async def callout(self,msg):
        await self.bot.get_channel(int(getenv("CALLOUT_CHANNEL"))).send(msg)