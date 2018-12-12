# -*- coding: utf-8 -*-
# @Time    : 18-12-3 上午10:51
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn

import sys
import json
import time
import threading
import wave
import requests
from pyaudio import PyAudio, paInt16
IS_PY3 = sys.version_info.major == 3

if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    timer = time.perf_counter



API_KEY = '22hQrRcbkQS7mRgtuD2h25Q3'
SECRET_KEY = 'u3bmPDWHZV3lktcu8jdiXOe1uErwehhw'

# 需要识别的文件
# AUDIO_FILE = './pcm/16k.pcm' # 只支持 pcm/wav/amr
AUDIO_FILE = '1_1.wav' # 只支持 pcm/wav/amr

# 文件格式
FORMAT = AUDIO_FILE[-3:];  # 文件后缀只支持 pcm/wav/amr

# 根据文档填写PID，选择语言及识别模型
DEV_PID = 1536;  # 1537 表示识别普通话，使用输入法模型。1536表示识别普通话，使用搜索模型

CUID = '123456PYTHON';
# 采样率
RATE = 16000;  # 固定值

ASR_URL = 'http://vop.baidu.com/server_api'


class DemoError(Exception):
    pass

"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_voice_assistant_get'  # 有此scope表示有asr能力，没有请在网页里勾选


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    print(result_str)
    result = json.loads(result_str)
    print(result)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        print('SUCCESS WITH TOKEN: %s ; EXPIRES IN SECONDS: %s' % (result['access_token'], result['expires_in']))
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """
class Recorder():
    def __init__(self, chunk=1024, framerate=16000, NUM_SAMPLES=2000, channels=1, sampwidth=2):
        self.framerate = framerate
        self.NUM_SAMPLES = NUM_SAMPLES
        self.channels = channels
        self.sampwidth = sampwidth
        self.CHUNK = chunk
        self._running = True
        self._frames = []
# TIME=2

    def save(self, filename):
        '''save the date to the wavfile'''
        wf = wave.open(filename,'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.sampwidth)
        wf.setframerate(self.framerate)
        wf.writeframes(b"".join(self._frames))
        wf.close()

    def start(self):
        threading._start_new_thread(self.__recording, ())

    def __recording(self):

        p = PyAudio()
        stream = p.open(format=paInt16,
                        channels=self.channels,
                        rate=self.framerate,
                        input=True,
                        frames_per_buffer=self.NUM_SAMPLES)
        while self._running:
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop(self):
        self._running = False




def asr_request(AUDIO_FILE):
    speech_data = []
    with open(AUDIO_FILE, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        raise DemoError('file %s length read 0 bytes' % AUDIO_FILE)

    params = {'cuid': CUID, 'token': token, 'dev_pid': DEV_PID}
    params_query = urlencode(params)

    headers = {
        'Content-Type': 'audio/' + FORMAT + '; rate=' + str(RATE),
        'Content-Length': length
    }

    # print post_data
    req = Request(ASR_URL + "?" + params_query, speech_data, headers)
    try:
        begin = timer()
        f = urlopen(req)
        result_str = f.read()
        print("Request time cost %f" % (timer() - begin))
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()

    if (IS_PY3):
        result_str = str(result_str, 'utf-8')
    print(result_str)
    # with open("result.txt", "a") as of:
    #     of.write(result_str)
    return '.'.join(eval(result_str).get('result'))

def rasa_input(asr_result):
    res = requests.post('http://localhost:5002/webhooks/rest/webhook', json={'sender': 'default', 'message': asr_result})
    print(res.json())


if __name__ == '__main__':

    token = fetch_token()

    while True:
        try:
            input('请按任意键开始')
            # if a == 1:
            rec = Recorder()
            begin = time.time()
            # print("Start recording")
            rec.start()
            input('请按任意键结束')
            # if b == 2:
            # print("Stop recording")
            rec.stop()
            fina = time.time()
            t = fina - begin
            print('录音时间为%ds' % t)
            rec.save(AUDIO_FILE)
            rasa_input(asr_request(AUDIO_FILE))
        except Exception as e:
            print(e)