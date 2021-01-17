# activity_check.py

import json
import os

import requests as req

USERS = os.environ.get('USERS').split(",")
API_HEADER = json.loads(os.environ.get('API_HEADER'))


def get_account_id():
    account_ids = []
    print("Grabbing account IDs...")
    uri = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    for user in USERS:
        account_id = json.loads(req.get(uri + user, headers=API_HEADER).content)
        try:
            account_ids.append(account_id["accountId"])
        except KeyError:
            print(f'Encountered an error (SUMMONER API): {account_id["status"]["message"]}')
            return get_account_id()
    return account_ids


def get_game_activity():
    track_log = "Tracking users: "
    for user in USERS:
        track_log += user
    print(track_log)
    games_played = []
    uri = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/"
    account_ids = get_account_id()
    print("Grabbing games played...")
    for account in account_ids:
        total_games = json.loads(req.get(uri + account, headers=API_HEADER).content)
        try:
            games_played.append(total_games["totalGames"])
        except KeyError:
            print(f"Encountered an error (MATCH API): {total_games['status']['message']}")
            return get_account_id()
    print("Games played on each account (in order): ", games_played)
    return games_played
