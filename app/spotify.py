import os
import json


def get_song_ids():
    path = '/tmp/song_ids.json'
    with open(path) as f:
        return json.load(f)


def is_song_acceptable(song):
    if not song['id']:
        print('Song ID Not Found')
        return False
    if not song['id'] in get_song_ids():
        return False
    return True
