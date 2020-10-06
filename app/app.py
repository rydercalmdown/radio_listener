import time
import helpers
import fingerprinter
import microphone
import notifications
import spotify
import radio
import switches


def listen_for_song(station_frequency=None):
    """Listens for a song on the radio and notifies if the song is acceptable"""
    if not station_frequency:
        # Use microphone
        station_frequency = '101.1'
        microphone.record_wav_from_microphone()
    else:
        radio.generate_wav_on_frequency_osx(station_frequency)
    song = fingerprinter.get_fingerprint()
    if song:
        notifications.notify_song_found(song, station_frequency, spotify.is_song_acceptable(song))
    else:
        print('Song Not Found')
    helpers.clean_up()


def wait_for_internet():
    """Wait for the internet to be connected before continuing"""
    notifications.display_simple_message('Checking WiFi...')
    while not helpers.is_internet_connected():
        notifications.display_simple_message('Waiting for WiFi...')
        sleep(10)
    notifications.display_simple_message('WiFi Connected')


def main():
    """Run the program"""
    switches.setup()
    notifications.display_simple_message('Starting up...')
    notifications.play_startup_sound()
    wait_for_internet()
    try:
        while True:
            for frequency in radio.get_known_radio_frequencies():
                notifications.display_simple_message('Listening on {}'.format(frequency))
                listen_for_song(frequency)
                helpers.clean_up()
    except KeyboardInterrupt:
        print('Exiting...')


if __name__ == '__main__':
    main()
