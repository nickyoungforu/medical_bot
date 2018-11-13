# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:15
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn


from rasa_core_sdk.forms import FormAction, EntityFormField
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk import endpoint


class Action_Total(FormAction):

    RANDOMIZE = True

    def name(self):
        return 'action_total'


    pass