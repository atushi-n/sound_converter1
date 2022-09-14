import threading

from pathlib import Path


import pygame
import serial
import os
import tkinter as tk
from tkinter import ttk


from gui import Template

import time


class SoundFiles:
    @classmethod
    def get_files_dict(cls):
        path = os.getcwd()
        import glob

        sounds_dict = {}
        files = glob.glob(f"{path}/sounds/*")
        for file in files:
            sounds_dict[str(Path(file).stem)] = file

        return sounds_dict

    @classmethod
    def get_files(cls):
        path = os.getcwd()
        import glob

        sounds_dict = {}
        files = glob.glob(f"{path}/sounds/*")
        for file in files:
            sounds_dict[str(Path(file).stem)] = file

        return list(sounds_dict.keys())


class App(Template):

    isArrival = False

    def __init__(self):
        super(App, self).__init__()
        self.createWidgets()
        self.attachWidgets()
        threading.Thread(target=self.event_handler).start()

    def createWidgets(self):
        self.frame_1 = tk.Frame(self, bg="tan")
        self.frame_3 = tk.Frame(self, bg="green")
        self.frame_2 = tk.Frame(self, bg="blue")

        self.combobox = ttk.Combobox(self.frame_1)

        self.combobox.configure(values=SoundFiles.get_files())
        self.combobox.set(SoundFiles.get_files()[0])

        self.play_button = tk.Button(
            self.frame_2,
            text="play",
            command=lambda: self.push_play_button(is_manual=True),
        )

        self.sleep_time_area = tk.Entry(self.frame_3)
        self.info_label = tk.Label(self.frame_3, text=":minutes")

        self.stop_button = tk.Button(
            self.frame_2, text="stop", command=self.push_stop_button
        )
        self.next_button = tk.Button(
            self.frame_1, text="↓", command=self.push_next_button
        )

    def attachWidgets(self):
        self.frame_1.pack(fill=tk.BOTH, side=tk.TOP, expand=1)
        self.frame_3.pack(fill=tk.BOTH, side=tk.TOP, expand=1)
        self.frame_2.pack(fill=tk.BOTH, side=tk.TOP, expand=1)

        self.combobox.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
        self.sleep_time_area.pack(fill=tk.BOTH, side=tk.LEFT, expand=1, pady=1)
        self.info_label.pack(fill=tk.BOTH, side=tk.LEFT, expand=1, pady=1)
        self.next_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
        self.play_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=1, pady=1)
        self.stop_button.pack(fill=tk.BOTH, side=tk.LEFT, expand=1, pady=1)

    def push_next_button(self):
        current_sound = self.combobox.get()
        sounds = self.combobox["values"]
        for i, sound in enumerate(sounds):
            if current_sound == sound:
                i += 1
                if i >= len(sounds):
                    i = 0
                self.combobox.set(sounds[i])
                break

    def push_play_button(self, is_manual=False):
        target_sound_path = SoundFiles.get_files_dict()[self.combobox.get()]
        pygame.mixer.init(frequency=11025)  # 初期設定
        pygame.mixer.music.load(target_sound_path)  # 音楽ファイルの読み込み
        pygame.mixer.music.play(1)  # 音楽の再生回数(1回)
        if is_manual:
            threading.Thread(target=self.play_timer).start()

    def push_stop_button(self):
        pygame.mixer.music.stop()  # 再生の終了

    def event_handler(self):  # サンプルを見るとこれが多いが音楽をキューい入れるというアプローチも一応ある
        MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(MUSIC_END)
        while True:
            time.sleep(1)
            for event in pygame.event.get():
                if event.type == MUSIC_END:
                    time.sleep(1)
                    if not App.isArrival:
                        self.push_next_button()
                        self.push_play_button()

    def play_timer(self):
        time.sleep(int(self.sleep_time_area.get()))
        pygame.mixer.music.stop()
        App.isArrival = True


def gui():
    app = App()
    app.run()


if __name__ == "__main__":

    threading.Thread(target=gui).start()  # guiの開始

    pygame.init()

    ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=None)

    while True:
        line = ser.readline()
        value = repr(line.strip())[2 : len(repr(line.strip())) - 1]
        print(
            f"{value}: {int(value) / 40}"
        )  # 0〜1に正規化している。※esp32は0~4095のアナログ値を取るがゆらぎを防ぐために割る10しているので送られてくる値は0~409である
        pygame.mixer.music.set_volume(int(value) / 40)  # リアルタイム対応
    ser.close()
