# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


#This is a simple example for a custom action which utters "Hello World!"

import logging, requests
from typing import Any, Text, Dict, List
from requests.exceptions import HTTPError

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    Form,
    UserUtteranceReverted,
    ConversationPaused,
    EventType,
)

logger = logging.getLogger(__name__)

class ActionHelloWorld(Action):


    def __init__(self):
        super().__init__()
        self._counter = 0
        # print('debug: ActionHelloWorld initialized')

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        self._counter += 1
        dispatcher.utter_message(text=f"Hallo Welt {self._counter}")

        # test add tag in rasa x
        endpoint = f"http://localhost:5002/api/conversations/{tracker.sender_id}/tags"
        label = '[{"value":"tag added by action","color":"00FF00"}]'
        try:
            response = requests.post(url=endpoint, data=label)
            response.raise_for_status()
        except Exception as err:
            logger.debug(f"error: {err}")  


class ActionMoveSlotMapping(Action):

    def __init__(self):
        super().__init__()

    def name(self) -> Text:
        return "action_move_slot_mapping"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city_from, city_to = 'unknown', 'unknown'

        for city in tracker.get_latest_entity_values(entity_type="city", entity_role='from'):
            city_from = city
            break

        for city in tracker.get_latest_entity_values(entity_type="city", entity_role='to'):
            city_to = city
            break
        
        return [SlotSet("city_from", city_from), SlotSet("city_to", city_to)]
        