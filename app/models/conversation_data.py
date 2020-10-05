class ConversationData:
    def __init__(self, message, section, initial_happiness_score, final_happiness_score, anonymous, conversation_id, client_id):
        self.message = message
        self.section = section
        self.initial_happiness_score = initial_happiness_score
        self.final_happiness_score = final_happiness_score
        self.anonymous = anonymous
        self.conversation_id = conversation_id
        self.client_id = client_id

