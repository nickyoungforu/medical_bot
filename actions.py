# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:15
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn


from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT, logger
from rasa_core_sdk.events import SlotSet, Form


class Action_Total(FormAction):

    RANDOMIZE = True
    required_slots_flag = -1
    slots_filled = set()
    def name(self):
        return 'request_form'

    # @staticmethod
    # def required_slots_mapping(tracker):
    #     last_entity = tracker.latest_message.get('entities')
    #     def validate_entity(entity):
    #         if entity:
    #             if set([k_v['entity'] for k_v in entity]).issubset({"department", "admission-time", "bed-number"}):
    #         pass
    #     return {
    #         1: 1
    #     }
    #     pass
    # 直接屏蔽基类method, 不重写
    def required_slots(self, tracker):
        slots = set([k for k, v in tracker.slots.items()])
        last_entity = tracker.latest_message.get('entities')
        required_slots_mapping = {
            0: {'path1': ["department", "admission-time", "bed-number"],
                'path2': ["patient-name", "admission-time"]},
            1: {'path1': ["department", "admission-time", "bed-number", "inspection-name"],
                'path2': ["patient-name", "admission-time", "inspection-name"]},
            2: {'path1': ["department", "admission-time", "bed-number", "inspection-time"],
                'path2': ["patient-name", "admission-time", "inspection-time"]},
            3: {'path1': ["department", "admission-time", "bed-number", "laboratory-indicator"],
                'path2': ["patient-name", "admission-time", "laboratory-indicator"]},
            4: {'path1': ["department", "admission-time", "bed-number", "order-name"],
                'path2': ["patient-name", "admission-time", "order-name"]},
            5: {'path1': ["department", "admission-time", "bed-number", "disease-name"],
                'path2': ["patient-name", "admission-time", "disease-name"]},
            6: {'path1': [],
                'path2': []},
            7: {'path1': ["department", "admission-time", "bed-number", "laboratory-indicator"],
                'path2': ["patient-name", "admission-time", "laboratory-indicator"]},
            -1: {'path1': None,
                 'path2': None},
        }
        # if self.slots_filled:
        if self.slots_filled.issubset({"department", "admission-time", "bed-number"}) and self.slots_filled:
            return required_slots_mapping[self.required_slots_flag]['path1']
        else:
            return required_slots_mapping[self.required_slots_flag]['path2']


    def request_next_slot(self,
                          dispatcher,
                          tracker,
                          domain
                          ):
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                dispatcher.utter_template("utter_ask_{}".format(slot), tracker)
                return [SlotSet(REQUESTED_SLOT, slot)]
        return None



    def slot_mappings(self):
        # return {"patient-name": self.from_entity(entity="patient-name",),
        #         "admission-time": self.from_entity(entity="admission-time", ),
        #         }
        return {"patient-name": self.from_entity(entity="patient-name",),
                "medical-record-number": self.from_entity(entity="medical-record-number",),
                "hospital-number": self.from_entity(entity="hospital-number", ),
                "department": self.from_entity(entity="department", ),
                "admission-time": self.from_entity(entity="admission-time", ),
                "bed-number": self.from_entity(entity="bed-number", ),
                "inspection-name": self.from_entity(entity="inspection-name", ),
                "inspection-time": self.from_entity(entity="inspection-time", ),
                "laboratory-indicator": self.from_entity(entity="laboratory-indicator", ),
                "order-name": self.from_entity(entity="order-name", ),
                "disease-name": self.from_entity(entity="disease-name", ),
                "literature-name": self.from_entity(entity="literature-name", ),
                "guide-name": self.from_entity(entity="guide-name", ),
                }


    def validate(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
        self.slots_filled.update([entities['entity'] for entities in tracker.latest_message.get('entities')])
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                               "Failed to validate slot {0} "
                                               "with action {1}"
                                               "".format(slot_to_fill,
                                                         self.name()))

        '''
        预留做数据校验
        for slot, value in slot_values.items():
            if slot == 'patient-name':
                pass

            elif slot == 'num_people':
                pass

            elif slot == 'sth...':
                pass
        '''

        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]

    def submit(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
        """Define what the form has to do
            after all required slots are filled"""

        # utter submit template
        dispatcher.utter_template('utter_submit', tracker)
        # return [Restarted()]
        # 若在此restart response的event执行后，预测后续action时,tracker已空
        return []

    def _activate_if_required(self, tracker):
        if tracker.active_form.get('name') is not None:
            logger.debug("The form '{}' is active"
                         "".format(tracker.active_form))
        else:
            logger.debug("There is no active form")

        if tracker.active_form.get('name') == self.name():
            return []
        else:
            if tracker.latest_message.get('intent')['name'] in ['request_patient_info', 'request_patient_emr', 'request_patient_detail']:
                self.required_slots_flag = 0
            elif tracker.latest_message.get('intent')['name'] == 'request_patient_inspection_report':
                self.required_slots_flag = 1
            elif tracker.latest_message.get('intent')['name'] == 'request_patient_laboratory_report':
                self.required_slots_flag = 2
            elif tracker.latest_message.get('intent')['name'] == 'request_patient_abnormal':
                self.required_slots_flag = 3
            elif tracker.latest_message.get('intent')['name'] == 'request_patient_Medical_order':
                self.required_slots_flag = 4
            elif tracker.latest_message.get('intent')['name'] == ['request_similar_patient', 'request_related_literature', 'request_related_guide']:
                self.required_slots_flag = 5
            elif tracker.latest_message.get('intent')['name'] == 'request_collect':
                self.required_slots_flag = 6
            elif tracker.latest_message.get('intent')['name'] == 'request_patient_laboratory_indicator':
                self.required_slots_flag = 7
            else:
                self.required_slots_flag = -1
            logger.debug("Activated the form '{}'".format(self.name()))
            return [Form(self.name())]

    def _deactivate(self):
        self.required_slots_flag = -1
        self.slots_filled.clear()
        logger.debug("Deactivating the form '{}'".format(self.name()))
        return [Form(None), SlotSet(REQUESTED_SLOT, None)]

