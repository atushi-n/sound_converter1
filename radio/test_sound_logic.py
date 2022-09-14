import time

import RPi.GPIO as GPIO

import sound_logic
from sift import TimeLight
from sound_logic import *







if __name__ == "__main__":



    sd = SoundLogic()

    time_light = TimeLight()
    sd.time_light = time_light

    GPIO.setmode(GPIO.BOARD)
    play_pin = 11
    stop_pin = 13
    next_pin = 15
    time_pin = 16
    GPIO.setup(play_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(stop_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(next_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(time_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    try:

        while True:


                play_push = GPIO.input(play_pin)
                stop_push = GPIO.input(stop_pin)
                next_push = GPIO.input(next_pin)
                time_push = GPIO.input(time_pin)






                if play_push:
                    sd.push_play()
                    time.sleep(0.3)

                elif stop_push:
                    sd.push_stop()
                    time.sleep(0.3)

                elif next_push:
                    sd.push_next()
                    time.sleep(0.3)

                elif time_push:
                    sd.push_time()
                    time.sleep(0.3)

                elif False:
                    exit()
                time.sleep(0.05)


    finally:
        time_light.destroy()
        GPIO.cleanup()
        print("exit")
