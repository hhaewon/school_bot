import asyncio

import discord
from discord.ext import commands

from utils import get_token

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

TOKEN = get_token()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Login bot: {bot.user}')

bot.run(TOKEN)
