import cv2 as cv
import mediapipe as mp
import imutils
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands


img1 = cv.imread("1.png")
img2 = cv.imread("2.png")
img3 = cv.imread("3.png")
img4 = cv.imread("4.png")
img5 = cv.imread("5.png")
img6 = cv.imread("6.png")
img7 = cv.imread("7.png")

images_list = [img1, img2, img3, img4, img5, img6, img7]


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

capture = cv.VideoCapture(0)
black = (0,0,0)
white = (255,255,255)
blue = (255,0,0)
red = (0,0,255)
green = (0,255,0)
yellow = (0,255,255)
image_number = 0
color = black
with mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5, max_num_hands = 2) as hands:
    while True:
        flag, frame = capture.read()
        frame = imutils.resize(frame, width=1280)
        frame[0:125, 0:1280] = images_list[image_number]

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # the form of the image that the media pipe accepts
        image = cv.flip(image, 1)
        image.flags.writeable = False #open the lock
        results = hands.process(image)
        image.flags.writeable = True #close the lock

        image = cv.cvtColor(image, cv.COLOR_RGB2BGR) # displaying the image after processing

        # print(results)

        if results.multi_hand_landmarks: # if there is a hand in the frame
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )
                x = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 1280)
                y = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 720)

                if y >= 0 and y <= 125:
                    if x >= 0 and x <= 163:
                        # delete
                        image_number = 6
                        continue
                    elif x >= 184 and x <= 344:
                        color = yellow
                        image_number = 4
                    elif x >= 372 and x <= 535:
                        color = black
                        image_number = 5
                    elif x >= 565 and x <= 724:
                        color = red
                        image_number = 3
                    elif x >= 758 and x <= 916:
                        color = white
                        image_number = 2
                    elif x >= 940 and x <= 1098:
                        color = green
                        image_number = 1
                    elif x >= 1100 and x <= 1280:
                        color = blue
                        image_number = 0

                cv.circle(image, (x,y), 10, color, thickness=4)
                print(x, y)

        cv.imshow('Virtual Painter', image)

        if cv.waitKey(10) & 0xFF == ord('q'):
            break

capture.release()
cv.destroyAllWindows()