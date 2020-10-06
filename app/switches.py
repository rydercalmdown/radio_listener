import RPi.GPIO as GPIO


def get_pin_announce_all_songs_switch():
    """Returns the pin of the favourites switch"""
    return 11


def get_pin_time_remaining_switch():
    """Returns the pin of the time remaining switch"""
    return 13


def get_listen_in_switch():
    """Returns the pin of the time remaining switch"""
    return 15


def is_active_announce_all_songs_switch():
    """Returns true if the announce all songs switch is on"""
    return GPIO.input(get_pin_announce_all_songs_switch()) == 1


def is_active_time_remaining_switch():
    """Returns true if the announce time remaining switch is on"""
    return GPIO.input(get_pin_time_remaining_switch()) == 1


def is_active_listen_in_switch():
    """Returns true if the announce time remaining switch is on"""
    return GPIO.input(get_listen_in_switch()) == 1


def setup():
    """Sets up switches on the raspberry pi"""
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(get_pin_announce_all_songs_switch(), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(get_pin_time_remaining_switch(), GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(get_listen_in_switch(), GPIO.IN, pull_up_down=GPIO.PUD_UP)


def teardown():
    """Cleans up GPIO"""
    GPIO.cleanup()
