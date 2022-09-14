
import RPi.GPIO as GPIO
import time
import RPi.GPIO as GPIO
from shiftr_74HC595.shiftr_74HC595 import ShiftRegister
from time import sleep


class TimeLight():

    def __init__(self):
        data_pin = 23  # GPIO23にデータピンを設定
        latch_pin = 22  # GPIO24にラッチピンを設定
        clock_pin = 21  # GPIO25にクロックピンを設定
        GPIO.setmode(GPIO.BOARD)
        self.current_light = 0
        self.shift_register = ShiftRegister(data_pin, latch_pin, clock_pin)
        self.shift_register.setOutputs([GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW])

    def light(self, data: int):
        '''

        :param data: 0~8
        :return:
        '''
        lights = []
        for i in range(1, 9):
            if i > data:
                lights.append(GPIO.LOW)
            else:
                lights.append(GPIO.HIGH)

        self.shift_register.setOutputs(lights)
        time.sleep(0.5)
        print(f"x{lights}")

        self.shift_register.latch()

    def next_light(self):

        print(self.current_light)
        self.light(self.current_light)
        self.add_current_light()

    def add_current_light(self):
        if self.current_light > 7:
            self.current_light = 0
        else:
            self.current_light += 1


    def destroy(self):
        self.shift_register.setOutputs([GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW])
        self.shift_register.latch()


if __name__ == "__main__":


    try:
        time_light = TimeLight()
        for x in range(15):
            time_light.next_light()




    except KeyboardInterrupt:
        pass
    finally:
        time_light.destroy()

    GPIO.cleanup()









