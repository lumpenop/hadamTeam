from flask import Flask

app = Flask(__name__)

from app.main.index import main
from app.main.sql import sql
from app.main.member import member
from app.test.test import test as test

app.register_blueprint(main)
app.register_blueprint(sql)
app.register_blueprint(test)
app.register_blueprint(member)