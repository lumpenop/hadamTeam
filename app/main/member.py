from flask import Blueprint, request, Response, render_template, flash, redirect, url_for
from flask import current_app as app
from werkzeug.utils import secure_filename
from app.module import dbModule
from datetime import datetime
from app.utils.util import allowed_file
import os

member = Blueprint('member', __name__, url_prefix='/')

UPLOAD_DIR = "app/static/images/"


# 맴버 등록페이지 HTML 렌더링
@member.route('/member_insertP', methods=['GET'])
def member_insertP():
    testData = 'upload page'
    return render_template('/main/member_insertP.html', testDataHtml=testData)


# 맴버 목록 페이지
@member.route('/member_list', methods=['GET'])
def member_list():
    db_class = dbModule.Database()

    sql = "SELECT * FROM member"
    row = db_class.executeAll(sql)
    # print(row)

    return render_template('/main/member_list.html',
                           result=None,
                           resultData=row,
                           resultUPDATE=None)

# 맴버 등록 처리
@member.route('/member_insert', methods = ['GET', 'POST'])
def member_insert():
    db_class = dbModule.Database()

    if request.method == 'POST':
        _memberId = request.form['memberId']
        _memberName = request.form['memberName']
        _age = request.form['age']
        _sex = request.form['sex']
        print("UPLOAD_DIR=", UPLOAD_DIR)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 저장할 경로 + 파일명
            path = os.path.join(UPLOAD_DIR, filename)
            print(path)
            file.save(path)
            # sql = "INSERT INTO files(file_id, file_name, file_path, create_date) \
            #                           VALUES(%s, %s, %s, %s)"
            # value = (_memberId, filename, path, datetime.now())
            # db_class.execute(sql, value)
            # db_class.commit()
            sql = "INSERT INTO member(member_id, member_name, age, sex, file_path, create_date) \
                              VALUES(%s, %s, %s, %s, %s, %s)"
            value = (_memberId, _memberName, _age, _sex, path, datetime.now())
            db_class.execute(sql, value)
            db_class.commit()
        else:
            print("확장자가 아닙니다.")

    return redirect('/member_list')


# 맴버 상세페이지 HTML 렌더링
@member.route('/member_detailView/<member_Id>', methods=['GET'])
def member_detailView(member_Id):
    db_class = dbModule.Database()

    sql = "SELECT * FROM member \
            where member_id = %s"
    row = db_class.executeOne(sql, member_Id)
    print(row)
    return render_template('/main/member_detailView.html',
                           result=None,
                           resultData=row,
                           resultUPDATE=None)


# 맴버 상세변경페이지 HTML 렌더링
@member.route('/member_updateView/<member_Id>', methods=['GET'])
def member_updateView(member_Id):
    db_class = dbModule.Database()

    sql = "SELECT * FROM member \
            where member_id = %s"
    row = db_class.executeOne(sql, member_Id)
    print(row)
    return render_template('/main/member_updateView.html',
                           result=None,
                           resultData=row,
                           resultUPDATE=None)


# 맴버 수정 처리
@member.route('/member_update', methods = ['GET', 'POST'])
def member_update():
    db_class = dbModule.Database()

    if request.method == 'POST':
        _memberId = request.form['memberId']
        _memberName = request.form['memberName']
        _age = request.form['age']
        _sex = request.form['sex']
        print("UPLOAD_DIR=", UPLOAD_DIR)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # 저장할 경로 + 파일명
            path = os.path.join(UPLOAD_DIR, filename)
            print(path)
            file.save(path)
            # sql = "INSERT INTO files(file_id, file_name, file_path, create_date) \
            #                           VALUES(%s, %s, %s, %s)"
            # value = (_memberId, filename, path, datetime.now())
            # db_class.execute(sql, value)
            # db_class.commit()
            sql = "UPDATE member \
                    SET member_name = %s, \
                        age = %s, \
                        sex = %s, \
                        file_path = %s, \
                        update_date = %s \
                        WHERE member_id = %s"
            value = (_memberName, _age, _sex, path, datetime.now(), _memberId)
            db_class.execute(sql, value)
            db_class.commit()

            sql = "SELECT * FROM member \
                        where member_id = %s"
            row = db_class.executeOne(sql, _memberId)
            print(row)

        else:
            print("확장자가 아닙니다.")

    return render_template('/main/member_updateView.html',
                           result=None,
                           resultData=row,
                           resultUPDATE=None)


# 맴버 삭제 HTML 렌더링
@member.route('/member_delete/<member_Id>', methods=['GET'])
def member_delete(member_Id):
    db_class = dbModule.Database()

    sql = "DELETE FROM member \
            where member_id = %s"
    db_class.execute(sql, member_Id)
    db_class.commit()

    return redirect('/member_list')



# 맴버 결제목록 페이지
@member.route('/member_paymentList', methods=['GET'])
def member_paymentList():
    db_class = dbModule.Database()

    sql = "SELECT a.*, ifnull(sum(b.cost), 0) as tt_cost FROM \
            member as a LEFT OUTER JOIN new_table as b  \
            ON a.member_id = b.member_id    \
            group by a.member_id"
    row = db_class.executeAll(sql)
    print(row)

    return render_template('/main/member_paymentList.html',
                           result=None,
                           resultData=row,
                           resultUPDATE=None)



# 맴버 결제상세페이지 HTML 렌더링
@member.route('/member_detailPaymentList/<member_Id>', methods=['GET'])
def member_detailPaymentList(member_Id):
    db_class = dbModule.Database()

    sql = "SELECT * FROM new_table \
            where member_id = %s"
    row = db_class.executeAll(sql, member_Id)
    print(row)
    return render_template('/main/member_detailPaymentList.html',
                           result=None,
                           resultData=row,
                           resultUPDATE=None)