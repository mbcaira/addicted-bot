import os
import discord
import activity_check
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DISCORD_AUTH = os.getenv('DISCORD_TOKEN')
DISCORD_SERVER = os.getenv('SERVER_NAME')
CHANNEL = os.getenv('GENERAL')

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})")
    general = client.get_channel(int(CHANNEL))
    await general.send("a d d i c t e d")

client.run(DISCORD_AUTH)
