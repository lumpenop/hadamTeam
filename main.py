import requests
import json
import cv2
import base64

img = cv2.imread('y2.jpg')

ret, encode_img = cv2.imencode('.jpg', img)
encode_bytes = encode_img.tobytes()
base64_encode = base64.b64encode(encode_bytes)
base64_string = base64_encode.decode('ascii')

url = "http://localhost:1234/transfer_image"
payload = {}
payload["frame"] = base64_string

headers = {'Content-Type': 'application/json'}
response = requests.request("POST", url, headers=headers, data=json.dumps(payload))


print(response.text)
