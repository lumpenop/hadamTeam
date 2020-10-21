import cv2
from flask import Flask

app = Flask(__name__)

host_addr = "0.0.0.0"
port_num = "8080"

@app.route("/")
def info():
    return "<h1>Hello World!</h1>"

@app.route("/hello")
def hello():
    return "<h1>JaeSung Fighting</h1>"


if __name__ == "__main__":
    app.run(host=host_addr, port=port_num)