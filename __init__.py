from mycroft import MycroftSkill, intent_file_handler
from adapt.intent import IntentBuilder
import requests
import json
from requests.compat import urljoin
import uuid

class Democroft(MycroftSkill):

    def initialize(self):
    # Set the address of your Rasa's REST endpoint
        self.conversation_active = False
        self.convoID = 100
        self.messages = []
        self.url="https://pfxsbjmewe.execute-api.us-east-1.amazonaws.com/dev/send?"

    def query(self, prompt=None):
        if self.conversation_active == False:
            return
        if prompt is None and len(self.messages) > 0:
            prompt = self.messages
        # Speak message to user and save the response
        msg = self.get_response(prompt, num_retries=0)
        self.log.warning(msg)
        # If user doesn't respond, quietly stop, allowing user to resume later
        if msg is None:
           self.log.warning("inside msg == NONE") 
           return
        if msg == "stop":
           session = self.url+"uid ="+str(self.convoID)+"&text=clear session"
           r = requests.get(session)
           #r-----> Error Handling to be done
           self.speak("Thank You for interacting with bot")
           self.speak("Now exiting")

           return 
         # Else reset messages
        #self.messages = []
        # Send post requests to said endpoint using the below format.
        # "sender" is used to keep track of dialog streams for different users
        # data = requests.post(
        #     self.RASA_API, json = {"message" : msg, "sender" : "user{}".format(self.convoID)}
        # )
        # A JSON Array Object is returned: each element has a user field along
        # with a text, image, or other resource field signifying the output
        # print(json.dumps(data.json(), indent=2))
        #for next_response in data.json():
        #    if "text" in next_response:
        #        self.messages.append(next_response["text"])
        # Output all but one of the Rasa dialogs
        #if len(self.messages) > 1:
        #    for rasa_message in self.messages[:-1]:
    #            self.log.warning(rasa_message)
    
        # Kills code when Rasa stop responding
     #   if len(self.messages) == 0:
      #      self.messages = ["no response from rasa"]
       #     return
        # Use the last dialog from Rasa to prompt for next input from the user
        # Allows a stream of user inputs by re-calling query_rasa recursively
        # It will only stop when either user or Rasa stops providing data

        #url1=urljoin(self.url,"?uid=100")
        #self.log.warning("url1:"+url1)
        #url2 = urljoin(url1,"&text=")
        # self.log.warning("url2:"+url2)
        #url3 = urljoin(url2,msg)
        url3 = self.url+"uid ="+str(self.convoID)+"&text="+msg
        self.log.warning("url3:"+url3)
        self.log.warning(url3)
        self.log.warning("prompt" + msg)
        r = requests.get(url3)
        t = r.json()
        self.log.warning(t)
        return_msg=t['data']['message']
        self.log.warning(return_msg)
        self.log.warning(r)
        return self.query(return_msg)

    @intent_file_handler('democroft.intent')
    def handle_democroft(self, message):
        self.convoID = uuid.uuid1()
        self.conversation_active = True
        prompt = "Ask something"
        self.query(prompt)
    
    @intent_file_handler('resume.intent')
    def handle_resume_chat(self, message):
        self.conversation_active = True
        prompt = "Say something"
        self.query(prompt)

def create_skill():
    return Democroft()

