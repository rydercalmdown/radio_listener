import helpers
import pyaudio
import wave


def record_wav_from_microphone():
    """Creates a wav file from listening to the device microphone"""
    print('Starting microphone recording...')
    chunk = 1024
    sample_format = pyaudio.paInt16
    channels = 2
    fs = 44100
    seconds = helpers.get_recording_length_seconds()
    filename = helpers.get_wav_output_path()
    p = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('Saving recorded file to {}...'.format(filename))
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()
    helpers.convert_wav_to_mp3()
