import json
import time
import os
from acrcloud.recognizer import ACRCloudRecognizer
import helpers


def get_song_name_from_result(result):
    """Returns the song name from results"""
    return result['metadata']['music'][0]['external_metadata']['spotify']['track']['name']


def get_spotify_id_from_result(result):
    """Returns the spotify id from results"""
    return result['metadata']['music'][0]['external_metadata']['spotify']['track']['id']


def get_first_artist_from_result(result):
    """Returns the first artist name from results"""
    return result['metadata']['music'][0]['external_metadata']['spotify']['artists'][0]['name']


def get_song_length_milliseconds(result):
    """Returns the length of the song in milliseconds"""
    return int(result['metadata']['music'][0]['duration_ms'])


def get_song_elapsed_milliseconds(result):
    """Returns the length of the song that has ellapsed in milliseconds"""
    return int(result['metadata']['music'][0]['play_offset_ms'])


def get_song_seconds_remaining(result):
    """Returns the seconds of the song remaining"""
    remaining_ms = get_song_length_milliseconds(result) - get_song_elapsed_milliseconds(result)
    return int(remaining_ms / 1000)


def get_song_percent_remaining(result):
    """Returns the percent of the song remaining"""
    return int((1 - (get_song_elapsed_milliseconds(result) / get_song_length_milliseconds(result))) * 100)


def save_fingerprint_result_to_file(result):
    """Saves the result of the fingerprint to a file"""
    file_path = os.path.join(helpers.get_json_output_directory(), str(int(time.time())) + '.json')
    with open(file_path, 'w') as outfile:
        json.dump(result, outfile)


def get_fingerprint():
    """Requests the identification of the song from the ACR module"""
    print('Requesting fingerprint...')
    config = {
        'host': os.environ.get('ACR_HOST'),
        'access_key': os.environ.get('ACR_ACCESS_KEY'), 
        'access_secret': os.environ.get('ACR_ACCESS_SECRET'),
        'timeout': 10
    }
    recognizer = ACRCloudRecognizer(config)
    mp3_path = helpers.get_mp3_output_path()
    start_seconds = 0
    rec_length = helpers.get_recording_length_seconds()
    result = json.loads(recognizer.recognize_by_file(mp3_path, start_seconds, rec_length))
    save_fingerprint_result_to_file(result)
    if int(result['status']['code']) == 0:
        try:
            song = {
                'name': get_song_name_from_result(result),
                'id': get_spotify_id_from_result(result),
                'artist': get_first_artist_from_result(result),
                'seconds_remaining': get_song_seconds_remaining(result),
                'percent_remaining': get_song_percent_remaining(result),
            }
            print('Song Found: {}'.format(song['name']))
            return song
        except KeyError:
            pass
    return None
