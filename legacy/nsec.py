import cv2
import numpy as np
import wave
from time import time as timer
import struct
import math

audio = wave.open('chips.wav', 'wb')
audio.setnchannels(1)
audio.setframerate(2400)
audio.setsampwidth(2)
# Captura de video a traves de la webcam
#cap = cv2.VideoCapture('./chips.mp4')
cap = cv2.VideoCapture(0)

fps = cap.get(cv2.CAP_PROP_FPS)
fps = 24 / 100
framerate = timer()
elapsed = int()
amp = 6000.0  # multiplier for amplitude

while (cap.isOpened()):
    start = timer()
    d = 0.1
    centers = []
    _, img = cap.read()

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Se obtiene un histograma basada en las saturaciones de colores.

    blue_lower = np.array([0, 0, 0], np.uint8)
    blue_upper = np.array([200, 255, 200], np.uint8)

    blue = cv2.inRange(hsv, blue_lower, blue_upper)  # Se crea una mascara utilizando intervalos de color azul.
    kernal = np.ones((5, 5), "uint8")  # Crea una matriz de 5x5 la cual recorrera el video,

    blue = cv2.erode(blue, kernal, iterations=1)  # Se erosiona utilizando el kernel sobre la mascara.
    # res1=cv2.bitwise_and(img, img, mask = blue) #La nueva imagen reemplazara a blue.

    (_, contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)  # Encuentra los contornos de los objetos que se ven en el filtroRGB(171, 187, 68)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)  # funcion de opencv que obtiene los contornos
        if (area > 100000 and area < 103000):
            x, y, w, h = cv2.boundingRect(contour)  # Encuentra coordenadas de los contornos.
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Spot {}".format(area), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))

            M = cv2.moments(contour)  # Se obtiene el centro de masa de los marcadores enconrados.
            print(M)
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            cv2.circle(img, (cx, cy), 7, (255, 255, 255), -1)

            cy = cy - 392
            print(cy)
            if (abs(cy) > 10):
                cy = 0

            cy /= 10.0
            audio.writeframes(struct.pack('h', int(cy * amp / 2)))

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
