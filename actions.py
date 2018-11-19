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
        return ["patient-name", "admission-time"]

    def slot_mappings(self):
        return {"patient-name": self.from_entity(entity="patient-name",
                                            ),
                "admission-time": self.from_entity(entity="admission-time",
                                                ),}


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
        dispatcher.utter_template('utter_slots_values', tracker)
        return []
        # return [Restarted()]

    def run(self, dispatcher, tracker, domain):

        # activate the form
        events = self._activate_if_required(tracker)
        # validate user input
        events.extend(self._validate_if_required(dispatcher, tracker, domain))

        # create temp tracker with populated slots from `validate` method
        temp_tracker = tracker.copy()
        for e in events:
            if e['event'] == 'slot':
                temp_tracker.slots[e["name"]] = e["value"]

        next_slot_events = self.request_next_slot(dispatcher, temp_tracker,
                                                  domain)
        if next_slot_events is not None:
            # request next slot
            events.extend(next_slot_events)
        else:
            # there is nothing more to request, so we can submit
            events.extend(self.submit(dispatcher, temp_tracker, domain))
            # deactivate the form after submission
            events.extend(self._deactivate())
            events.extend([Restarted()])

        return events