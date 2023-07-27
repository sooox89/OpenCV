import cv2
import numpy as np
import torch
import ultralytics
import supervision as sv
from ultralytics import YOLO

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#각 박스에 위치를 리스트에 넣기
def paintPoints(img, boxes, myColors):
    for i in range(len(boxes)):
        newPoints = []
        box = boxes[i]
        myColor = myColors[i]
        x1,y1,x2,y2 = box.xyxy[0][0],box.xyxy[0][1],box.xyxy[0][2],box.xyxy[0][3]
        target_x = (x1+x2)/2
        target_y = y1
        newPoints.append([target_x, target_y,i])
    return newPoints
    # for point in newPoints:
    #     cv2.circle(img, (int(point[0]), int(point[1])), 10,myColor, cv2.FILLED)

#그 리스트에 있는 점들을 그리기.
def drawOnCanvas(img, myPoints, myColors):
    for point in myPoints:
        cv2.circle(img, (int(point[0]), int(point[1])), 5, myColors[point[2]], cv2.FILLED)

    # 색깔 설정, 객체 3명이라고 한정.
    myColors = [[51, 153, 255], [255, 0, 0], [0, 255, 0], [0, 0, 255]]
    myPoints = []
    # 학습된 모델 가져오기
    model = YOLO("/Users/gimgeon-yu/Desktop/openCV/724.pt")

    # 영상 가져오기.
    cap = cv2.VideoCapture("/Users/gimgeon-yu/Desktop/openCV/friend_group_1.mp4")  # 이 부분은 각자 수정하세요.
    # cap = cv2.VideoCapture(1)

    # 박스 환경설정
    box_annotator = sv.BoxAnnotator(
        thickness=2,
        text_thickness=2,
        text_scale=1
    )

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        results = model.predict(img)[0]

        try:
            # results = model.track(source="https://youtu.be/Zgi9g1ksQHc", conf=0.3, iou=0.5, show=True)
            boxes = results.boxes
            print("id : ", boxes.id)
            points = paintPoints(img, boxes, myColors)
            for point in points:
                myPoints.append(point)
            drawOnCanvas(img, myPoints, myColors)


        except:
            print("flag2")
            pass

        detections = sv.Detections.from_yolov8(results)
        img = box_annotator.annotate(scene=img, detections=detections)
        cv2.imshow("YoLO Test", img)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

