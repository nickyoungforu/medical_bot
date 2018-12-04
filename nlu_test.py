# -*- coding: utf-8 -*-
# @Time    : 18-11-6 下午4:53
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn


from rasa_nlu.model import Interpreter
from rasa_nlu.extractors.crf_entity_extractor import CRFEntityExtractor
from rasa_nlu import registry

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