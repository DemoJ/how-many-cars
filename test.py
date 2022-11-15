import cv2

# ip摄像机地址url
# url = r"rtsp://admin:xxxxxx@192.168.1.75:554/11"
# cap = cv2.VideoCapture(url)

# 访问摄像机需要的信息
ip = '192.168.1.9'
user = 'admin'
password = 'admin' # 访问摄像机需要密码
# 抓取视频流
cap = cv2.VideoCapture("rtsp://" + user + ":" + password + "@" + ip + ":8554/live")  # 端口port通常是固定的554
ret, frame = cap.read()
cv2.namedWindow(ip, 0)
cv2.resizeWindow(ip, 500, 300)
# 使用，展示
while ret:
    ret, frame = cap.read()
    cv2.imshow(ip, frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# 退出时释放窗口和内存
cv2.destroyAllWindows()
cap.release()