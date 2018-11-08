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
        if (area > 100000 and area < 103000):
            img = image.add_rectangle_of_contour_on_image(img, contour, area)
            cx, cy = image.get_mass_center_of_contour(contour)

            cy = s.trim_amplitude(cy)
            s.write(cy)

    cv2.imshow("Color Tracking", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

    diff = timer() - start
    while diff < fps:
        diff = timer() - start

if __name__ == "__main__":
    pass
