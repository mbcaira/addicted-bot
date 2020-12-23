# bot.py

import asyncio
import os

import discord
from dotenv import load_dotenv

import activity_check

load_dotenv()

DISCORD_AUTH = os.getenv('DISCORD_TOKEN')
DISCORD_SERVER = os.getenv('SERVER_NAME')
CHANNEL = os.getenv('GENERAL')

client = discord.Client()

game_activity = activity_check.get_game_activity()


def game_played():
    return not activity_check.get_game_activity() == game_activity


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})")
    general = client.get_channel(int(CHANNEL))
    while True:
        if game_played():
            await general.send("PEDRO IS ADDICTED AND HAS PLAYED LEAGUE AS OF NOW AND OWES SERUNDER, "
                               "INFUSIONAL, AND SUBARU $100 LUL")
        await asyncio.sleep(300)


client.run(DISCORD_AUTH)