from models import output_data
from utilities import html_helper

class EndOfConversation:
    def __init__(self, next_user_input_option_types):
        self.next_user_input_option_types = next_user_input_option_types
        self._html_helper = html_helper.HtmlHelper()

    def get_initial_conversation_end_output_data(self, initial_happiness_score):

        response = "Thank you for using this bot. Please rate how you feel on a scale \
                from 1 to 10, where 1 is terrible and 10 is great. As a reminder, the score you \
                gave at the start was "+str(initial_happiness_score)

        next_user_options = [""] # n/a because next user input type is not buttons

        next_user_input = self.next_user_input_option_types.next_user_input_final_happiness_survey # this puts a string of html around it

        conversation_end_output_data = output_data.OutputData(response, -1, next_user_options, next_user_input, "finalHappinessSurvey")

        return conversation_end_output_data

    def get_section_minus_one_output_data(self, initial_happiness_score, final_happiness_score):
        
        response = self.__get_happiness_change_response(initial_happiness_score, final_happiness_score)

        next_user_options = [""] # n/a because next user input type is not buttons

        next_user_input = self.next_user_input_option_types.next_user_input_free_text

        conversation_end_output_data = output_data.OutputData(response, -2, next_user_options, next_user_input, "freeText")

        return conversation_end_output_data

    def get_section_minus_two_output_data(self):

        response = "Thank you for your feedback, and thank you for using the Talk It Over chatbot."

        next_user_options = [""] # n/a because next user input type is not buttons

        conversation_end_output_data = output_data.OutputData(response, -3, next_user_options, "", "")
        
        return conversation_end_output_data
    
    def __get_happiness_change_response(self, initial_happiness_score, final_happiness_score):
        
        response = ""
        
        happiness_change = final_happiness_score - initial_happiness_score

        if happiness_change < 0:
            response = "Oh no! I'm so sorry you're feeling worse than you were at the start! :-(. \
                Please tell us why we made things worse, and what we could do better in future"
        elif happiness_change == 0:
            response = "We wanted to make things better for you, sorry you're feeling no better than \
                you did at the start. Optional final question - Please tell us whether we met your \
                expectations, and any suggestions for improvement."
        elif happiness_change > 0:
            response = "I'm glad you're feeling better than you did at the start. Optional final question: \
                if you have any comments to help us improve this bot, please make them here"

        return response