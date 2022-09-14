import threading
import time
from pathlib import Path
import pygame
import os

import glob


class SoundFiles:
    SOUND_FILE_PATH = f"{os.getcwd()}/sounds/*"

    @classmethod
    def get_files_dict(cls) -> dict:

        sounds_dict = {}
        files = glob.glob(SoundFiles.SOUND_FILE_PATH)
        for file in files:
            sounds_dict[str(Path(file).stem)] = file
        return sounds_dict

    @classmethod
    def get_files(cls) -> list:
        path = os.getcwd()
        import glob

        sounds_dict = {}
        files = glob.glob(f"{path}/sounds/*")
        for file in files:
            sounds_dict[str(Path(file).stem)] = file

        return list(sounds_dict.keys())


class SoundLogic:#ラズパイ側ではイベントが発行されないのにubuntuで実行するとstopのときもイベントが発行されてしまうバグがある。
    def __init__(self):
        pygame.init()
        self.time_light = None

        self.thread_event = threading.Event()
        self.s_push = False#バグ用のコード。ラズパイでは消す
        self.isArrival = False
        self.now_play = False
        self.file_names = SoundFiles.get_files()
        self.sound_index = 0
        self.until_sleep_minute = 5

        # 自動で次を再生する。（再生の終了イベントをハンドルする）
        # daemonをTrueにすると、メインスレッドが終了すると自身も終了する
        threading.Thread(target=self.sound_finish_event_handler, daemon=True).start()

    def get_until_sleep_second(self):
        return self.until_sleep_minute

    def play_sound(self):
        self.now_play = True
        self.isArrival = False
        pygame.mixer.init(frequency=11025)  # 初期設定
        print(SoundFiles.get_files_dict()[self.file_names[self.sound_index]])
        pygame.mixer.music.load(
            SoundFiles.get_files_dict()[self.file_names[self.sound_index]]
        )  # 音楽ファイルの読み込み
        pygame.mixer.music.play(1)  # 音楽の再生回数(1回)

    def stop_sound(self):
        self.now_play = False
        pygame.mixer.music.stop()  # 再生の終了

    def next_sound(self):
        if len(self.file_names) - 1 > self.sound_index:
            self.sound_index += 1
        else:
            self.sound_index = 0

    def push_play(self):
        print("push_play")
        if not self.now_play:
            self.play_sound()
            threading.Thread(
                target=self.play_timer, daemon=True
            ).start()

    def push_stop(self):
        print("push_stop")
        if self.now_play:
            self.s_push = True  # バグ用のコード。ラズパイでは消す
            self.thread_event.set()
            self.stop_sound()

    def push_next(self):
        print("push_next")
        self.next_sound()
        if self.now_play:
            self.play_sound()

    def push_time(self):
        print("push time")
        if not self.now_play:
            self.push_time_event()

    def push_time_event(self):
        self.until_sleep_minute = self.time_light.current_light * 10
        self.time_light.next_light()

    # このスレッドはインスタンス作成時から破棄まで、キルされることはない
    def sound_finish_event_handler(self):  # サンプルを見るとこれが多いが音楽をキューに入れるというアプローチも一応ある

        # 他のイベントとかぶらせないために独自イベント32851を作成して登録
        MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(MUSIC_END)

        while True:
            time.sleep(1)
            for event in pygame.event.get():
                print(event)
                if event.type == MUSIC_END:
                    print("音楽が終了")
                    if not self.isArrival:  # 到達していない
                        if not self.s_push:#バグ用のコード。ラズパイでは消す
                            print("next sound")
                            self.next_sound()
                            self.play_sound()
                        else:
                            self.s_push = True#バグ用のコード。ラズパイでは消す
    def play_timer(self):
        print("timer start")
        if self.thread_event.wait(self.get_until_sleep_second()):#指定した時間でタイマーを開始
            print("明示的")
        else:
            print("タイマーが到達")
            pygame.mixer.music.fadeout(1500)
            time.sleep(1.5)
            self.isArrival = True
            self.stop_sound()

        print("timer stop")
        self.thread_event.clear()


if __name__ == "__main__":

    sd = SoundLogic()
    print(SoundFiles.SOUND_FILE_PATH)
    try:
        while True:
            opr = input(f"push key : current index {sd.sound_index}\n")
            if opr == "p":
                sd.push_play()
            elif opr == "s":
                sd.push_stop()
            elif opr == "n":
                sd.push_next()
            elif opr == "t":
                sd.push_time()
            elif opr == "e":
                exit()
    finally:

        print("exit")
