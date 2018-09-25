import unittest
import os
from visual_microphone.sound import Sound


class TestVisualMicrophone(unittest.TestCase):
    def setUp(self):
        pass

    def test_sound_file_created(self):
        s = Sound()
        for i in range(0, 1000):
            s.write(0.4)
        self.assertTrue(os.path.isfile('sounds.wav'))


if __name__ == "__main__":
    unittest.main()