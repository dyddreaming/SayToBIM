import tkinter as tk
from tkinter import ttk
from datetime import datetime
import sounddevice as sd
import soundfile as sf
import threading
import os
import pandas as pd
from KeyWord import key_word
import json
import requests
import pyaudio
import wave
from Voice import wav_to_text, record_audio

# 全局变量来存储聊天对话信息
chat_history = []
start_flag = False


def create_chat_window():
    results = {}
    # 音频文件存储目录
    audio_dir = "audio_messages"

    # 创建音频存储目录
    os.makedirs(audio_dir, exist_ok=True)

    # def record_audio(dur, output_file):
    #     chunk = 1024
    #     sample_format = pyaudio.paInt32
    #     channels = 2
    #     fs = 44100
    #
    #     p = pyaudio.PyAudio()
    #
    #     stream = p.open(format=sample_format,
    #                     channels=channels,
    #                     rate=fs,
    #                     frames_per_buffer=chunk,
    #                     input=True)
    #
    #     frames = []
    #
    #     print('----------开始录制---------')
    #
    #     for i in range(int(fs / chunk * dur)):
    #         data = stream.read(chunk)
    #         frames.append(data)
    #     print('----------录制结束了--------')
    #     """while start_flag:
    #         data = stream.read(chunk)
    #         frames.append(data)"""
    #
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()
    #
    #     wf = wave.open(output_file, 'wb')
    #     wf.setnchannels(channels)
    #     wf.setsampwidth(p.get_sample_size(sample_format))
    #     wf.setframerate(fs)
    #     wf.writeframes(b''.join(frames))
    #     wf.close()

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
            # 在聊天框中显示用户发送的消息（左边，蓝色）
            chat_display.config(state=tk.NORMAL)
            chat_message = f"You: {txt}\n"
            chat_display.insert(tk.END, chat_message, "user_message")
            chat_display.config(state=tk.DISABLED)
            chat_history.append(chat_message)  # 将消息添加到聊天历史

            print('----------开始提取文字关键字--------')
            dict_data = key_word(txt)
            print(dict_data)

            # 将结果转换为JSON格式
            results_json = json.dumps(dict_data)

            # 发送POST请求
            url = 'http://127.0.0.1:8080/make_data'
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=results_json, headers=headers)

            # 检查响应状态
            if response.status_code == 200:
                print("数据成功发送到服务器")
            else:
                print("发送数据时出现错误")

    # def stop_record():
    #     global start_flag
    #     start_flag = False
    #     print('----------录制结束了--------')
    #     txt = wav_to_text(wav_file)
    #     if txt == 'error':
    #         print('语音转文字出错')
    #     else:
    #         # 在聊天框中显示用户发送的消息（左边，蓝色）
    #         chat_display.config(state=tk.NORMAL)
    #         chat_message = f"You: {txt}\n"
    #         chat_display.insert(tk.END, chat_message, "user_message")
    #         chat_display.config(state=tk.DISABLED)
    #         chat_history.append(chat_message)  # 将消息添加到聊天历史
    #
    #         print('----------开始提取文字关键字--------')
    #         dict_data = key_word(txt)
    #         print(dict_data)
    #
    #         # 将结果转换为JSON格式
    #         results_json = json.dumps(dict_data)
    #
    #         # 发送POST请求
    #         url = 'http://127.0.0.1:8080/make_data'
    #         headers = {'Content-Type': 'application/json'}
    #         response = requests.post(url, data=results_json, headers=headers)
    #
    #         # 检查响应状态
    #         if response.status_code == 200:
    #             print("数据成功发送到服务器")
    #         else:
    #             print("发送数据时出现错误")

    def view_chat_history():
        # 创建一个新弹窗来显示数据表格
        data_window = tk.Toplevel(root)
        data_window.title("Data Table")

        # 读取CSV文件
        data = pd.read_csv("data.csv", encoding="gb2312")

        # 删除NaN行
        data = data.dropna()

        # 创建表格控件
        frame = tk.Frame(data_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # 创建水平滚动条
        hsb = ttk.Scrollbar(frame, orient="horizontal")
        hsb.pack(side="bottom", fill="x")

        tree = ttk.Treeview(frame, columns=list(data.columns), show="headings", xscrollcommand=hsb.set)
        tree.pack(fill=tk.BOTH, expand=True)

        # 添加滚动条
        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vsb.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vsb.set)

        # 添加表头
        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor=tk.CENTER)

        # 设置表格高度
        table_height = min(len(data), 10)  # 限制显示行数为10行
        tree["height"] = table_height

        # 插入数据
        for _, row in data.iterrows():
            tree.insert("", "end", values=list(row))

        # 设置水平滚动条的联动
        hsb.config(command=tree.xview)

        # 增大字体
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14))
        style.configure("Treeview", font=("Arial", 12))

        # 添加表格线
        style.configure("Treeview", rowheight=30)  # 设置行高
        style.map("Treeview", background=[("selected", "#008CBA")])  # 设置选中行的背景颜色为按钮颜色
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe', 'border': 1})])  # 显示网格线和边框线

        # 添加列选中功能
        selected_col = None

        def on_tree_select(event):
            nonlocal selected_col
            col = tree.identify_column(event.x)
            selected_col = col

            # 重置所有列的颜色
            for column in tree["columns"]:
                tree.tag_configure(column, background="")

            # 设置选中列的颜色
            if selected_col:
                tree.tag_configure(selected_col, background="#008CBA")

        # 绑定事件
        tree.bind("<Button-1>", on_tree_select)

    def send_message(event=None):  # 使用event参数来处理Enter键事件
        text = entry.get()
        if text:
            # 在聊天框中显示用户发送的消息（左边，蓝色）
            chat_display.config(state=tk.NORMAL)
            chat_message = f"You: {text}\n"
            chat_display.insert(tk.END, chat_message, "user_message")
            chat_display.config(state=tk.DISABLED)
            chat_history.append(chat_message)  # 将消息添加到聊天历史

            entry.delete(0, tk.END)
            results.update(key_word(text))
            print(results)
            flag = 0
            geometry = ""
            for geometry, attributes in results.items():
                if attributes:
                    continue
                else:
                    reply = "Bot:请提供{}的属性信息。".format(geometry)
                    flag = 1
                    break

            if flag == 0:
                reply = "Bot:好的，马上为您进行建模，请稍等。".format(geometry)
                # 将结果转换为JSON格式
                results_json = json.dumps(results)

                # 发送POST请求
                url = 'http://127.0.0.1:8080/make_data'
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, data=results_json, headers=headers)

                # 检查响应状态
                if response.status_code == 200:
                    print("数据成功发送到服务器")
                else:
                    print("发送数据时出现错误")

            chat_display.config(state=tk.NORMAL)
            chat_display.insert(tk.END, f"{reply}\n", "bot_message")
            chat_display.config(state=tk.DISABLED)
            chat_history.append(reply)  # 将机器人回复添加到聊天历史

    # 创建主窗口
    root = tk.Tk()
    root.title("Modeling")

    # 创建聊天显示框
    chat_display = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, bg="#f2f2f2", font=("Arial", 12))
    chat_display.grid(row=0, column=0, padx=10, pady=10, columnspan=2, sticky="nsew")

    # 创建消息输入框
    entry = tk.Entry(root, width=40, font=("Arial", 12))
    entry.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="ew")
    entry.bind('<Return>', send_message)  # 绑定Enter键事件

    # 创建按钮框架
    button_frame = tk.Frame(root)
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)

    # 创建发送文本按钮
    send_button = tk.Button(button_frame, text="发送文本", command=send_message, bg="#008CBA", fg="white",
                            font=("Arial", 12))
    send_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

    # 创建录制语音按钮
    record_audio_button = tk.Button(button_frame, text="录制语音", command=core_code, bg="#008CBA", fg="white",
                                    font=("Arial", 12))
    record_audio_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

    # # 创建停止录制按钮
    # stop_audio_button = tk.Button(button_frame, text="停止录制", command=stop_record, bg="#008CBA", fg="white", font=("Arial", 12))
    # stop_audio_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

    # 创建查看历史按钮
    view_history_button = tk.Button(button_frame, text="模型查看", command=view_chat_history, bg="#008CBA", fg="white",
                                    font=("Arial", 12))
    view_history_button.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.BOTH, expand=True)

    # 设置聊天框样式
    chat_display.tag_configure("user_message", foreground="#008CBA", justify="left")  # 用户消息样式
    chat_display.tag_configure("bot_message", foreground="#FF5733", justify="left")  # 机器人消息样式

    # 设置窗口大小不可调整
    root.resizable(False, False)

    # 设置窗口背景颜色
    root.configure(bg="#ffffff")

    # 设置聊天显示框不可编辑
    chat_display.config(state=tk.DISABLED)

    # 设置消息输入框和发送按钮在窗口大小变化时自动扩展
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # 启动主事件循环
    root.mainloop()


if __name__ == "__main__":
    create_chat_window()
