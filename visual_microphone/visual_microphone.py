import cv2
import numpy as np
from time import time as timer


class VisualMicrohone(object):
    def __init__(self, upper, lower, video):
        self.capture = self.setup_capture(video)
        self.start = 0
        self.mask = None
        self.area_size_min = None
        self.area_size_max = None
        self.lower_color_range = np.array(lower, np.uint8)
        self.upper_color_range = np.array(upper, np.uint8)
        self.amplitudes = []

    @staticmethod
    def setup_capture(video):
        """Give path to the video or 0 for webcam"""
        return cv2.VideoCapture(video)

    def escape_on_q(self):
        """ Press 'q' on the video to quit the program """
        escape = False
        if cv2.waitKey(10) & 0xFF == ord('q'):
            self.capture.release()
            cv2.destroyAllWindows()
            escape = True

        return escape

    def set_color_mask(self, img):
        """ Create a mask based on the hsv profile of the image from the video and the selected color """
        img_hsv_profile = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        self.mask = cv2.inRange(img_hsv_profile, self.lower_color_range, self.upper_color_range)
        self.__erode_mask()

    def __erode_mask(self):
        """ Erode the pixel near the border in the mask to reduce noise """
        kernel = np.ones((5, 5), "uint8")
        self.mask = cv2.erode(self.mask, kernel, iterations=1)

    def get_contours(self):
        """ Get the contours of the objects found with the mask """
        (_, contours, hierarchy) = cv2.findContours(self.mask, cv2.RETR_TREE,
                                                    cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def select_area(self, contour):
        area = cv2.contourArea(contour)
        if self.area_size_min is None:
            self.area_size_min = area

        if self.area_size_max is None:
            self.area_size_max = area

        if self.area_size_min <= area <= self.area_size_min:
            area = False
        return area

    def get_movement_amplitude(self, contour):
        """ Getting the centroid of the contour and returning its relative coordinates """
        centroid = cv2.moments(contour)
        cx = int(centroid['m10'] / centroid['m00'])
        cy = int(centroid['m01'] / centroid['m00'])
        print(cx)
        self.amplitudes.append([cx, cy, self.get_time()])

    def get_time(self):
        return timer() - self.start

    def process_video(self):
        while self.capture.isOpened():
            print("yeah")
            self.start = timer()
            _, img = self.capture.read()
            cv2.imshow("Color Tracking", img)
            self.escape_on_q()
            self.set_color_mask(img)
            contours = self.get_contours()
            for _, contour in enumerate(contours):
                if self.select_area(contour):
                    self.get_movement_amplitude(contour)


if __name__ == "__main__":
    vm = VisualMicrohone([0, 0, 0], [255, 255, 255], "../resources/chips.mp4")
    vm.process_video()

