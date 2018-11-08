import wave
import struct


class Sound(object):

    def __init__(self, sound_file='sounds.wav', channels=1, framerate=2400, amp_width=2, amp_multiplier=6000.0):
        self.audio = wave.open(sound_file, 'wb')
        self.audio.setnchannels(channels)
        self.audio.setframerate(framerate)
        self.audio.setsampwidth(amp_width)
        self.amp_multiplier = amp_multiplier
        self.offset = 392

    def write(self, amplitude):
        self.audio.writeframes(struct.pack('h', int(amplitude * self.amp_multiplier / 2)))

    def trim_amplitude(self, amplitude):
        amplitude = amplitude - self.offset
        if abs(amplitude) > 10:
            amplitude = 0

        return amplitude / 10.0


if __name__ == "__main__":
    pass
