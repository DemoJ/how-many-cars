import numpy as np
import cv2 as cv
count1 = 0
count2 = 0
cv.namedWindow("frame",0);
cv.resizeWindow("frame", 216*2, 384*2);
vc = cv.VideoCapture(r"Z:\files\1111.mp4")
writer1 = cv.VideoWriter(r'Z:\files\myresult.avi', cv.VideoWriter_fourcc(*'DIVX'), 30,
                         (1920, 1080), True)#输出图像
BS = cv.createBackgroundSubtractorMOG2(detectShadows=False)
while (vc.isOpened()):
    ret, frame = vc.read()
    # ROI = frame[200:900,300,900]
    # cv.line(frame, (0,600), (19200,600), (0,255,0), 2, 4)
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    # ret,Binary = cv.threshold(gary,50,255,cv.THRESH_BINARY)
    fgmask = BS.apply(gray)
    image = cv.medianBlur(fgmask,5)
    # cv.imshow("BS",fgmask)
    element = cv.getStructuringElement(cv.MORPH_RECT,(1, 1));
    element2 = cv.getStructuringElement(cv.MORPH_RECT, (1, 1));
    image2 = cv.morphologyEx(image, cv.MORPH_OPEN,element);
    image3 = cv.dilate(image2, element2)
    # cv.imshow('frame', image3)
    contours, hierarchy = cv.findContours(image3, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for cnt in contours:
        x, y, w, h = cv.boundingRect(cnt)
        # if y+h == 600:
        #     count1+=1
        if cv.contourArea(cnt) < 10000 or w < 100 or h < 100 :
            continue
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        writer1.write(frame)#输出图形，可以看到掉帧现象极为明显
        # cv.putText(frame,"Count:"+str(count1),(500,500),cv.FONT_HERSHEY_COMPLEX,2,(255,0,0))
    # frame=cv.flip(frame, -1)
    cv.imshow("frame",frame)
    k = cv.waitKey(int(100/6)) & 0xff
    if k == 27:
        break
vc.release()
cv.destroyAllWindows()

