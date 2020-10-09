''' This script detects a object of specified object colour from the webcam video feed.
Using OpenCV library for vision tasks and HSV color space for detecting object of given specific color.'''

# Import necessary modules
# from speed_racer import gameLoop
import asyncio
import cv2
import imutils
import numpy as np
import pyautogui
from collections import deque
import time


class Movement:

    def main(self):
        # Define HSV colour range for green colour objects
        self.greenLower = (29, 86, 6)
        self.greenUpper = (64, 255, 255)
        self.up_frame = self.load_image('imgs/fondo1.png')
        self.down_frame = self.load_image('imgs/up.png')
        # Used in deque structure to store no. of given self.buffer points
        self.buffer = 20

        # Points deque structure storing 'self.buffer' no. of object coordinates
        self.pts = deque(maxlen=self.buffer)
        self.video_capture = cv2.VideoCapture(0)
        time.sleep(2)
        # loop = asyncio.get_event_loop()
        # task1 = loop.create_task(self.video_camera())
        self.video_camera()

        # Start video capture

    def video_camera(self):
        while True:
            # Store the readed frame in frame, ret defines return value
            ret, frame = self.video_capture.read()
            # Flip the frame to avoid mirroring effect
            frame = cv2.flip(frame, 1)
            # Resize the given frame to a 600*600 window
            frame = imutils.resize(frame, width=500)

            hsv_converted_frame = self.filter_techniques(frame)
           
            # Create a mask for the frame, showing green values
            mask = cv2.inRange(hsv_converted_frame, self.greenLower, self.greenUpper)
            # Erode the masked output to delete small white dots present in the masked image
            mask = cv2.erode(mask, None, iterations=2)
            # Dilate the resultant image to restore our target
            mask = cv2.dilate(mask, None, iterations=2)

            # Display the masked output in a different window
            cv2.imshow('Masked Output', mask)

            # Find all contours in the masked image
            cnts, _ = cv2.findContours(
                mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Define center of the ball to be detected as None
            center = None

            # If any object is detected, then only proceed
            if(len(cnts)) > 0:
                # Find the contour with maximum area
                c = max(cnts, key=cv2.contourArea)
                # Find the center of the circle, and its radius of the largest detected contour.
                ((x, y), radius) = cv2.minEnclosingCircle(c)

                self.centroid_calculate(c)

                if x > 210 and y < 276:
                    pyautogui.press("right")
                if x < 300 and y < 276:
                    pyautogui.press("left")
                if y > 277:
                    pyautogui.press("enter")
                # Proceed only if a ball of considerable size is detected
                if radius > 10:
                    # Draw circles around the object as well as its centre
                    cv2.circle(frame, (int(x), int(y)),
                               int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 255, 255), -1)

                # Append the detected object in the frame to self.pts deque structure
                self.pts.appendleft(center)

            # Show the output frame
            alpha = 0.5
            added_image = cv2.addWeighted(frame[0:370, 0:500, :], alpha, self.up_frame[0:370, 0:500, :], 1-alpha, 0)
            frame[0:370, 0:500] = added_image

            cv2.imshow('Frame', frame)
            key = cv2.waitKey(1) & 0xFF

            # If q is pressed, close the window
            if(key == ord('q')):
                self.quit()

    def centroid_calculate(self, c):
        # Calculate the centroid of the ball, as we need to draw a circle around it.
        M = cv2.moments(c)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        return center


    def load_image(self, image_url):
        return cv2.imread(image_url)


    def filter_techniques(self,frame):
        # Blur the frame using Gaussian Filter of kernel size 5, to remove excessivve noise
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
        # Convert the frame to HSV, as HSV allow better segmentation.
        hsv_converted_frame = cv2.cvtColor(
            blurred_frame, cv2.COLOR_BGR2HSV)
        return hsv_converted_frame


    def quit(self):
        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    movement = Movement()
    movement.main()

