import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript


vstrl = ['set','volume','output','volume','0']
#print(list(vStr.split(" ")))



#set volume output volume 100
###########################
#wCam, hCam = 640, 480   # Width and Height of the Camera

###########################



cap = cv2.VideoCapture(0)
#cap.set(3, wCam)
#cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

volBar = 400
volPer = 0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw= False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        x1,y1 = lmList[4][1], lmList[4][2]
        x2,y2 = lmList[8][1], lmList[8][2]
        cx,cy = (x1+x2)//2, (y1+y2)//2

        cv2.circle(img,(x1,y1), 8, (255,0,255), cv2.FILLED)
        cv2.circle(img,(x2,y2), 8, (255, 0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2), (255,0,255),3)

        cv2.circle(img, (cx,cy),8, (255, 0, 255),cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        #print(length)

        #Hand range 70 - 300

        vol = np.interp(length,[50,300],[0,100])
        volBar = np.interp(length, [70, 250], [400, 150])
        volPer = np.interp(length, [70, 250], [0, 100])

        vstrl[4] = str(vol)
        vStr = ' '.join(map(str,vstrl))
        #print(vStr)
        osascript.run(vStr)
        code, out, err = osascript.run("output volume of (get volume settings)")
        #print(out)



        if(length<70):
            cv2.circle(img, (cx,cy),8, (0,255,0),cv2.FILLED)

    cv2.rectangle(img, (50,150), (85,400), (0,255,0),3)
    cv2.rectangle(img, (50,int(volBar)),(85, 400),(0,255,0),cv2.FILLED)
    cv2.putText(img, str(int(volPer)), (40,450), cv2.FONT_ITALIC, 1, (0,255, 0), 3)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_ITALIC,1,(255,0,0),3)

    cv2.imshow("Img",img)
    cv2.waitKey(1)

    