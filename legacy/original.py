import cv2
import numpy as np

#Captura de video a traves de la webcam
cap=cv2.VideoCapture(0)

while(1):
    d=0.1
    centers=[]
    _, img = cap.read()

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV) #Se obtiene un histograma basada en las saturaciones de colores.

    blue_lower=np.array([80,150,100],np.uint8)
    blue_upper=np.array([150,255,255],np.uint8)

    blue=cv2.inRange(hsv,blue_lower,blue_upper) #Se crea una mascara utilizando intervalos de color azul.

    kernal = np.ones((5 ,5), "uint8") #Crea una matriz de 5x5 la cual recorrera el video,

    blue=cv2.erode(blue,kernal, iterations=1) #Se erosiona utilizando el kernel sobre la mascara.
    res1=cv2.bitwise_and(img, img, mask = blue) #La nueva imagen reemplazara a blue.


    (_,contours,hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #Encuentra los contornos de los objetos que se ven en el filtro

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour) #funcion de opencv que obtiene los contornos
        if(area>300):
            x,y,w,h = cv2.boundingRect(contour) #Encuentra coordenadas de los contornos.
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            cv2.putText(img,"Marcador",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))


            M = cv2.moments(contour) #Se obtiene el centro de masa de los marcadores enconrados.
            cx = int(M['m10'] /M['m00'])
            cy = int(M['m01'] /M['m00'])
            centers.append([cx,cy])
            cv2.circle(img, (cx, cy), 7, (255, 255, 255), -1)

        if len(centers)==2:
            D = np.linalg.norm(cx-cy) #Se aplica distancia euclidiana para encontrar la distancia entre los centros de ...