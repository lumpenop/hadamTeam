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

import numpy as np
import time

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    def __init__(self, fn):
        super(Worker, self).__init__()

        self.fn = fn
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        try:
            result = self.fn()
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

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
            #print(result)
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

        f = partial(self.send_json, payload, 'http://localhost:1234/register_face', self.register_response_queue)
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
        f = partial(self.send_json, payload, 'http://localhost:1234/transfer_image', self.recognize_response_queue)
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
        self.mutex.unlock()

        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
        if not self.timer:
            self.timer = QTimer()
            self.timer.setInterval(1000)
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