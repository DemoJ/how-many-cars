import cv2

url = "rtsp://admin:admin123@192.168.1.6:8554/live"
# 加载视频文件
video = cv2.VideoCapture(url)

# 获取第一帧画面
ret, frame = video.read()

# 获取画面的高度和宽度
height, width = frame.shape[:2]

# 创建背景减除器对象
bg_subtractor = cv2.createBackgroundSubtractorMOG2()

count1 = 0
car_flow = 0
MIN_CONTOUR_AREA = 1000

while True:
    count2 = 0
    # 读取下一帧画面
    ret, frame = video.read()

    # 如果没有更多帧画面，退出循环
    if not ret:
        break

    # 运用背景减除器处理当前帧画面
    mask = bg_subtractor.apply(frame)

    # 腐蚀处理得到的掩模
    mask = cv2.erode(mask, None, iterations=2)

    # 对掩模进行阈值化处理
    _, thresh = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)

    # 检测图像中的轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 循环遍历所有轮廓
    for contour in contours:
        # 计算轮廓的边界框
        (x, y, w, h) = cv2.boundingRect(contour)

        # 如果边界框的面积超过了阈值，则表示找到了运动的车辆
        if cv2.contourArea(contour) > MIN_CONTOUR_AREA:
            # 在当前帧画面中绘制红色矩形框，框住运动的车辆
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            count2 += 1

    car_diff = count2 - count1
    if car_diff > 0:
        car_flow = car_flow + car_diff
    count1 = count2
    # 在当前帧画面中绘制
    cv2.putText(frame, f"Flow: {car_flow}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # 展示图像
    cv2.imshow("Camera", frame)

    # 等待用户按下q键，退出循环
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()