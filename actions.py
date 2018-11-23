# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:15
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn


from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT, logger
from rasa_core_sdk.events import SlotSet, Form


class Action_Total(FormAction):

    RANDOMIZE = True
    request_intent = ''
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
        required_slots_mapping = {
            'request_patient_info':
                {'path1': ["department", "admission-time", "bed-number"],
                 'path2': ["patient-name", "admission-time"]},
            'request_patient_emr':
                {'path1': ["department", "admission-time", "bed-number"],
                 'path2': ["patient-name", "admission-time"]},
            'request_patient_detail':
                {'path1': ["department", "admission-time", "bed-number"],
                 'path2': ["patient-name", "admission-time"]},
            'request_patient_inspection_report':
                {'path1': ["department", "admission-time", "bed-number", "inspection-name"],
                 'path2': ["patient-name", "admission-time", "inspection-name"]},
            'request_patient_laboratory_report':
                {'path1': ["department", "admission-time", "bed-number", "inspection-time"],
                 'path2': ["patient-name", "admission-time", "inspection-time"]},
            'request_patient_laboratory_indicator':
                {'path1': ["department", "admission-time", "bed-number", "laboratory-indicator"],
                 'path2': ["patient-name", "admission-time", "laboratory-indicator"]},
            'request_patient_abnormal':
                {'path1': ["department", "admission-time", "bed-number"],
                 'path2': ["patient-name", "admission-time"]},
            'request_patient_Medical_order':
                {'path1': ["department", "admission-time", "bed-number", "order-name"],
                 'path2': ["patient-name", "admission-time", "order-name"]},
            'request_similar_patient':
                {'path1': ["department", "admission-time", "bed-number", "disease-name"],
                 'path2': ["patient-name", "admission-time", "disease-name"]},
            'request_related_literature':
                {'path1': ["department", "admission-time", "bed-number", "disease-name"],
                 'path2': ["patient-name", "admission-time", "disease-name"]},
            'request_related_guide':
                {'path1': ["department", "admission-time", "bed-number", "disease-name"],
                 'path2': ["patient-name", "admission-time", "disease-name"]},
            'request_collect':
                {'path1': [],
                 'path2': []},
        }
        if self.slots_filled.issubset({"department", "admission-time", "bed-number"}) and self.slots_filled:
            return required_slots_mapping.get(self.request_intent).get('path1')
        else:
            return required_slots_mapping.get(self.request_intent).get('path2')

    def slot_mappings(self):
        # return {"patient-name": self.from_entity(entity="patient-name",),
        #         "admission-time": self.from_entity(entity="admission-time", ),
        #         }
        return {"patient-name": self.from_entity(entity="patient-name",),
                "medical-record-number": self.from_entity(entity="medical-record-number",),
                "hospital-number": self.from_entity(entity="hospital-number", ),
                "department": self.from_entity(entity="department", ),
                "admission-time": self.from_entity(entity="time", ),
                "bed-number": self.from_entity(entity="bed-number", ),
                "inspection-name": self.from_entity(entity="inspection-name", ),
                "inspection-time": self.from_entity(entity="time", ),
                "laboratory-indicator": self.from_entity(entity="laboratory-indicator", ),
                "order-name": self.from_entity(entity="order-name", ),
                "disease-name": self.from_entity(entity="disease-name", ),
                "literature-name": self.from_entity(entity="literature-name", ),
                "guide-name": self.from_entity(entity="guide-name", ),
                }

    def validate(self, dispatcher, tracker, domain):
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
        def none_func():
            pass
        dispatcher.utter_template('utter_submit', tracker)
        # do sth
        intent2operate = {
            'request_patient_info':
                print('request_patient_info'),
            'request_patient_emr':
                print('request_patient_emr'),
            'request_patient_detail':
                print('request_patient_inspection_report'),
            'request_patient_inspection_report':
                print('request_patient_inspection_report'),
            'request_patient_laboratory_report':
                print('request_patient_laboratory_report'),
            'request_patient_laboratory_indicator':
                print('request_patient_laboratory_indicator'),
            'request_patient_abnormal':
                print('request_patient_abnormal'),
            'request_patient_Medical_order':
                print('request_patient_Medical_order'),
            'request_similar_patient':
                print('request_similar_patient'),
            'request_related_literature':
                print('request_related_literature'),
            'request_related_guide':
                print('request_related_guide'),
            'request_collect':
                print('request_collect'),
        }
        operate = intent2operate.get(self.request_intent, none_func)
        # return [Restarted()]
        # 若在此restart response的event执行后，预测后续action时,tracker已空
        return []

    def extract_other_slots(self,
                            dispatcher,  # type: CollectingDispatcher
                            tracker,  # type: Tracker
                            domain  # type: Dict[Text, Any]
                            ):
        # type: (...) -> Dict[Text: Any]
        """Extract the values of the other slots
            if they are set by corresponding entities from the user input
            else return None
        """
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)

        slot_values = {}
        for slot in self.required_slots(tracker):
            # look for other slots
            if slot != slot_to_fill:
                # list is used to cover the case of list slot type
                other_slot_mappings = self.get_mappings_for_slot(slot)

                for other_slot_mapping in other_slot_mappings:
                    intent = tracker.latest_message.get("intent",
                                                        {}).get("name")
                    # check whether the slot should be filled
                    # by entity with the same name
                    # should_fill_slot = (
                    #         other_slot_mapping["type"] == "from_entity" and
                    #         other_slot_mapping.get("entity") == slot and
                    #         self.intent_is_desired(other_slot_mapping,
                    #                                tracker)
                    # )
                    # 为了处理不同slot用同一entity抽取
                    should_fill_slot = (
                            other_slot_mapping["type"] == "from_entity" and
                            self.intent_is_desired(other_slot_mapping,
                                                   tracker)
                    )
                    if should_fill_slot:
                        # list is used to cover the case of list slot type
                        # value = list(tracker.get_latest_entity_values(slot))
                        value = list(tracker.get_latest_entity_values(other_slot_mapping.get("entity")))
                        if len(value) == 1:
                            value = value[0]

                        if value:
                            logger.debug("Extracted '{}' "
                                         "for extra slot '{}'"
                                         "".format(value, slot))
                            slot_values[slot] = value
                            # this slot is done, check  next
                            break

        return slot_values

    def _activate_if_required(self, tracker):
        if tracker.active_form.get('name') is not None:
            logger.debug("The form '{}' is active"
                         "".format(tracker.active_form))
        else:
            logger.debug("There is no active form")

        if tracker.active_form.get('name') == self.name():
            return []
        else:
            self.request_intent = tracker.latest_message.get('intent')['name']
            logger.debug("Activated the form '{}'".format(self.name()))
            return [Form(self.name())]

    def _deactivate(self):
        self.request_intent = ''
        self.slots_filled.clear()
        logger.debug("Deactivating the form '{}'".format(self.name()))
        return [Form(None), SlotSet(REQUESTED_SLOT, None)]

