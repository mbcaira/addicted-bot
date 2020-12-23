# bot.py

import asyncio
import os
from datetime import date

import discord

import activity_check

DISCORD_AUTH = os.environ.get('DISCORD_TOKEN')
DISCORD_SERVER = os.environ.get('SERVER_NAME')
CHANNEL = os.environ.get('GENERAL')

START_DATE = date(2021, 1, 15)  # January 15th, 2021
END_DATE = date(2021, 5, 1)  # May 1st, 2021

client = discord.Client()

print("Grabbing initial data...")
game_activity = activity_check.get_game_activity()
print("\n\n\nSTARTING GAME TRACKER")


def game_played():
    return not activity_check.get_game_activity() == game_activity


def valid_timeframe():
    return START_DATE <= date.today() <= END_DATE


@client.event
async def on_ready():
    for guild in client.guilds:
        print(f"{client.user} is connected to the following server:\n{guild.name}(id: {guild.id})")
    general = client.get_channel(int(CHANNEL))

    while True:
        while valid_timeframe():
            print("Checking for game activity...")
            if game_played():
                await general.send("PEDRO IS ADDICTED AND HAS PLAYED LEAGUE AS OF NOW AND OWES SERUNDER, "
                                   "INFUSIONAL, AND SUBARU $100 LUL")
                print("Game has been played, shutting down.")
                exit(0)
            print("Waiting 1 minute...")
            await asyncio.sleep(60)
        print("Not within timeframe, bot will be inactive for {} days...".format((START_DATE-date.today()).days))
        await asyncio.sleep(60)


if __name__ == "__main__":
    client.run(DISCORD_AUTH)
