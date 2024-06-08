import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

while True:
    success, img = cap.read()
    imgBG = cv2.imread("BG.png")

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw

    cv2.imshow("Image", img)
    cv2.imshow("BG", imgBG)
    cv2.imshow("Scaled", imgScaled)

    cv2.waitKey(1)
