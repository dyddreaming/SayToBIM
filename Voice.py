#!/usr/bin/env python3

import wave
from datetime import datetime
from pydub import AudioSegment
import pyaudio

import speech_recognition as sr
from KeyWord import key_word

start_flag = True


def record_audio(dur, output_file):
    chunk = 1024
    sample_format = pyaudio.paInt32
    channels = 2
    fs = 44100

    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    print('----------开始录制---------')

    for i in range(int(fs / chunk * dur)):
        data = stream.read(chunk)
        frames.append(data)
    print('----------录制结束了--------')
    """while start_flag:
        data = stream.read(chunk)
        frames.append(data)"""

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(output_file, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()


def wav_to_text(audio_file):
    result = 'error'
    # 创建 SpeechRecognition 对象
    r = sr.Recognizer()

    # 读取音频文件
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)

    # 识别音频文件
    try:
        result = r.recognize_google(audio, language='zh-CN')
        print(result)
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
        # raise 'Google Speech Recognition could not understand audio'
    except sr.RequestError as e:
        # raise 'Could not request results from Google Speech Recognition Service'
        print('Could not request results from Google Speech Recognition Service')
    return result


def core_code():
    start_time = datetime.now()

    duration = 15  # 录制时长（秒）
    mxf_file = './wavdata/recording'  # 录制输出的文件路径

    str1 = datetime.strftime(start_time, '%Y%m%d%H%M%S')
    # wav_file=mxf_file+start_time.strftime('%Y-%m-%d-%H-%M-%S')+'.wav'
    wav_file = mxf_file + str1 + '.wav'
    print(wav_file)
    record_audio(duration, wav_file)
    print('----------开始语音转文字--------')
    txt = wav_to_text(wav_file)
    if txt == 'error':
        print('语音转文字出错')
    else:
        print('----------开始提取文字关键字--------')
        dict_data = key_word(txt)
        print(dict_data)
