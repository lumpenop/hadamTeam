from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout,QPushButton,QLineEdit
from PyQt5.QtGui import QPixmap
import sys
import cv2
import base64
import json
import requests
import traceback
from threading import Thread

from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread, QMutex, QObject, QRunnable, QThreadPool, QTimer
from functools import partial
from queue import Queue
from nlp import nlp
from app.module import dbModule

import numpy as np
import time

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class App(QWidget):
    def __init__(self):
        super().__init__()

        self.send_queue = Queue(maxsize=10)
        self.recognize_response_queue = Queue(maxsize=10)
        self.register_response_queue = Queue(maxsize=10)

        self.mutex = QMutex()
        self.cv_face_frame = None

        self.setWindowTitle("Haedam")
        self.disply_width = 640
        self.display_height = 480
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        self.textLabel = QLabel('Webcam')
        #self.face_recognize_button = QPushButton('face recognize', self)
        self.name_textbox = QLineEdit(self)

        self.register_face_button = QPushButton('register face', self)

        #self.face_recognize_button.clicked.connect(self.on_face_recognize_click)
        self.register_face_button.clicked.connect(self.on_register_face_click)
        self.transfer_image = None
        self.requesting = False
        self.box = None
        self.face_name = None
        faceName = self.face_name
        #self.threadpool = QThreadPool()

        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        #vbox.addWidget(self.face_recognize_button)
        vbox.addWidget(self.name_textbox)
        vbox.addWidget(self.register_face_button)

        self.setLayout(vbox)

        self.timer = None

        self.send_thread = Thread(target=self.send_request, args=(self.send_queue,))
        self.send_thread.start()

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    def send_request(self, q):
        while True:
            #print('send queue')
            f = q.get()
            if f is None:
                break
            f()


    def on_timer(self):
        #print('on timer')
        if self.register_response_queue.qsize():
            result = self.register_response_queue.get()
            # print("result: ", result)
        if self.recognize_response_queue.qsize():
            result = self.recognize_response_queue.get()

            if 'box' in result:
                self.mutex.lock()
                self.box = result['box']
                self.face_name = result['message']
                self.mutex.unlock()

        if self.send_queue.qsize() == 0:
            self.request_face_recognize()


    def encode_frame(self, image):
        #print(image)
        send_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        retval, buffer = cv2.imencode('.jpg', send_image)
        jpg_as_text = base64.b64encode(buffer)
        jpg_as_text = jpg_as_text.decode('utf-8')
        return jpg_as_text

    def send_json(self, data, url, response_queue):
        #print('send_json')
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers,
                                    data=json.dumps(data))
        response_queue.put(response.json())

    def request_face_register_click(self, name):
        self.mutex.lock()
        #print('test start')
        #print(self.cv_face_frame)
        if self.cv_face_frame is None:
            print('cv_face_frame is None')
            self.mutex.unlock()
            return None
        #print('transform face frame')
        self.transfer_image = self.cv_face_frame.copy() # frame = cv2.imread('b2.jpg')
        self.mutex.unlock()
        #print(self.transfer_image)
        image_data = self.encode_frame(self.transfer_image)
        print(name)
        payload = {}
        payload['frame'] = image_data
        payload['name'] = name

        f = partial(self.send_json, payload, 'http://101.101.218.133:1234/register_face', self.register_response_queue) #'http://localhost:1234/register_face'
        self.send_queue.put(f)

    def on_register_face_click(self):
        #if not self.requesting:
        name = self.name_textbox.text()
        #f = partial(self.request_face_register_click,name)
        self.requesting = True
        self.request_face_register_click(name)
        #worker = Worker(f)
        #worker.signals.result.connect(self.response_face_register)
        #self.threadpool.start(worker)


    def request_face_recognize(self):
        self.mutex.lock()
        if self.cv_face_frame is None:
            print('self.cv_face_frame is None')
            self.mutex.unlock()
            return
        self.transfer_image = self.cv_face_frame.copy() # frame = cv2.imread('b2.jpg')
        self.mutex.unlock()

        if self.transfer_image is None:
            print('self.transfer_image is None')
            return

        image_data = self.encode_frame(self.transfer_image)

        payload = {}
        payload['frame'] = image_data
        f = partial(self.send_json, payload, 'http://101.101.218.133:1234/transfer_image',  self.recognize_response_queue) #'http://localhost:1234/transfer_image'
        self.send_queue.put(f)

    def response_face_recognize(self, result):
        print(result)
        self.requesting = False

        if result is None:
            return

        if 'box' in result:
            self.mutex.lock()
            self.box = result['box']
            self.face_name = result['message']
            self.mutex.unlock()

    def closeEvent(self, event):
        self.thread.stop()
        self.send_queue.put(None)
        self.send_thread.join()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        self.mutex.lock()
        self.cv_face_frame = cv_img.copy()
        if self.box != None:
            cv2.rectangle(cv_img, (self.box[0], self.box[1]), (self.box[2], self.box[3]), (0,0,255), 3)
        if self.face_name:
            cv2.putText(cv_img, self.face_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                1,  (255, 0, 0), 2, cv2.LINE_AA)
            if self.face_name != 'Unknown':
                print("self.face_name = ", self.face_name)
                db_class = dbModule.Database()

                sql = "SELECT * FROM member \
                            where member_id = %s"
                row = db_class.executeOne(sql, self.face_name)
                print("row.member_name = ", row["member_name"])

                menu = {'따뜻한아메리카노': 1000, '시원아메리카노': 1000, '따뜻한라테': 2000, '시원라테': 2000,
                        '따뜻한카라멜마끼아또': 2000, '시원카라멜마키아또': 2000, '레몬에이드': 2000}
                nlp(row["member_id"], row["member_name"], menu)


        self.mutex.unlock()

        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        if not self.timer:
            self.timer = QTimer()
            self.timer.setInterval(50)
            self.timer.timeout.connect(self.on_timer)
            self.timer.start()


    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = App()
    a.show()
    sys.exit(app.exec_())