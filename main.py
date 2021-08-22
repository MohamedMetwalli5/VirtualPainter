import cv2 as cv
import imutils
import numpy as np
import time

def play_drums(x,y):
    pass

img1 = cv.imread("1.png")
img2 = cv.imread("2.png")
img3 = cv.imread("3.png")
img4 = cv.imread("4.png")
img5 = cv.imread("5.png")
img6 = cv.imread("6.png")
img7 = cv.imread("7.png")

images_list = [img1, img2, img3, img4, img5, img6, img7]
capture = cv.VideoCapture(0)

while True:
    isTrue, frame = capture.read()
    frame = imutils.resize(frame, width=1280)
    frame = cv.flip(frame, 1)    # to make the frame displayed properly
    frame[0:125, 0:1280] = images_list[0]

    hsv_frame = cv.cvtColor(frame[126:, 0:1280], cv.COLOR_BGR2HSV)

    low_green = np.array([42, 129, 33])
    high_green = np.array([80, 255, 255])
    mask = cv.inRange(hsv_frame, low_green, high_green)
    contours,_ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # print(contours)

    x, y = 0, 0
    f_center, f_radius = 0, 0

    try:
        for i in range(10):
            f_center, f_radius = cv.minEnclosingCircle(contours[i])
            x, y = int(f_center[0]), int(f_center[1])

            if cv.contourArea(contours[i]) > 2100:
                cv.circle(frame, (x, y), 10, (0, 250, 250), 3)
                break
    except:
        pass

    cv.imshow("Mask", mask)


    cv.imshow("Virtual Painter",frame)
    if cv.waitKey(6) & 0xFF == ord("q"):
        break

capture.release()
cv.destroyAllWindows()
