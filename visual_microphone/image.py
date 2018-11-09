import cv2
import numpy as np

BLUE_RGB = (255, 0, 0)
WHITE_RGB = (255, 255, 255)


def create_mask(img):
    lower_color = np.array([0, 0, 0], np.uint8)
    upper_color = np.array([200, 255, 200], np.uint8)

    # Get an Histogram based on the color saturation of the image
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Create a mask based on the lower_color and upper_color
    return cv2.inRange(hsv, lower_color, upper_color)


def erode_mask(mask):
    # Create a kernel matrix
    kernel = np.ones((5, 5), "uint8")

    # Erode the mask using the kernel
    return cv2.erode(mask, kernel, iterations=1)


def get_contours(eroded_mask):
    # Return the contourns of the objects detected with the eroded mask
    (_, contours, _) = cv2.findContours(eroded_mask, cv2.RETR_TREE,
                                        cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_area_from_contour(contour):
    # Get area from contour
    return cv2.contourArea(contour)


def draw_rectangular_contour(img, contour, area):
    # Get the rectangle bounding the contour
    x, y, w, h = cv2.boundingRect(contour)
    # Add the rectangle on the img
    img = cv2.rectangle(img, (x, y), (x + w, y + h), BLUE_RGB, 2)
    # Write Area and its (x, y) coordinates
    cv2.putText(img, "Area {}".format(area), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, BLUE_RGB)

    return img


def get_mass_center(contour):
    # Get the mass center
    M = cv2.moments(contour)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    return cx, cy


def draw_center(img, contour):
    cx, cy = get_mass_center(contour)
    # Add the rectangle on the img
    img = cv2.circle(img, (cx, cy), 7, WHITE_RGB, -1)

    return img


def show_image(img, title="image rendered"):
    # Show the image on a separate window
    cv2.imshow(title, img)


def escape_on_q(cap):
    # Need to press Q on the image
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
