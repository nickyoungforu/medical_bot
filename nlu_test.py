# -*- coding: utf-8 -*-
# @Time    : 18-11-6 下午4:53
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn


from rasa_nlu.model import Interpreter
import json
interpreter = Interpreter.load("./models/nlu/current")
while True:
    try:
        inputs = input('inputs:')
        message = inputs
        result = interpreter.parse(message)
        print(json.dumps(result, indent=2))
    except Exception as e:
        pass