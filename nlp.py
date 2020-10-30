#!/usr/bin/env python
# coding: utf-8

# In[ ]:
# from stt import stt

from Recode import recode
from stt import stt
from TTS import tts_
import sys

# !pip install konlpy

def nlp(empid, name, menu, breaker=0):
    import pandas as pd
    import pymysql
    from konlpy.tag import Hannanum
    import pyaudio



    # from TTS import tts_
    # from Recode import recode
    # from main import play_song
    g = 0
    kor_to_num = {
        '한': 1,
        '두': 2,
        '세': 3,
        '네': 4,
        '하나': 1,
        '둘': 2,
        '셋': 3,
        '넷': 4,
        '다섯': 5,
        '여섯': 6,
        '일곱': 7,
        '여덟': 8,
        '아홉': 9,
        '열': 10,
        '한개': 1,
        '두개': 2,
        '세개': 3,
        '네개': 4,
        '다섯개': 5,
        '여섯개': 6,
        '일곱개': 7,
        '여덟개': 8,
        '아홉개': 9,
        '열개': 10,
        '1잔': 1,
        '한잔': 1,
        '2잔': 2,
        '두잔': 2,
        '3잔': 3,
        '세잔': 3,
        '4잔': 4,
        '네잔': 4,
        '5잔': 5,
        '다섯잔': 5,
        '6잔': 6,
        '여섯잔': 6,
        '7잔': 7,
        '일곱잔': 7,
        '8잔': 8,
        '여덟잔': 8,
        '9잔': 9,
        '아홉잔': 9,
        '10잔': 10,
        '열잔': 10,

    }

    num_to_kor = {
        '1': '한',
        '2': '두',
        '3': '세',
        '4': '네',
        '5': '다섯',
        '6': '여섯',
        '7': '일곱',
        '8': '여덟',
        '9': '아홉',
        '10': '열',
    }

    hot_or_ice = {

        '따듯한': '따뜻한',
        '핫': '따뜻한',
        '아이스': '시원',
        '뜨거운': '따뜻한',
        '차가운': '시원',
        '콜드': '시원',

    }

    recode(f'어서오세요 {name}님 반갑습니다  주문하실 음료와 수량을 말씀해주세요',g,3)
    g+=1
    txt = stt()
    #txt = '아이스 아메리카노 하나 아이스 라떼 하나 주세요'

    # txt = '아이스 아메리카노 주세요'
    # t = input(f"어서오세요 {name}님 반갑습니다\n")
    txt = txt.split()



    for i in range(len(txt) - 1):

        if txt[i] in hot_or_ice.keys():
            txt[i] = hot_or_ice.get(txt[i])

    de = []
    for i in range(len(txt)):
        if txt[i] == '라떼':
            txt[i] = '라테'
        elif txt[i] == '거' or txt[i] == '것' or txt[i] == '겉':
            de.append(i)

    if len(de) > 0:
        for j in range(len(de)):
            txt.remove(txt[de[j]])

    txt = " ".join(txt)

    hannanum = Hannanum()

    ##
    n = 0
    ind = []

    a = hannanum.nouns(txt)

    a = " ".join(a)

    a = a.replace("따뜻한 아메리카노", "따뜻한아메리카노")
    a = a.replace("아메리카노 따뜻한", "따뜻한아메리카노")
    a = a.replace("아메리카노 시원", "시원아메리카노")
    a = a.replace("시원 아메리카노", "시원아메리카노")
    a = a.replace("라테 따뜻한", "따뜻한라테")
    a = a.replace("따뜻한 라테", "따뜻한라테")
    a = a.replace("라테 시원", "시원라테")
    a = a.replace("시원 라테", "시원라테")
    a = a.replace("카라멜마끼아또 따뜻한", "따뜻한카라멜마끼아또")
    a = a.replace("카라멜마끼아또 시원", "시원카라멜마끼아또")
    a = a.replace("시원 카라멜마끼아또", "시원카라멜마끼아또")

    back = 0

    a = a.replace('랑', "")
    a = a.replace('이랑', "")
    a = a.replace("하고", "")
    a = a.replace('와', "")
    a = a.replace('과', "")
    a = a.replace('은', "")
    a = a.replace('는', "")
    a = a.replace('이요', "")

    a = a.split()

    if a[-1:][0] != '주세요':
        a.append('주세요')

    for i in a:
        # print("a = ", a)
        if i in menu:
            # print("menu= ", menu)
            back += 1

    # print("back = ", back)
    # breaker = 4
    if back == 0:
        print("breaker = ", breaker)
        if breaker < 3:

            print(breaker)
            recode('다시 말씀해주세요', g)
            g += 1
            txt = stt()
            # nlp(empid, name, menu, breaker + 1)


        else:

            warnning = '입력 실패로 종료됩니다'
            recode(warnning, g)
            g += 1

    else:

        y = []

        for i in range(len(a) - 1):

            if a[i] in menu.keys() and a[i + 1] not in kor_to_num.keys():
                ind.append(i)

        if len(ind) > 0:

            for i in range(len(ind)):
                a.insert(ind[i] + i + 1, 1)
                a[ind[i] + i + 1] = '1잔'

        kill = 0

        for i in range(len(a) - 1):

            if len(a) <= 2:
                warnning = '다시 말씀해주세요'
                recode(warnning, g)
                g += 1

                kill += 1

                break

            if i % 2 == 0 and a[i] not in menu.keys():

                warnning = '다시 말씀해주세요'
                recode(warnning, g)
                g += 1

                kill += 1

                break






            else:

                n = n + 1

        if kill > 0:
            nlp(empid, name, menu, breaker)

        if n == len(a) - 1:

            for i in range(len(a) - 1):
                y.append(a[i])
                y[i] = y[i].replace("시원아메리카노", "시원한 아메리카노")
                y[i] = y[i].replace("시원라테", "시원한 라떼")
                y[i] = y[i].replace("시원카라멜마끼아또", "시원한 카라멜마끼아또")
                y[i] = y[i].replace("따뜻한아메리카노", "따뜻한 아메리카노")
                y[i] = y[i].replace("따뜻한라테", "따뜻한 라떼")
                y[i] = y[i].replace("따뜻한카라멜마끼아또", "따뜻한 카라멜마끼아또")

            y = " ".join(y)

            recode('{} 주문하시겠습니까?'.format(y), g, 2)
            print('주문하시겠습니까?')
            g += 1
            Q = stt()





        else:

            menucheck = []
            for i in range(len(a) - 1):
                y.append(a[i])
                y[i] = y[i].replace("시원아메리카노", "시원한 아메리카노")
                y[i] = y[i].replace("시원라테", "시원한 라떼")
                y[i] = y[i].replace("시원카라멜마끼아또", "시원한 카라멜마끼아또")
                y[i] = y[i].replace("따뜻한아메리카노", "따뜻한 아메리카노")
                y[i] = y[i].replace("따뜻한라테", "따뜻한 라떼")
                y[i] = y[i].replace("따뜻한카라멜마끼아또", "따뜻한 카라멜마끼아또")

                menucheck.append(y[i])

            y = " ".join(y)

            recode('{}주문하시겠습니까?'.format(menucheck), g, 3)
            g += 1
            Q = stt()

        b = ''
        m = []
        amt = []
        cost = []
        total2 = 0

        total3 = []

        if Q == '':
            tts_('다시 말씁해주세요.', g) ######################
            g += 1

        elif Q.split()[0] == '다시':

            Q = recode('주문하실 음료와 수량을 다시 말씀해주세요', g)
            t = stt()
            # nlp(empid, name, menu, breaker)

        elif Q == '네' or '주세요':

            for i in range(len(a) - 1):

                if i % 2 == 0:

                    p = menu.get(a[i])

                    w = 0

                    a[i] = a[i].replace("시원아메리카노", "시원한 아메리카노")
                    a[i] = a[i].replace("시원라테", "시원한 라떼")
                    a[i] = a[i].replace("시원카라멜마끼아또", "시원한 카라멜마끼아또")
                    a[i] = a[i].replace("따뜻한아메리카노", "따뜻한 아메리카노")
                    a[i] = a[i].replace("따뜻한라테", "따뜻한 라떼")
                    a[i] = a[i].replace("따뜻한카라멜마끼아또", "따뜻한 카라멜마끼아또")

                    m.append(a[i])

                else:
                    w = num_to_kor.get(a[i])
                    w = kor_to_num.get(a[i])
                    amt.append(w)

                total = p * w

                if total != 0:
                    cost.append(total)

                total2 = total2 + total

                if i == (len(a) - 2):

                    for i in range(len(m)):
                        for j in range(1, 11):
                            if amt[i] == j:
                                b = str(amt[i]).replace(str(j), num_to_kor.get(str(j)))

                        total3.append(m[i] + b + '잔')
            total3.append(str(total2) + "원 입니다.")  ###################
            total3 = " ".join(total3)
            tts_(total3, g)
            g += 1

            for i in range(len(m)):

                con = pymysql.connect(host='101.101.218.133', port=3306, user='root', password='1234', db='SBA_3',
                                      charset='utf8')

                cursor = con.cursor()
                sql = 'INSERT INTO SBA_3.new_table(member_id,hot_or_ice, menu_name, amount,cost) VALUES("%s","%s","%s",%d,%d);' % (
                empid, m[i].split()[0], m[i].split()[1], kor_to_num.get(b), cost[i])
                cursor.execute(sql)
                con.commit()


            # break
            sys.exit()

        else:

            tts_('종료', g) ######################
            g += 1