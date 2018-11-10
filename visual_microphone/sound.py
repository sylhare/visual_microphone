import wave
import struct


class Sound(object):

    def __init__(self, sound_file='sounds.wav', channels=1, framerate=2400, amp_width=2, amp_multiplier=6000.0):
        self.audio = wave.open(sound_file, 'wb')
        self.audio.setnchannels(channels)
        self.audio.setframerate(framerate)
        self.audio.setsampwidth(amp_width)
        self.amp_multiplier = amp_multiplier
        self.offset = 0
        self.low_pass = 10

    def write(self, amplitude):
        self.audio.writeframes(struct.pack('h', int(amplitude * self.amp_multiplier / 2)))

    def set_offset(self, offset):
        self.offset = offset

    def trim_amplitude(self, amplitude):
        amplitude = amplitude - self.offset
        if abs(amplitude) > self.low_pass:
            amplitude = 0

        return amplitude


if __name__ == "__main__":
    pass
