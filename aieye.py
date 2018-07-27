# -*- coding: utf-8 -*-
import cv2
import json
import subprocess
from datetime import datetime
from time import sleep
from googletrans import Translator

textleft = "左"
textright = "右"
i = 0

def shellCommand(command):
    proc = subprocess.Popen(
            command,
            shell  = True,
            stdin  = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE)
    return proc.communicate()

def jtalk(t):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    c = subprocess.Popen(cmd,stdin=subprocess.PIPE)
    c.stdin.write(bytes(t, 'utf-8'))
    c.stdin.close()
    c.wait()
    aplay = ['aplay','-q','open_jtalk.wav']
    wr = subprocess.Popen(aplay)

#def say_datetime():
#    d = datetime.now()
#    text = '%s月%s日、%s時%s分%s秒、ABC' % (d.month, d.day, d.hour, d.minute, d.second)
#    jtalk(text)

def transe(sentence):
    translator = Translator()
    translated = translator.translate(sentence,src='en' ,dest='ja')
    print(translated.text)
    #print(translated)
    jtalk(translated.text)

def shoot():
    takepic = shellCommand("raspistill -o origin.jpg -w 1344 -h 672")
    print("taked picture")
    seppalate = divide()

def divide():
    img = cv2.imread("origin.jpg")
    height, width, channels = img.shape
    left = img[0:height, 0:width//2]
    left = cv2.resize(left, (224, 224))
    cv2.imwrite("left.jpg", left)
    right = img[0:height, width//2:width]
    cv2.imwrite("right.jpg", right)
    print("diveded")
    search = recognition()
    return left, right

def recognition():
    analyseleft = shellCommand("python3 /home/pi/monotone/Raspberry_Pi_3_Image_Classification/GoogleNet/google_net_raspi.py --image /var/isaax/project/left.jpg" )
    #analyseleft = shellCommand("python3 /home/pi//MonoTone/monotone/Raspberry_Pi_3_Image_Classification/GoogleNet/google_net_raspi.py --image /home/pi/MonoTone/left.jpg" )
    analyseright = shellCommand("python3 /home/pi/monotone/Raspberry_Pi_3_Image_Classification/GoogleNet/google_net_raspi.py --image /var/isaax/project/right.jpg" )
    leftdata = analyseleft[0].decode("utf-8").split("\n")
    rightdata = analyseright[0].decode("utf-8").split("\n")
    print(leftdata)
    print(rightdata)
    leftdetections = leftdata[:2]#最も可能性の高い2要素を取り出し

    sleep(1)
    jtalk(textleft)
    for ldetection in leftdetections:
        print("left")
        ldetection = json.loads(ldetection)
        print(ldetection["class"])
        transe(ldetection["class"])
        print(ldetection["score"])


    rightdetections = rightdata[:2]#最も可能性の高い2要素を取り出し
    sleep(1)
    jtalk(textright)
    for rdetection in rightdetections:
        print("right")
        rdetection = json.loads(rdetection)
        print(rdetection["class"])
        transe(rdetection["class"])
        print(rdetection["score"])


    # examples output: ['wardrobe,0.06655291467905045', 'stretcher,0.05793076753616333', ....]
    # results = analyseleft[0].decode("utf-8").split("\n")
    # print(results[:-3])




if __name__ == '__main__':
    while True:
        print("__loopstarted__")
        print("[{0}]times is ok".format(i))
        shoot()
        i = i + 1
        sleep(1)
