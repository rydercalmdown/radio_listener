import os
import platform
import pydub
import requests


def is_internet_connected():
    url = 'https://rydercalmdown.com'
    response = requests.get(url)
    return response.status_code == 200


def get_wav_output_path():
    """Returns the path associated with the wave output"""
    return '/tmp/radio_sample.wav'


def get_mp3_output_path():
    """Returns the path associated with the mp3 output"""
    return '/tmp/radio_sample.mp3'


def get_notification_output_path():
    """Returns the path associated with the notification output"""
    return '/tmp/notification_message.mp3'


def get_json_output_directory():
    """Returns the directory associated with song output"""
    directory = '/tmp/fingerprinting_results'
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_recording_length_seconds():
    """Returns the sample length of the recording in seconds"""
    return 5


def convert_wav_to_mp3():
    """Creates an MP3 from the audio source"""
    print('Converting wav to mp3')
    sound = pydub.AudioSegment.from_wav(get_wav_output_path())
    sound.export(get_mp3_output_path(), format='mp3')


def remove_file_if_exists(file_path):
    """Remove a file if it exists"""
    if os.path.exists(file_path):
        os.remove(file_path)


def is_running_on_osx():
    """Returns true if we are running on osx"""
    return platform.system() == 'Darwin'


def clean_up():
    """Cleans up all files afterwards"""
    remove_file_if_exists(get_wav_output_path())
    remove_file_if_exists(get_mp3_output_path())
    remove_file_if_exists(get_notification_output_path())
