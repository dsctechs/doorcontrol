import RPi.GPIO as GPIO
import subprocess
import ffmpeg
import array
from datetime import datetime
from time import sleep


def StartCamera(cam):
    print('Door',camera[cam],' status = opened')
    print('Starting Camera %s'%cam)
    camstatus[cam] = 1

    if(cam == 0):
        filename = "/tmp/front-"+ datetime.now().strftime("%Y%m%d_%H%M%S") +".avi"
        stream1 = ffmpeg.input("/dev/video0", t='300', s='640x360')
        stream1 = ffmpeg.output(stream1,filename)
        return ffmpeg.run_async(stream1, quiet=True)
    else :
        filename = "/tmp/back-"+ datetime.now().strftime("%Y%m%d_%H%M%S") +".avi"
        stream2 = ffmpeg.input("/dev/video2", t='300', s='640x360')
        stream2 = ffmpeg.output(stream2,filename)
        return ffmpeg.run_async(stream2, quiet=True)

def StopCamera(cam, process):
    print('Door',camera[cam],' status = closed')
    print('Stopping Camera %s'%cam)
    camstatus[cam] = 0
    process.terminate()

doors = [11, 12]
camera = [1, 2]
camstatus = [0, 0]
camProcess = []

GPIO.setmode(GPIO.BOARD)
for door in doors:
	GPIO.setup(door, GPIO.IN)

while True:
    camindx = 0
    for door in doors:
        if(GPIO.input(door)):
            if(camstatus[camindx]==1):
                StopCamera(camindx, camProcess[camindx])
        else:
            if(camstatus[camindx]==0):
                camProcess.insert(camindx, StartCamera(camindx))

        camindx = camindx + 1
    sleep(1)

