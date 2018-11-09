from visual_microphone import image
from visual_microphone.sound import Sound
from visual_microphone.visual_microphone import VisualMicrohone
import cv2
from time import time as timer

s = Sound("duck-sound-2.wav")

cap = VisualMicrohone.setup_capture('../resources/chips.mp4')

fps = cap.get(cv2.CAP_PROP_FPS) / 100

while cap.isOpened():
    start = timer()
    _, img = cap.read()

    mask = image.create_mask(img)
    eroded_mask = image.erode_mask(mask)
    contours = image.get_contours(eroded_mask)

    for pic, contour in enumerate(contours):
        area = image.get_area_from_contour(contour)

        if 100000 < area < 103000:
            img = image.draw_rectangular_contour(img, contour, area)
            cx, cy = image.get_mass_center(contour)

            cy = s.trim_amplitude(cy)
            s.write(cy)

    image.show_image(img, "duck test")
    image.escape_on_q(cap)

    diff = timer() - start
    while diff < fps:
        diff = timer() - start

if __name__ == "__main__":
    pass
