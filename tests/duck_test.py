from visual_microphone import image
from visual_microphone.sound import Sound
from visual_microphone.visual_microphone import VisualMicrohone
import cv2

s = Sound("duck-sound-2.wav")
s.offset = 392

cap = VisualMicrohone.setup_capture('../resources/chips.mp4')

fps = cap.get(cv2.CAP_PROP_FPS) / 100

while cap.isOpened():
    _, img = cap.read()

    contours = image.create_coutours(img)

    for pic, contour in enumerate(contours):
        area = image.get_area_from_contour(contour)

        if 100000 < area < 103000:
            img = image.draw_rectangular_contour(img, contour, area)
            cx, cy = image.get_mass_center(contour)

            cy = s.trim_amplitude(cy)
            s.write(cy)

    image.show_image(img, "duck test")
    image.escape_on_q(cap)

if __name__ == "__main__":
    pass
