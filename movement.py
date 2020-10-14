''' This script detects a object of specified object colour from the webcam video feed.
Using OpenCV library for vision tasks and HSV color space for detecting object of given specific color.'''

#Importa modulos necesarios
import cv2
import imutils
import numpy as np
import pyautogui
from collections import deque
import time
import math

#Definr color HSV del rango de color de objetos verdes
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
up_frame = cv2.imread('.imgs/fondo1.png')
down_frame = cv2.imread('.imgs/up.png')
#Usar en una estructura cola para almancenar los puntos en buffer
buffer = 20


pts = deque(maxlen = buffer)

#Inicia video
video_capture = cv2.VideoCapture(0)

#Dormir por dos segundos la captura
time.sleep(2)

#Ciclo OpenCV
while True:
    #Almancenar el frame leido
    ret, frame = video_capture.read()
    #Flip the frame para evitar el efecto de espejo
    frame = cv2.flip(frame,1)
    #Cmabio de tamaño a 600x600
    frame = imutils.resize(frame, width = 500)
    #Aplicar filtro gaussian bllur de tamaño 5, remover el exceso de ruido
    blurred_frame = cv2.GaussianBlur(frame, (5,5), 0)
    
    #Convertir frame rgb a hsv
    hsv_converted_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    #Crear máscara para el grame, mostrando valores verdes
    mask = cv2.inRange(hsv_converted_frame, greenLower, greenUpper)
    #Erosionar la salida para eliminar los pequeños puntos blancos presentes en la imagen enmascarada
    mask = cv2.erode(mask, None, iterations = 2)
    #Dilara la imagen resultante para guardar como nuestro nuevo objetivo
    mask = cv2.dilate(mask, None, iterations = 2)

    cv2.imshow('Masked Output', mask)

    #Encuentra todos los contornos en la imagen de mascara
    cnts,_ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    center = None


    if(len(cnts)) > 0:
        #Find the contour with maximum area
        c = max(cnts, key = cv2.contourArea)
        #Encuentra el centro del circulo y su radio de la detección mas grande del contorno
        ((x,y), radius) = cv2.minEnclosingCircle(c)

        #Calcular el centroido alrededor de la bola para dibujarlo
        M = cv2.moments(c)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        print("x: " + str(x))
        print("y: " + str(y))
        print("radius: " + str(radius))
        if x>210 and y<276:
            pyautogui.press("right")
        if x<300 and y <276:
            pyautogui.press("left")
        if y>277:
            pyautogui.press("enter")

        if radius > 10:
            #Dibujar los circulos alrededor del objeto 
            cv2.circle(frame, (int(x), int(y)), int(radius), (0,255,255), 2)
            cv2.circle(frame, center, 5, (0,255,255), -1)

        #Concatena los centroides
        pts.appendleft(center)



    alpha = 0.5
    foreground = np.ones((100,100,3),dtype='uint8')*255
    added_image = cv2.addWeighted(frame[0:370,0:500,:],alpha,up_frame[0:370,0:500,:],1-alpha,0)
    frame[0:370,0:500] = added_image


    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF

    #Si presiona q se termina la ejecución
    if(key == ord('q')):
        break

video_capture.release()
cv2.destroyAllWindows()
