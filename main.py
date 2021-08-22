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

with mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5, max_num_hands = 2) as hands:
    while True:
        flag, frame = capture.read()
        frame = imutils.resize(frame, width=1280)
        frame[0:125, 0:1280] = images_list[0]

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

        cv.imshow('Virtual Painter', image)

        if cv.waitKey(10) & 0xFF == ord('q'):
            break

capture.release()
cv.destroyAllWindows()