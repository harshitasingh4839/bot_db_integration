

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []




import pymongo
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionCheckClient(Action):

    def name(self):
        return "action_check_client"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict):
        
        # Get the name of the person from the user's input
        client_name = tracker.get_slot('person')
        
        # MongoDB connection
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["meeting_scheduling"]
        collection = db["clients"]

        # Query the database
        result = collection.find_one({"name": client_name})
        
        if result:
            email = result['email']
            dispatcher.utter_message(f"Yes, {client_name} is our client. Their email is {email}.")
            return [SlotSet("client_email", email)]
        else:
            dispatcher.utter_message(f"I'm sorry, but {client_name} is not in our client database.")
            return [SlotSet("client_email", None)]