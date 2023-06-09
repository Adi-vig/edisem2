import cv2
import pickle
import cvzone
import numpy as np
import requests
# import qrgen

# Video feed
cap = cv2.VideoCapture(1)

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

width, height =150, 280

def checkParkingSpace(imgPro):
    spaceCounter = 0

    for pos in posList:
        x, y = pos

        imgCrop = imgPro[y:y + height, x:x + width]
        # cv2.imshow(str(x * y), imgCrop)
        count = cv2.countNonZero(imgCrop)


        if count < 2500:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(img, f'FREE: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(0,200,0))
    
counter=0
while True:

    # if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
    #     cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    
    dim = (1100, 720)
    # resize image
    img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    imG = cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE)
    
    # cv2.imshow("Real time feed", img)


    
    
    
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    
    
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    
    kernel = np.ones((3, 3), np.uint8)
    
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Parking Lot", img)
    
    
    
    
    
    
    
    # with open('img', 'wb') as f:
    #     pickle.dump(img, f)
    
    
    
    if counter==40:
        _,imdata = cv2.imencode('.JPG', img)

        print('.', end='', flush=True)

        requests.put('http://127.0.0.1:5000/upload', data=imdata.tobytes())
        
        # 40ms = 25 frames per second (1000ms/40ms), 
        # 1000ms = 1 frame per second (1000ms/1000ms)
        # but this will work only when `imshow()` is used.
        # Without `imshow()` it will need `time.sleep(0.04)` or `time.sleep(1)`

        if cv2.waitKey(10) == 27:  # 40ms = 25 frames per second (1000ms/40ms) 
            break
        counter=0
        
    counter+=1
    
    
    
    
    
    
    
    
    
    
    
    # cv2.imshow("ImageBlur", imgBlur)
    
    # cv2.imshow("gray", imgGray)
    
    # cv2.imshow("binary", imgThreshold)
    
    # cv2.imshow("medianblur", imgMedian)
    
    # cv2.imshow("Dialte", imgDilate)
    
    cv2.waitKey(20)