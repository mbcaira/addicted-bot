import json
import os

import requests as req


user_info = {
    "P3DRO": os.environ.get('P3DRO'),
    "snib2r": os.environ.get('snib2r')
}


def get_game_activity():
    games_played = []
    for user in user_info:
        res = req.get(user_info.get(user))
        games_played.append(json.loads(res.content)["totalGames"])
    return games_played
