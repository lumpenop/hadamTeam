
client_id = "109vqxa5ud"
client_secret = "z5s6MESERmZmNqhCv3TyXkudZfEfFpzPOrI2y1PB"

import urllib.request

import pygame

def tts_(res, num):
    print("tts")
    encText = urllib.parse.quote(res)
    data = "speaker=nara&volume=0&speed=-1&pitch=0&format=mp3&text=" + encText;
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if (rescode == 200):
        print("TTS mp3 저장")
        response_body = response.read()
        with open('./play_audio{}.mp3'.format(num), 'wb') as f:
            f.write(response_body)
            f.close()
        pygame.mixer.init()
        pygame.mixer.music.load("./play_audio{}.mp3".format(num))

        pygame.mixer.music.play()

        clock = pygame.time.Clock()
        while pygame.mixer.music.get_busy():
            clock.tick(1000)

        pygame.mixer.quit()



    else:
        print("Error Code:" + rescode)

