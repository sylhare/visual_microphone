import wave
import struct


class Sound(object):

    def __init__(self, sound_file='sounds.wav', channels=1, framerate=2400, amp_width=2, amp_multiplier=6000.0):
        self.audio = wave.open(sound_file, 'wb')
        self.audio.setnchannels(channels)
        self.audio.setframerate(framerate)
        self.audio.setsampwidth(amp_width)
        self.amp_multiplier = amp_multiplier

    def write(self, amplitude):
        self.audio.writeframes(struct.pack('h', int(amplitude * self.amp_multiplier / 2)))


if __name__ == "__main__":
    pass
    # s = Sound()
    # for i in range(0, 1000):
    #     s.write(0.4)