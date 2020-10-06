import os
import helpers
import switches


def get_known_radio_frequencies():
    """Returns a list of known radio frequencies in Mhz"""
    return [
        '107.7',
        '106.9',
        '105.3',
        '103.9',
        '103.1',
        '102.3',
        '101.3',
        '98.1',
        '97.5',
        '96.7',
        '95.9',
        '95.3',
        '93.9',
        '92.7',
    ]


def convert_str_frequency_to_hertz(frequency):
    """Takes a string frequency like '103.1' to hertz"""
    return int(float(frequency) * 1000000)


def generate_wav_on_frequency_osx(frequency):
    """Generates a wav file on frequency for OSX"""
    frequency = convert_str_frequency_to_hertz(frequency)
    recording_length = helpers.get_recording_length_seconds()
    output_path = helpers.get_wav_output_path()
    rtl_cmd = 'rtl_fm -f {frequency} -M wbfm -s 200000 -r 48000 -'.format(**locals())
    if switches.is_active_listen_in_switch():
        sox_pipe = 'tee >( play -r 48000 -t s16 -L -c 1  - ) | sox -t raw -e signed -c 1 -b 16 -r 48000 - {output_path} > /dev/null'.format(**locals())
    else:
        sox_pipe = 'sox -t raw -e signed -c 1 -b 16 -r 48000 - {output_path} > /dev/null'.format(**locals())
    radio_cmd = rtl_cmd + ' | ' + sox_pipe
    main_cmd = 'timeout {recording_length} bash -c "{radio_cmd}" > /dev/null'.format(**locals())
    if helpers.is_running_on_osx():
        main_cmd = 'g' + main_cmd
    os.system(main_cmd)
    helpers.convert_wav_to_mp3()


def stream_on_frequency(frequency, timeout_seconds):
    """Streams to speakers on frequency for a timeout period"""
    frequency = convert_str_frequency_to_hertz(frequency)
    rtl_cmd = 'rtl_fm -f {frequency} -M wbfm -s 200000 -r 48000 - '.format(**locals())
    sox_pipe = '| play -r 48000 -t s16 -L -c 1  -'
    radio_cmd = rtl_cmd + sox_pipe
    main_cmd = 'timeout {timeout_seconds} bash -c "{radio_cmd}" > /dev/null'.format(**locals())
    if helpers.is_running_on_osx():
        main_cmd = 'g' + main_cmd
    os.system(main_cmd)
