from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app

from app.module import dbModule

test = Blueprint('test', __name__, url_prefix='/test')


@test.route('/', methods=['GET'])
def index():
    return render_template('/test/test.html',
                           result=None,
                           resultData=None,
                           resultUPDATE=None)

@test.route('/insert', methods=['GET'])
def insert():
    db_class = dbModule.database()

    sql = "INSER INTO test_db.price(price_id) \
          VALUES(%d)" % ('12')
    db_class.execute(sql)
    db_class.commit()

    return render_template('test/test.html',
                           result='insert is done!',
                           resultData=None,
                           resultUPDATE=None)

@test.route('/select', methods=['GET'])
def select():
    db_class = dbModule.Database()

    sql = "SELECT * FROM price"
    row = db_class.executeAll(sql)
    print(row)

    return render_template('/test/test.html',
                           result=None,
                           resultData=row[0],
                           resultUPDATE=None)


@test.route('/update', methods=['GET'])
def update():
    db_class = dbModule.Database()

    sql = "UPDATE test_db.price \
                SET price='%s' \
                WHERE price_id='11'" % ('1500')
    db_class.execute(sql)
    db_class.commit()

    sql = "SELECT price_id, size, price_name, price, classification \
                FROM test_db.price"
    row = db_class.executeAll(sql)

    return render_template('/test/test.html',
                           result=None,
                           resultData=None,
                           resultUPDATE=row[0])


