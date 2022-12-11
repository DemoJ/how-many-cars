import cv2
import numpy as np

def get_count(frame,car_count):
# 进行图像处理
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 检测图像中的边缘
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # 检测图像中的形状
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历所有检测到的形状
    for c in contours:
        # 计算形状的面积
        area = cv2.contourArea(c)

        # 计算形状的周长
        perimeter = cv2.arcLength(c, True)

        # 计算形状的长宽比
        ratio = perimeter / (2 * np.sqrt(area))

        # 如果形状的面积大于1000且长宽比在1.5到3之间，判定为车辆
        if area > 1000 and 1.5 < ratio < 3:
            car_count += 1
    return  car_count

# 打开摄像头
camera = cv2.VideoCapture(r"Z:\files\1111.mp4")

car_flow = 0

# 读取第一帧图像
ret, frame1 = camera.read()

# 初始化第一帧图像中的车辆数量为0
car_count1 = 0

# 检测第一帧图像中的车辆
car_count1=get_count(frame1,car_count1)


# 设置循环条件，持续读取摄像头的帧
while True:
    ret, frame2 = camera.read()

    # 如果到达视频末尾，退出循环
    if not ret:
        break

    car_count2 = 0
    # 检测第二帧图像中的车辆
    car_count2=get_count(frame2,car_count2)

    # 计算两帧图像中车辆数的差值
    car_diff = car_count2 - car_count1
    if car_diff > 0:
        car_flow = car_flow+car_diff

    # 更新第一帧图像中的车辆数量为第二帧图像中的车辆数量
    car_count1 = car_count2

    cv2.putText(frame2, f"Flow: {car_flow}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 展示图像
    cv2.imshow("Camera", frame2)

    # 等待用户按下q键，退出循环
    key = cv2.waitKey(int(100/6))
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()