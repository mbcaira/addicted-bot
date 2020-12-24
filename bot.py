# bot.py

import asyncio
import os
from datetime import datetime

import discord

from activity_check import get_game_activity

DISCORD_AUTH = os.environ.get('DISCORD_TOKEN')
DISCORD_SERVER = os.environ.get('SERVER_NAME')
CHANNEL = os.environ.get('GENERAL')

START_DATE = datetime(2021, 1, 15)  # January 15th, 2021
END_DATE = datetime(2021, 5, 1)  # May 1st, 2021

client = discord.Client()


def valid_timeframe():
    return START_DATE <= datetime.now() <= END_DATE


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"{client.user} is connected to the following server:\n{guild.name}(id: {guild.id})")
    general = client.get_channel(int(CHANNEL))

    while True:
        if valid_timeframe():
            print("Grabbing initial data...")
            game_activity = get_game_activity()
            print("\nSTARTING GAME TRACKER")
            while valid_timeframe():
                print("Checking for game activity...")
                if game_activity != get_game_activity():
                    await general.send("PEDRO IS ADDICTED AND HAS PLAYED LEAGUE AS OF NOW AND OWES SERUNDER, "
                                       "INFUSIONAL, AND SUBARU $100 LUL")
                    print("Game has been played, shutting down.")
                    exit(0)
                print("Waiting 1 minute...")
                await asyncio.sleep(60)
        else:
            sleep_time = START_DATE - datetime.today()
            print("Not within timeframe, bot will be inactive for {} days, will begin monitoring then..."
                  .format(sleep_time.days))
            await asyncio.sleep(sleep_time.total_seconds())


if __name__ == "__main__":
    client.run(DISCORD_AUTH)
