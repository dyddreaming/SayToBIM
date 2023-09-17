from Chat import create_chat_window
from flask import Flask, render_template, request, jsonify
import multiprocessing as mp
from multiprocessing import Process, Value, Array
import json

results = {}
hand_data = {}
app = Flask(__name__)

@app.route('/make_data', methods=['GET', 'POST'])
def make_data():
    global results
    if request.method == 'POST':
        results.update(request.get_json())
        print(results)
        data = {'state':True}
        return jsonify(data)
    if request.method == 'GET':
        # 如果是GET请求，返回数组信息
        temp = {}
        temp.update(results)
        #results.clear()
        return jsonify(temp)

@app.route('/hand_data',methods=['GET', 'POST'])
def hand_data():
    global hand_data
    if request.method == 'POST':
        hand_data = request.get_json()
        print(hand_data)
        data = {'state': True}
        return jsonify(data)
    if request.method == 'GET':
        return jsonify(hand_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)