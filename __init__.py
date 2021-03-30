from mycroft import MycroftSkill, intent_file_handler


class Democroft(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('democroft.intent')
    def handle_democroft(self, message):
        self.speak_dialog('democroft')


def create_skill():
    return Democroft()

