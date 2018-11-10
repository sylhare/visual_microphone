from time import time as timer
import cv2


class Framer(object):

    def __init__(self, capture):
        self.timer = timer()
        self.difference = 0
        self.fps = capture.get(cv2.CAP_PROP_FPS) / 100

    def lap(self):
        """ To Adapt to the right frequency """
        while self.difference < self.fps:
            self.difference = timer() - self.timer
