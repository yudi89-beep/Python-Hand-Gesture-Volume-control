import cv2                  # Open CV - Python
import mediapipe as mp      # google ML
import time                 # to check the Frame Rate
cap = cv2.VideoCapture(0)   # opens Webcam (0 : default inbuilt WebCam) Through The open CV package

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0

while True:
    success, img = cap.read()

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)            #displays the position of the detection


    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h, w, c = img.shape               # height width and channle of the image
                cx, cy = int(lm.x*w), int(lm.y*h) # Finds the position of the center X and Y
                print(id, cx,cy)                      # Prints the position From the center

                #if id==8:
                    #cv2.circle(img, (cx,cy), 15 , (255,0,0),cv2.FILLED)     # id 8 index finger

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime



    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_ITALIC,3,(255,0,255),3)


    cv2.imshow('Image', img)                        # Opens Webcam Window
    cv2.waitKey(1)
