class OutputData:
    def __init__(self, response, next_section, next_user_options, next_user_input, next_user_input_type,ai_data = {},response_type = None):
        self.response = response
        self.next_section = next_section
        self.next_user_options = next_user_options
        self.next_user_input = next_user_input
        self.next_user_input_type = next_user_input_type
        self.ai_data = ai_data
        self.response_type = response_type