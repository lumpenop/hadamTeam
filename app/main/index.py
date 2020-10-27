from flask import Blueprint, request, Response, render_template, flash, redirect, url_for
from flask import current_app as app
from app.module.real_time_face_detection import gen

main = Blueprint('main', __name__, url_prefix='/')


@main.route('/main', methods=['GET'])
def index():
    testData = 'testData arry'
    return render_template('/main/index.html', testDataHtml=testData)


@main.route('/video_feed')
def video_feed():
    for x in gen():
        print(x)
    print("gen = ", str(gen()))
    return Response(
        gen(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

