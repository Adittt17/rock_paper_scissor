import streamlit as st
import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
import random
import time

st.title("Rock-Paper-Scissors with Hand Detection")

# Initialize HandDetector once
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Session state to keep variables across reruns
if 'scores' not in st.session_state:
    st.session_state.scores = [0, 0]  # AI, Player

if 'stateResult' not in st.session_state:
    st.session_state.stateResult = False

if 'startGame' not in st.session_state:
    st.session_state.startGame = False

if 'initialTime' not in st.session_state:
    st.session_state.initialTime = 0

if 'imgAI' not in st.session_state:
    st.session_state.imgAI = None

# Streamlit webcam input
img_file_buffer = st.camera_input("Show your hand")

if img_file_buffer is not None:
    # Read image from camera
    bytes_data = img_file_buffer.getvalue()
    np_img = np.frombuffer(bytes_data, np.uint8)
    img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize and crop like your original code
    imgScaled = cv2.resize(img, (0, 0), fx=0.875, fy=0.875)
    imgScaled = imgScaled[:, 80:480]

    hands, img_processed = detector.findHands(imgScaled)

    # Create blank background image (you can load BG.png here if you upload it as resource)
    imgBG = np.zeros((720, 1280, 3), np.uint8)
    imgBG[:] = (50, 50, 50)  # dark background

    if st.session_state.startGame:
        if not st.session_state.stateResult:
            if st.session_state.initialTime == 0:
                st.session_state.initialTime = time.time()

            timer = time.time() - st.session_state.initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                st.session_state.stateResult = True

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)

                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1  # Rock
                    elif fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2  # Paper
                    elif fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3  # Scissors

                    randomNumber = random.randint(1, 3)
                    # Load AI hand image, upload images 1.png, 2.png, 3.png to Streamlit app folder
                    imgAI = cv2.imread(f'dashboard/{randomNumber}.png', cv2.IMREAD_UNCHANGED)

                    if imgAI is not None:
                        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
                        st.session_state.imgAI = imgAI

                    # Score calculation
                    if (playerMove == 1 and randomNumber == 3) or \
                       (playerMove == 2 and randomNumber == 1) or \
                       (playerMove == 3 and randomNumber == 2):
                        st.session_state.scores[1] += 1

                    if (playerMove == 3 and randomNumber == 1) or \
                       (playerMove == 1 and randomNumber == 2) or \
                       (playerMove == 2 and randomNumber == 3):
                        st.session_state.scores[0] += 1

        imgBG[234:654, 795:1195] = imgScaled

        if st.session_state.stateResult and st.session_state.imgAI is not None:
            imgBG = cvzone.overlayPNG(imgBG, st.session_state.imgAI, (149, 310))

    else:
        imgBG[234:654, 795:1195] = imgScaled

    # Display scores
    cv2.putText(imgBG, str(st.session_state.scores[0]), (410, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    cv2.putText(imgBG, str(st.session_state.scores[1]), (1112, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)

    st.image(imgBG, channels="BGR")

# Buttons to control game state
if st.button("Start Game"):
    st.session_state.startGame = True
    st.session_state.initialTime = 0
    st.session_state.stateResult = False

if st.button("Reset Scores"):
    st.session_state.scores = [0, 0]
    st.session_state.startGame = False
    st.session_state.stateResult = False
    st.session_state.initialTime = 0
    st.session_state.imgAI = None
