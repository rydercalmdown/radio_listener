#!/bin/bash

brew install portaudio ffmpeg librtlsdr sox coreutils mpg321
virtualenv -p python3 ../env
. ../env/bin/activate
pip install -r ../app/requirements.txt
