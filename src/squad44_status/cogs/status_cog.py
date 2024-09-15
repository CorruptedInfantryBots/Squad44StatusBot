import logging
import random
import requests
import discord
from discord.ext import commands, tasks

logger = logging.getLogger("discord:cog:status")

BATTLEMETRICS_API = "https://api.battlemetrics.com/servers/29196421"


    

class StatusCog(commands.Cog):
    STATUS_TEMPLATE = "{players}/100 Players on {map}"
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_status.start()
        self.players:int
        self.players:str
        self.mode:str
    
    def get_status(self):
        resp = requests.get(BATTLEMETRICS_API)
        resp.raise_for_status()
        status = resp.json().get("data", {})
        players = status.get("attributes", {}).get("players", 0)
        map = status.get("attributes", {}).get("details", {}).get("map", "")
        mode = status.get("attributes", {}).get("details", {}).get("gameMode", "")
        return StatusCog.STATUS_TEMPLATE.format(players=players,map=map,mode=mode)

    @tasks.loop(seconds=5.0)
    async def update_status(self):
        logger.info("Update status")
        status = self.get_status()
        logger.info(f"Status {status}")
        await self.bot.change_presence(activity=discord.CustomActivity(name=status))

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()
