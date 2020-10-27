import numpy as np
import cv2
import io
import time

xml = '../data/haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(xml)

cap = cv2.VideoCapture(0) # 노트북 웹캠을 카메라로 사용
cap.set(3,640) # 너비
cap.set(4,480) # 높이
count = 0
result = ''
num = 0

def gen():
    global result, count, num

    while(True):
        ret, frame = cap.read()
        # frame = cv2.flip(frame, 1) # 좌우 대칭
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # print("ret = ", ret)
        # fps = cap.get(cv2.CAP_PROP_FPS)
        # print('fps = ', fps)
        # faces = face_cascade.detectMultiScale(gray,1.05, 5)
        # print("Number of faces detected: " + str(len(faces)))

        # if len(faces):
        #     for (x,y,w,h) in faces:
        #         cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

        encode_return_code, image_buffer = cv2.imencode('.jpg', frame)
        io_buf = io.BytesIO(image_buffer)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + io_buf.read() + b'\r\n')

        count += 1
        img = cv2.imdecode(image_buffer, cv2.IMREAD_COLOR)
        if count % 30 == 0:
            # if
            num += 1
            cv2.imwrite('test' + str(num) + '.jpg', img)

        print("count = ", count)
        # cv2.imwrite('test' + str(count) + '.jpg', img)

        # if int(fps) == 1:
        #     print(frame)


        if count == 91:
            print("%d frame: %s" % (count, frame))
            result = '12345'
            break

        # cv2.imshow('result', frame)
        #
        # k = cv2.waitKey(30) & 0xff
        # if k == 27: # Esc 키를 누르면 종료
        #     break

    return result

    cap.release()
    cv2.destroyAllWindows()



