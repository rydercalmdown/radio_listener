import os
import helpers
import switches
import subprocess
import lcd_display
from gtts import gTTS


def say_information_out_loud(song, station_frequency):
    """Says information out loud, because we're driving and that's the safest way"""
    message = "{}, by {} is playing on {} .".format(song['name'], song['artist'], station_frequency)
    if switches.is_active_time_remaining_switch():
        message += 'There are {} seconds left.'.format(song['seconds_remaining'])
    gTTS(text=message, lang='en', slow=False).save(helpers.get_notification_output_path())
    # subprocess.Popen(['mpg321', helpers.get_notification_output_path()])
    os.system("mpg321 --quiet {}".format(helpers.get_notification_output_path()))


def display_screen(song, station_frequency):
    message = "{} - {} by {}".format(station_frequency, song['name'], song['artist'])
    lcd_display.write(song['name'], 1)
    lcd_display.write(song['artist'], 2)
    lcd_display.write(str(song['seconds_remaining']) + ' seconds left...', 3)
    lcd_display.write(station_frequency + ' FM', 4)


def display_simple_message(message):
    """Displays a simple message to the user"""
    lcd_display.clear()
    lcd_display.write(message, 1)


def notify_song_found(song, station_frequency, favourite=False):
    """Notifies a user that a song has been found"""
    display_screen(song, station_frequency)
    if switches.is_active_announce_all_songs_switch() or favourite:
        say_information_out_loud(song, station_frequency)


def play_startup_sound():
    """Plays a startup sound over the speakers"""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'misc/startup.mp3')
    os.system("mpg321 --quiet {}".format(path))
