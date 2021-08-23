import cv2 as cv
import mediapipe as mp
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
mode = "selection mode"
brush_thickness = 15

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
xp,yp = 0,0

capture = cv.VideoCapture(0)
black = (0,0,0)
white = (255,255,255)
blue = (255,0,0)
red = (0,0,255)
green = (0,255,0)
yellow = (0,255,255)
brown = (0, 75, 150)
image_number = 0
color = black
image_canvas = np.zeros((720, 1280, 3), np.uint8)
with mp_hands.Hands(min_detection_confidence = 0.8, min_tracking_confidence = 0.5, max_num_hands = 2) as hands:
    while True:
        flag, frame = capture.read()
        frame = cv.resize(frame, (1280, 720))
        frame[0:125, 0:1280] = images_list[image_number]

        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB) # the form of the image that the media pipe accepts
        image = cv.flip(image, 1)
        # mask = cv.inRange(image[126:, 0:1280], blue, blue)
        image.flags.writeable = False #open the lock
        results = hands.process(image)
        image.flags.writeable = True #close the lock

        image = cv.cvtColor(image, cv.COLOR_RGB2BGR) # displaying the image after processing

        if results.multi_hand_landmarks: # if there is a hand in the frame
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                                          mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )
                x1 = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * 1280)
                y1 = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * 720)

                x2 = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * 1280)
                y2 = int(results.multi_hand_landmarks[0].landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * 720)



                if y1 >= 0 and y1 <= 125:
                    if x1 >= 0 and x1 <= 163:
                        color = black
                        image_number = 6
                        brush_thickness = 35
                    elif x1 >= 184 and x1 <= 344:
                        color = yellow
                        image_number = 4
                        brush_thickness = 15
                    elif x1 >= 372 and x1 <= 535:
                        color = brown
                        image_number = 5
                        brush_thickness = 15
                    elif x1 >= 565 and x1 <= 724:
                        color = red
                        image_number = 3
                        brush_thickness = 15
                    elif x1 >= 758 and x1 <= 916:
                        color = white
                        image_number = 2
                        brush_thickness = 15
                    elif x1 >= 940 and x1 <= 1098:
                        color = green
                        image_number = 1
                        brush_thickness = 15
                    elif x1 >= 1100 and x1 <= 1280:
                        color = blue
                        image_number = 0
                        brush_thickness = 15
                if abs(x1-x2) <= 56:
                    mode = "selection mode"
                    print("selection mode")
                    xp, yp = x1, y1
                else:
                    mode = "painting mode"
                    print("painting mode")
                    if xp == 0 and yp == 0:
                        xp = x1
                        yp = y1
                    if mode == "painting mode":
                        cv.line(image_canvas,(xp,yp), (x1,y1), color, brush_thickness)
                    xp, yp = x1, y1
                cv.circle(image, (x1,y1), 10, color, cv.FILLED)
                # print(x1, y1)

        image_gray = cv.cvtColor(image_canvas, cv.COLOR_BGR2GRAY)
        _, image_inv = cv.threshold(image_gray, 50, 255, cv.THRESH_BINARY_INV)
        image_inv = cv.cvtColor(image_inv, cv.COLOR_GRAY2BGR)
        image = cv.bitwise_and(image, image_inv)
        image = cv.bitwise_or(image, image_canvas)
        # print(frame.shape[0])
        cv.imshow('Virtual Painter', image)
        # cv.imshow('image canvas', image_canvas)

        if cv.waitKey(10) & 0xFF == ord('q'):
            break

capture.release()
cv.destroyAllWindows()
