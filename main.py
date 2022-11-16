import cv2
import numpy as np
from tracker import EuclideanDistTracker

# 访问摄像机需要的信息
ip = '192.168.1.10'
user = 'admin'
password = 'admin'  # 访问摄像机需要密码

tracker = EuclideanDistTracker()
cap = cv2.VideoCapture("rtsp://" + user + ":" + password + "@" + ip + ":8554/live")  # 抓取视频流端口,port通常是固定的554
ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    # ret, frame = cap.read()
    diff = cv2.absdiff(frame1, frame2)
    # this method is used to find the difference bw two  frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # here i would add the region of interest to count the single lane cars
    height, width = blur.shape
    print(height, width)
    # thresh_value = cv2.getTrackbarPos('thresh', 'trackbar')
    _, threshold = cv2.threshold(blur, 23, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(threshold, (1, 1), iterations=1)
    contours, _, = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    detections = []
    # DRAWING RECTANGLE BOX (Bounding Box)
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 300:
            continue
        detections.append([x, y, w, h])
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x, y, w, h, id = box_id
        cv2.putText(frame1, str(id), (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('frame', frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    key = cv2.waitKey(30)
    if key == ord('q'):
        break
cv2.destroyAllWindows()
