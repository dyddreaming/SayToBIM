def play_audio():
    # 播放录制的音频
    audio_file = os.path.join(audio_dir, "audio_message.wav")
    if os.path.exists(audio_file):
        print("播放音频...")
        audio_data, fs = sf.read(audio_file, dtype='float32')
        sd.play(audio_data, fs)
        sd.wait()
        print("音频播放完成")
    else:
        print("音频文件不存在")


def send_audio_message():
    # 发送音频消息
    threading.Thread(target=record_audio).start()


def play_received_audio():
    # 播放接收到的音频消息
    threading.Thread(target=play_audio).start()