#!/usr/bin/env python
# coding: utf-8
def stt():
 import sys
 import requests
 client_id = "109vqxa5ud"
 client_secret = "z5s6MESERmZmNqhCv3TyXkudZfEfFpzPOrI2y1PB"
 lang = "Kor" # 언어 코드 ( Kor, Jpn, Eng, Chn )
 url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?lang=" + lang
 data = open('./file.wav', 'rb')
 headers = {
     "X-NCP-APIGW-API-KEY-ID": client_id,
     "X-NCP-APIGW-API-KEY": client_secret,
     "Content-Type": "application/octet-stream"
 }
 response = requests.post(url,  data=data, headers=headers)
 rescode = response.status_code
 if(rescode == 200):
     print (response.text)
 else:
     print("Error : " + response.text)
     
 return response.text[9:-2]

