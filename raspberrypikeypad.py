import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
import requests
import time
import sys
from telegram import Bot
import threading

# setting up and initializing the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(27, GPIO.IN)

# setting up the camera
my_camera = PiCamera()
my_camera.resolution = (1920, 1080) # the resolution can be changed

# telegram bot and its credentials 
# please edit this portion to your chatbot credentials 
TOKEN = ""
getcontent = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
chat_id = ""

# function used for motion detection
def motion_detection():
    distance_threshold = 30

    def distance():
        # an ultrasonic sensure function used to measure the distance
        GPIO.output(25, 1)
        time.sleep(0.00001)
        GPIO.output(25, 0)

        # measure pulse width (i.e. time of flight) at Echo
        StartTime = time.time()
        StopTime = time.time()
        while GPIO.input(27) == 0:
            StartTime = time.time()  # capture start of high pulse
        while GPIO.input(27) == 1:
            StopTime = time.time()  # capture end of high pulse
        ElapsedTime = StopTime - StartTime

        # compute distance in cm, from time of flight
        Distance = (ElapsedTime * 34300) / 2
        # distance=time*speed of ultrasound,
        # /2 because to & fro
        return Distance
    
    def unlocking_door():
        while True: 
            # checks if the owner wants to open the door 
            updates = requests.get(getcontent).json()
            for update in updates['result']:
                if 'message' in update and 'text' in update['message']:
                    command = update['message']['text']
                    if command == '/unlock_door':
                        print("Door opened")
                        for _ in range(3):
                            # the LED would blink 3 times to indicate that the door has been opened
                            GPIO.output(24, 1)
                            sleep(0.2)
                            GPIO.output(24, 0)
                            sleep(0.2)
                        sys.exit()
            sleep(5)
    command_thread = threading.Thread(target=unlocking_door)
    command_thread.start()


    while True:
        # check if there is a presence using the ultrasonic sensor
        if distance() <= distance_threshold:
            print("Presence Detected")
            # capture a picture of the intruder
            picture_filename = "intruder_picture.jpg"
            my_camera.capture(picture_filename)

            # send the picture to the homeowner
            files = {'photo': open(picture_filename, 'rb')}
            data = {'chat_id': chat_id}
            response = requests.post(url, files=files, data=data)
            sleep(10)

# function used for keypad activation
def keypad_activation():
    MATRIX = [[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9],
              ['*', 0, '#']]
    ROW = [6, 20, 19, 13]
    COL = [12, 5, 16]

    # setting up the GPIO pins
    for i in range(3):
        GPIO.setup(COL[i], GPIO.OUT)
        GPIO.output(COL[i], 1)

    for j in range(4):
        GPIO.setup(ROW[j], GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # the door password that can be altered
    code = [1, 2, 3, 4]
    entered_code = []

    maxAttempts = 3
    attempts = 0
        
    while True:
        while attempts < maxAttempts:
            for i in range(3):
                GPIO.output(COL[i], 0)
                for j in range(4):
                    if GPIO.input(ROW[j]) == 0:
                        entered_code.append(MATRIX[j][i])
                        while GPIO.input(ROW[j]) == 0:
                            sleep(0.1)
                GPIO.output(COL[i], 1)

            if len(entered_code) == 4:
                # check if the entered code is correct
                if entered_code == code:
                    print("Door opened")
                    for _ in range(3):
                        # the LED would blink 3 times to indicate that the door has been opened
                        GPIO.output(24, 1)
                        sleep(0.2)
                        GPIO.output(24, 0)
                        sleep(0.2)
                    sys.exit()
                else:
                    print("Incorrect Password")
                    attempts += 1
                    print("Attempts remaining:", maxAttempts - attempts)
                    if attempts == maxAttempts:
                        print("Homeowner has been notified!")
                        # buzzer function used to alert the homeowner
                        for _ in range(4):
                            GPIO.output(18, 1)
                            sleep(0.2)
                            GPIO.output(18, 0)
                            sleep(0.2)

                        # capture a picture of the intruder
                        picture_filename = "intruder_picture.jpg"
                        my_camera.capture(picture_filename)

                        files = {'photo': open(picture_filename, 'rb')}
                        data = {'chat_id': chat_id}
                        response = requests.post(url, files=files, data=data)

                    entered_code = []

# create threads used for motion detection and keypad activation
t1 = threading.Thread(target=motion_detection)
t2 = threading.Thread(target=keypad_activation)

# start the threads
t1.start()
t2.start()

# join the threads
t1.join()
t2.join()
