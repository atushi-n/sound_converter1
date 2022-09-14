import threading
from pathlib import Path
import pygame
import os
import tkinter as tk
from tkinter import ttk

import pykakasi

from gui import Template
import time
import glob


from i2clcda import *
from sound_logic import SoundLogic, SoundFiles

if __name__ == "__main__":

    pygame.init()
    lcd_init()
    kks = pykakasi.kakasi()

    sound_logic = SoundLogic()

    sound_logic.push_play(SoundFiles.get_files_dict()["打ち上げ花火1"])

    try:
        s_index = 0
        while True:
            s_index = s_index + 1 if s_index < len(SoundFiles.get_files()) - 1 else 0
            time.sleep(1)
            text1 = ""
            text2 = ""
            for x in kks.convert(SoundFiles.get_files()[s_index]):
                if 13 >= len(text1):
                    text1 += x["hepburn"]
                else:
                    text2 += x["hepburn"]
            lcd_string(text1, LCD_LINE_1)
            lcd_string(text2, LCD_LINE_2)

            time.sleep(3)
    except KeyboardInterrupt:
        pass
    finally:
        print("exit")
        lcd_byte(0x01, LCD_CMD)
