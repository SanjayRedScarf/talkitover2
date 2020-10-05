class TioOutputs:
    def __init__(self, introduction_output_data, number_of_response_fragments, anonymous, conversation_id):
        self.response = introduction_output_data.response
        self.number_of_response_fragments = number_of_response_fragments
        self.next_section = introduction_output_data.next_section
        self.next_user_options = introduction_output_data.next_user_options
        self.next_user_input = introduction_output_data.next_user_input
        self.next_user_input_type = introduction_output_data.next_user_input_type
        self.anonymous = anonymous
        self.conversation_id = conversation_id