# -*- coding: utf-8 -*-
# @Time    : 18-11-7 下午4:15
# @Author  : nick
# @Email   : zhiyuan.chen@wowjoy.cn


from rasa_core_sdk import ActionExecutionRejection
from rasa_core_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_core_sdk.events import SlotSet, Restarted


class Action_Total(FormAction):

    RANDOMIZE = True

    def name(self):
        return 'request_form'

    @staticmethod
    def required_slots(tracker):
        # slots = set([k for k, v in tracker.slots if v])
        # if tracker.latest_message['intent'] == 'request_patient_info':
        #     if slots.issubset({"patient-name", "admission-time"}):
        #         return ["patient-name", "admission-time"]
        #     elif slots.issubset({"department", "admission-time", "bed-number"}):
        #         return ["department", "admission-time", "bed-number"]
        return ["patient-name", "admission-time"]

    def slot_mappings(self):
        return {"patient-name": self.from_entity(entity="patient-name",),
                "admission-time": self.from_entity(entity="admission-time", ),
                }
        # return {"patient-name": self.from_entity(entity="patient-name",),
        #         "medical-record-number": self.from_entity(entity="medical-record-number",),
        #         "hospital-number": self.from_entity(entity="hospital-number", ),
        #         "department": self.from_entity(entity="department", ),
        #         "admission-time": self.from_entity(entity="admission-time", ),
        #         "bed-number": self.from_entity(entity="bed-number", ),
        #         "inspection-name": self.from_entity(entity="inspection-name", ),
        #         "inspection-time": self.from_entity(entity="inspection-time", ),
        #         "laboratory-indicator": self.from_entity(entity="laboratory-indicator", ),
        #         "order-name": self.from_entity(entity="order-name", ),
        #         "disease-name": self.from_entity(entity="disease-name", ),
        #         "literature-name": self.from_entity(entity="literature-name", ),
        #         "guide-name": self.from_entity(entity="guide-name", ),
        #         }


    def validate(self, dispatcher, tracker, domain):
        # type: (CollectingDispatcher, Tracker, Dict[Text, Any]) -> List[Dict]
        """Validate extracted requested slot
            else reject the execution of the form action
        """
        # extract other slots that were not requested
        # but set by corresponding entity
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
