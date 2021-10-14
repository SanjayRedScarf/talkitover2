class UserInputs:
    def __init__(self, anonymous, conversation_id, message, response, section, client_id,ai_data ={}):
        self.anonymous = anonymous
        self.conversation_id = conversation_id
        self.message = message
        self.response = response
        self.section = section
        self.client_id = client_id
        self.ai_data = ai_data