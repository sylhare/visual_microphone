import cv2

from visual_microphone import image
from visual_microphone.sound import Sound


class VisualMicrohone(object):
    def __init__(self, video, title="new-sound"):
        self.capture = cv2.VideoCapture(video)
        self.image = None
        self.area = None
        self.sound = Sound("{}.wav".format(title))
        self.lower = 100000
        self.higher = self.lower + 3000

    def record(self):
        print("... recording ...")
        while self.capture.isOpened():
            _, self.image = self.capture.read()
            list(map(lambda x: self.detect_sound(x[1]), enumerate(image.create_coutours(self.image))))

    def detect_sound(self, contour):
        self.area = image.get_area_from_contour(contour)

        if self.lower < self.area < self.higher:
            self.__experience(contour)
            cx, cy = image.get_mass_center(contour)
            amplitude = self.sound.trim_amplitude(cy)
            self.sound.write(amplitude)

    def __experience(self, contour):
        """ To add some user exeprience"""
        self.image = image.draw_rectangular_contour(self.image, contour, self.area)
        image.show_image(self.image, "visual microphone")
        image.escape_on_q(self.capture)


if __name__ == "__main__":
    mic = VisualMicrohone('../resources/chips.mp4')
    mic.record()
