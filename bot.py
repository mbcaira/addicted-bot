import asyncio
import os
from datetime import datetime
from pymongo import MongoClient

import discord

from activity_check import get_game_activity

# Get credentials from environment variables
DISCORD_AUTH = os.environ.get('DISCORD_TOKEN')
DISCORD_SERVER = os.environ.get('SERVER_NAME')
CHANNEL = os.environ.get('GENERAL')
MONGODB_URI = os.environ.get('MONGODB_URI')
WAIT_TIME = int(os.environ.get('WAIT_TIME'))

START_DATE = [int(info) for info in os.environ.get('START_DATE').split("/")]
END_DATE = [int(info) for info in os.environ.get('END_DATE').split("/")]

BEGIN = datetime(START_DATE[2], START_DATE[1], START_DATE[0])
END = datetime(END_DATE[2], END_DATE[1], END_DATE[0])

discord_client = discord.Client()

def valid_timeframe():
    return BEGIN <= datetime.now() <= END

@discord_client.event
async def on_ready():
    try:
        with MongoClient(MONGODB_URI) as mongo_client:
            db = mongo_client['GamesPlayed']['games']
            print("Connected to MongoDB successfully.")
            for guild in discord_client.guilds:
                print(f"{discord_client.user} is connected to the following server:\n{guild.name}(id: {guild.id})")
            general = discord_client.get_channel(int(CHANNEL))
            print(f"Checking for activity between the dates: {START_DATE[0]}/{START_DATE[1]}/{START_DATE[2]} - {END_DATE[0]}/"
                  f"{END_DATE[1]}/{END_DATE[2]}")
          
            while True:
                if valid_timeframe():
                    if db.find_one is None:
                        print("Grabbing initial data...")
                        try:
                            logged_games = get_game_activity()
                            logged_games = {
                                "gamesPlayed": logged_games
                            }
                            insert_status = db.insert_one(logged_games)
                            print(f"Inserted initial games played into database ({insert_status.inserted_id}): {get_game_activity()}")
                            game_activity = logged_games['gamesPlayed']
                        except ConnectionError:
                            print("Could not grab initial data at this moment, trying again...") 
                    else:
                        game_activity = db.find_one()['gamesPlayed']
                    print("\nSTARTING GAME TRACKER")
                    while valid_timeframe():
                        print("Checking for game activity...")
                        try:
                            activity = get_game_activity()
                            if activity != game_activity:
                                await general.send(os.getenv('MESSAGE'))
                                print("A game has been played, shutting down...")
                                exit(0)
                            print(f"Waiting {WAIT_TIME*60} minute(s)")
                        except ConnectionError:
                            print("Connection error while checking game activity, retrying...")
                elif datetime.today() > END:
                    await general.send(os.getenv('SUCCESS'))
                    return
                else:
                    sleep_time = BEGIN - datetime.today()
                    print("Not within timeframe, bot will be inactive for {} days, will begin monitoring then..."
                        .format(sleep_time.days))
                    await asyncio.sleep(sleep_time.total_seconds())
    except:
        print("Error connecting to MongoDB and Discord, please check credentials or connection.")
        exit(1)

if __name__ == "__main__":
    discord_client.run(DISCORD_AUTH)