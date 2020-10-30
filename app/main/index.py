from flask import Blueprint, request, Response, render_template, flash, redirect, url_for
from flask import current_app as app
from app.module.real_time_face_detection import gen
from app.module import dbModule
from client import QApplication, App
import sys

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/main', methods=['GET'])
def index():
    db_class = dbModule.Database()

    sql = "SELECT * FROM menu"
    row = db_class.executeAll(sql)
    print(row)
    return render_template('/main/index.html', resultData=row)


@main.route('/video_feed')
def video_feed():
    # for x in gen():
    #     print(x)
    # print("gen = ", str(gen()))
    # return Response(
    #     gen(),
    #     mimetype='multipart/x-mixed-replace; boundary=frame'
    # )

    app = QApplication(sys.argv)
    a = App()
    a.show()
    # sys.exit(app.exec_())
    app.exec_()

@main.route("/save", methods =["POST", "GET"])
def save_audio():
    from client import App
    print("save_audio")
    from nlp import nlp
    if request.method == "POST":
        # print("empid: ", empid)
        empid = "sba_202020"
        name = "김승원"
        menu = {'따뜻한아메리카노': 1000, '시원아메리카노': 1000, '따뜻한라테': 2000, '시원라테': 2000,
                '따뜻한카라멜마끼아또': 2000, '시원카라멜마키아또': 2000, '레몬에이드': 2000}
        print("empid = ", empid, ", name = ", name, " , menu = ", menu)
        nlp(empid, name, menu)
    return redirect('http://localhost:8181/main')