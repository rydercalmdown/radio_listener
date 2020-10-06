# Radio Listener Project
A raspberry pi based device that iterates through radio stations, fingerprints songs, compares them to a known list and lets me know when one I like is playing.


## Installation
I originally built the core components of this on my OSX computer before moving it to a raspberry pi - so you'll find code and installation instructions accounting for both.

### Raspberry Pi Installation
These components are required for development on OSX, they're mostly to do with listening to the microphone - not the radio. If you don't need to do this, don't worry about it.

Follow the instructions in my example pi_loop repository - just don't clone the code, and don't configure rc.local. Everything else should still apply.

Copy over the application code to your raspberry pi via SCP.
```bash
make copy
```

Reinstall python3-pip, and virtualenv since they're probably not working correctly.
```bash
sudo apt-get update && sudo apt-get -y install python3-pip
sudo python3 -m pip install virtualenv
```

In the radio_listener directory, create a virtual environment with python3 as your python binary.
```bash
cd /home/pi/radio_listener && virtualenv env
```

Activate your virtual environment, and install python dependencies.
```bash
. env/bin/activate && pip install -r requirements.txt
```

We then need to fix the acrcloud dependency, since it doesn't install properly by default. While still in the virtual environment, run the following:
```bash
pip uninstall pyacrcloud
cd /home/pi
# you'll need git for this if you don't already have it.
git clone https://github.com/acrcloud/acrcloud_sdk_python.git
cd /home/pi/acrcloud_sdk_python/raspberrypi/aarch32/python3 && python setup.py install
```

Next, install base dependencies
```bash
sudo apt-get update \
    && sudo apt-get -y install rtl-sdr sox ffmpeg coreutils libasound-dev libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
```

Then blacklist old drivers that we don't need to use:
```bash
echo 'blacklist dvb_usb_rtl28xxu' | sudo tee --append /etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf
```

Restart the raspberry pi.
```bash
sudo reboot
```

You can test whether or not everything is functioning by running the following command - which is listening on 103.1 FM.

```bash
rtl_fm -f 103100000 -M wbfm -s 200000 -r 48000 - | play -r 48000 -t s16 -L -c 1  -
```

Configure the app to run on startup:
```bash
sudo nano /etc/rc.local
```

Add the following line before the end:
```txt
bash /home/pi/radio_listener/entrypoint.sh &
```


### OSX Installation

These components are required for development on OSX, they're mostly to do with listening to the microphone - not the radio. If you don't need to do this, don't worry about it.
```bash
brew install portaudio
brew install ffmpeg
```

These are lower level dependencies are required to operate the radio.
```bash
# OSX rtl-sdr, available on path as rtl_fm, also for sox, play, and gtimeout
brew install librtlsdr
brew install sox
brew install coreutils
```

The following components are required for text to speech to function.
```bash
brew install mpg321
```

To install python dependencies simply, use a virtual environment.
```bash
# Create the virtual environment
virtualenv -p python3 env

# Activate it
. env/bin/activate

# Install the python requirements
pip install -r src/requirements.txt
```


## Music Fingerprinter
This project uses a music fingerprinting API. There are many available, but I'm using ACRCloud since it's got a free tier, is easy to set up, and doesn't require me to speak to salespeople before I try it out.

If you want to do the same, you'll need to setup an account with them, a project, and grab the necessary environment variables:

```bash
export ACR_HOST=
export ACR_ACCESS_KEY=
export ACR_ACCESS_SECRET=
```

A typical positive response from the fingerprinting service looks like this, and has lots of information we can play with. I make the assumption that the spotify key needs to exist, as I compare all songs against my main music source - spotify.

```json
{
    "metadata": {
        "timestamp_utc": "2020-05-24 00:26:07",
        "music": [{
            "play_offset_ms": 225640,
            "artists": [{
                "name": "Beyonc\u00e9"
            }],
            "lyrics": {
                "copyrights": ["Sony/ATV Music Publishing LLC", "Warner/Chappell Music", "Inc."]
            },
            "acrid": "adc3642e397fe01e3800abbaca9df129",
            "genres": [{
                "name": "Pop"
            }, {
                "name": "R&B/Soul/Funk"
            }, {
                "name": "Contemporary R&B"
            }],
            "album": {
                "name": "I AM...SASHA FIERCE"
            },
            "label": "Music World Music/Columbia",
            "external_ids": {},
            "result_from": 3,
            "contributors": {
                "composers": ["Beyonc\u00e9 Knowles", "Ryan Tedder", "Evan Kidd Bogart"],
                "lyricists": ["Beyonce Knowles", "Evan Kidd Bogart", "Ryan B. Tedder"]
            },
            "title": "Halo",
            "duration_ms": 261000,
            "score": 100,
            "external_metadata": {
                "spotify": {
                    "track": {
                        "name": "Halo",
                        "id": "2CvOqDpQIMw69cCzWqr5yr"
                    },
                    "artists": [{
                        "name": "Beyonc\u00e9",
                        "id": "6vWDO969PvNqNYHIOW5v0m"
                    }],
                    "album": {
                        "name": "I AM...SASHA FIERCE - Platinum Edition",
                        "id": "3ROfBX6lJLnCmaw1NrP5K9"
                    }
                }
            },
            "release_date": "2008-11-14"
        }]
    },
    "cost_time": 0.046999931335449,
    "status": {
        "msg": "Success",
        "version": "1.0",
        "code": 0
    },
    "result_type": 0
}
```

## Hardware & Architecture
This project uses a Raspberry Pi with WiFi tethered to my mobile phone. It's entirely possible to use a GSM module with the raspberry pi so a phone isn't required - but that's too much work for this project so I didn't do it. You'll additionally need a power supply that can adapt to your car (or a battery), USB speakers, and possibly a LCD screen.


### Software Defined Radio (SDR) Component
I'm using a Nooelec NESDR Smart v4 Bundle for my SDR receiver, connected via USB to the raspberry pi. They've got a [guide for how to set it up with linux here](https://www.nooelec.com/store/qs#linux).

### Architecture
- Hardware
    - SDR Receiver
    - Raspberry Pi
    - WiFi Card or GSM Module
    - Speakers
    - Screen
- Software
    - Radio iterator module
    - Fingerprinting and song normalization module
    - Comparison module
    - Speech to text module
