import time
import wave
import random
import pathlib
from pathlib import Path
import pydub
import numpy as np

def create_white_noise():
    A = 1.0  # 振幅
    sec = 10  # 信号の長さ s
    sf = 44100  # サンプリング周波数 Hz

    x = np.random.rand(round(sf * sec))  # ホワイトノイズの生成
    print(x.shape)
    # sd.play(x,sf)
    print("再生中")

    # status=sd.wait()
    write_file = wave.open(str("effect.wav"), "wb")

    # wavを書き込むための設定
    write_file.setnchannels(1)  # チャンネル数
    write_file.setsampwidth(2)  # ビットデプス(サンプルノイズ)
    write_file.setframerate(sf)  # サンプリングレート

    write_file.writeframes(x)  # ファイルに書き込み
    write_file.close()


def print_wave_info(wave_file):
    print(f"channel: {wave_file.getnchannels()}")  # モノラルorステレオ
    print(f"samplingrate: {wave_file.getframerate()}")  # サンプリング周波数
    print(f"{wave_file.getnframes()}")  # フレームの総数
    print(f"bitDepth: {wave_file.getsampwidth()}")  # ビットデプス（サンプルサイズ）Byte表現


def distribution_sound(dist, input_file: Path, output_file: Path = None):
    if output_file is None:
        output_file = Path(f"{input_file.parent}/{input_file.stem}_out.wav")

    wave_file = wave.open(str(input_file), "r")
    print_wave_info(wave_file)
    x = wave_file.readframes(wave_file.getnframes())  # frameの読み込み
    x = np.frombuffer(x, dtype="int16").copy()  # numpy.arrayに変換※copy()していることに注意

    # startが1だとレフトに割り振りできる
    start = 1 if dist == "left" else 0
    for i in range(start, x.shape[0], 2):
        x[i] = 0

    # wavデータ書き込み用のファイルを作成
    write_file = wave.open(str(output_file), "wb")

    # wavを書き込むための設定
    write_file.setnchannels(2)  # チャンネル数
    write_file.setsampwidth(2)  # ビットデプス(サンプルノイズ)
    write_file.setframerate(wave_file.getframerate())  # サンプリングレート

    bytearray_data = bytearray(x)  # listを元にbytearrayオブジェクトを作成
    write_file.writeframes(bytearray_data)  # ファイルに書き込み
    write_file.close()


def stereo_to_monaural(input_file: Path, output_file: Path = None):
    if output_file is None:
        output_file = Path(f"{input_file.parent}/{input_file.stem}_out.wav")

    wave_file = wave.open(str(input_file), "r")

    print_wave_info(wave_file)

    x = wave_file.readframes(wave_file.getnframes())  # frameの読み込み
    x = np.frombuffer(x, dtype="int16").copy()  # numpy.arrayに変換
    print(x.shape)
    print(x)
    left, right = x[::2], x[::1]  # モノラルにするためにどちらかを使う

    # wavデータ書き込み用のファイルを作成
    write_file = wave.open(str(output_file), "wb")

    # wavを書き込むための設定
    write_file.setnchannels(1)  # チャンネル数
    write_file.setsampwidth(2)  # ビットデプス(サンプルノイズ)
    write_file.setframerate(wave_file.getframerate())  # サンプリングレート

    bytearray_data = bytearray(left)  # listを元にbytearrayオブジェクトを作成
    write_file.writeframes(bytearray_data)  # ファイルに書き込み
    write_file.close()


def monaural_down_depth8(input_file: Path, output_file: Path = None):
    if output_file is None:
        output_file = Path(f"{input_file.parent}/{input_file.stem}_down_d8.wav")

    wave_file = wave.open(str(input_file), "r")

    print_wave_info(wave_file)

    frames = wave_file.readframes(wave_file.getnframes())  # frameの読み込み
    frames = np.frombuffer(frames, dtype="int16").copy()  # numpy.arrayに変換 符号付き16bit整数
    data = []

    i = 0
    while True:
        if frames.shape[0] - 1 <= i:
            if frames.shape[0] % 2 != 0:
                element1 = (((frames[i]) / (2 ** 8)).item()).to_bytes(1, byteorder="big", signed=False)  # 1byteに収める
                data.append(int.from_bytes(element1 + b'0'))
            break

        element1 = (int)(((frames[i]) / (2 ** 8)).item()) + 128  # 1byteに収める item()はnumpy.float64をfloatに
        print(element1)
        i += 1
        element2 = (int)(((frames[i]) / (2 ** 8)).item()) + 128  # 1byteに収める
        print(element2)

        print(element1.to_bytes(1, byteorder="big", signed=False) + element2.to_bytes(1, byteorder="big", signed=False))
        i += 1
        # print(element1.to_bytes(1, byteorder="big", signed=False))

        b = (element1.to_bytes(1, byteorder="big", signed=False) + element2.to_bytes(1, byteorder="big", signed=False))

        data.append(int.from_bytes(b, byteorder="big"))

    data = np.array(data, dtype="int16")

    # wavデータ書き込み用のファイルを作成
    write_file = wave.open(str(output_file), "wb")

    # wavを書き込むための設定
    write_file.setnchannels(1)  # チャンネル数
    write_file.setsampwidth(1)  # ビットデプス(サンプルノイズ)
    write_file.setframerate(wave_file.getframerate())  # サンプリングレート

    bytearray_data = bytearray(data)  # listを元にbytearrayオブジェクトを作成
    write_file.writeframes(bytearray_data)  # ファイルに書き込み
    write_file.close()


def monaural_down_depth10(input_file: Path, output_file: Path = None):
    if output_file is None:
        output_file = Path(f"{input_file.parent}/{input_file.stem}_down_d10.wav")

    wave_file = wave.open(str(input_file), "r")

    print_wave_info(wave_file)

    frames = wave_file.readframes(wave_file.getnframes())  # frameの読み込み
    frames = np.frombuffer(frames, dtype="int16").copy()  # numpy.arrayに変換
    data = []

    i = 0
    while True:
        if frames.shape[0] - 1 <= i:
            break

        element1 = (int)(((frames[i]) / (2 ** 6)).item())  # 10bitに収める
        i += 1

        b = (element1.to_bytes(2, byteorder="big", signed=True))

        data.append(int.from_bytes(b, byteorder="big"))

    data = np.array(data, dtype="int16")

    # wavデータ書き込み用のファイルを作成
    write_file = wave.open(str(output_file), "wb")

    # wavを書き込むための設定
    write_file.setnchannels(1)  # チャンネル数
    write_file.setsampwidth(2)  # ビットデプス(サンプルノイズ)
    write_file.setframerate(wave_file.getframerate())  # サンプリングレート

    bytearray_data = bytearray(data)  # listを元にbytearrayオブジェクトを作成
    write_file.writeframes(bytearray_data)  # ファイルに書き込み
    write_file.close()


def monaural_down_sampling(input_file: Path, output_file: Path = None):
    if output_file is None:
        output_file = Path(f"{input_file.parent}/{input_file.stem}_down.wav")

    wave_file = wave.open(str(input_file), "r")

    print_wave_info(wave_file)

    x = wave_file.readframes(wave_file.getnframes())  # frameの読み込み
    x = np.frombuffer(x, dtype="int16").copy()  # numpy.arrayに変換

    print(x.shape)
    print(x)

    data = []
    j = 0
    for i in range(0, x.shape[0], 4):
        data.append(x[i])

    data = np.array(data, dtype="int16")

    # wavデータ書き込み用のファイルを作成
    write_file = wave.open(str(output_file), "wb")

    # wavを書き込むための設定
    write_file.setnchannels(1)  # チャンネル数
    write_file.setsampwidth(2)  # ビットデプス(サンプルノイズ)
    write_file.setframerate(wave_file.getframerate() / 4)  # サンプリングレート

    bytearray_data = bytearray(data)  # listを元にbytearrayオブジェクトを作成
    write_file.writeframes(bytearray_data)  # ファイルに書き込み
    write_file.close()


def monaural_cut(input_file: Path, output_file: Path = None):
    if output_file is None:
        output_file = Path(f"{input_file.parent}/{input_file.stem}_cut.wav")

    wave_file = wave.open(str(input_file), "r")

    print_wave_info(wave_file)

    x = wave_file.readframes(wave_file.getnframes())  # frameの読み込み
    x = np.frombuffer(x, dtype="int16").copy()  # numpy.arrayに変換

    q_3 = np.percentile(x, 75)  # 第３四分位数→あまりいいやり方ではないかもしれない
    q_1 = np.percentile(x, 5)  # 第１四分位数

    data = []
    j = 0
    for i in range(0, x.shape[0]):
        if x[i] > q_3:
            data.append(q_3)
        elif x[i] < q_1:
            data.append(q_1)
        else:
            data.append(x[i])

    data = np.array(data, dtype="int16")

    # wavデータ書き込み用のファイルを作成
    write_file = wave.open(str(output_file), "wb")

    # wavを書き込むための設定
    write_file.setnchannels(1)  # チャンネル数
    write_file.setsampwidth(2)  # ビットデプス(サンプルノイズ)
    write_file.setframerate(wave_file.getframerate())  # サンプリングレート

    bytearray_data = bytearray(data)  # listを元にbytearrayオブジェクトを作成
    write_file.writeframes(bytearray_data)  # ファイルに書き込み
    write_file.close()


def mp3_to_wav(input_file: Path, output_file: Path = None):
    if output_file is None:
        output_file = Path(f"{input_file.parent}/{input_file.stem}_out.wav")

    sound = pydub.AudioSegment.from_mp3(input_file)
    sound.export(str(output_file), format="wav")


# base_sound = AudioSegment.from_file("sounds/宝石の国op.wav", format="wav")  # 効果音を読み込み
# effect_sound = AudioSegment.from_file("effect.wav", format="wav")
# effect_sound = effect_sound + ratio_to_db(0.1)
# start_time_ms = 5 * 1000  # 効果音を５秒時点から鳴らす
# result_sound = base_sound.overlay(effect_sound, start_time_ms)  # ベースの音声に効果音をつける
# result_sound.export("result_sound.wav", format="wav")