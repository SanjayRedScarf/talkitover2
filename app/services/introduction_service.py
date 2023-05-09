from models import output_data
from utilities import html_helper

class IntroductionService:

    def __init__(self, next_user_input_option_types):
        self.next_user_input_option_types = next_user_input_option_types
        self._html_helper = html_helper.HtmlHelper()

    def get_introduction_output_data(self, conversation_input_data):

        introduction_output_data = ""
        number_of_response_fragments = ""

        client_id = conversation_input_data.client_id
        user_message = conversation_input_data.message
        initial_happiness_score = conversation_input_data.initial_happiness_score

        if conversation_input_data.section == 1:
            introduction_output_data = self.__get_section_one_output_data(initial_happiness_score, client_id)
        elif conversation_input_data.section == 2:
            introduction_output_data = self.__get_section_two_output_data(user_message, client_id)
        elif conversation_input_data.section == 3:
            introduction_output_data = self.__get_section_three_output_data(user_message, client_id)
        elif conversation_input_data.section == 3.5:
            introduction_output_data = self.__get_section_three_point_five_output_data(user_message, client_id)
        elif conversation_input_data.section == 4:
            introduction_output_data = self.__get_section_four_output_data(user_message, client_id)
        elif conversation_input_data.section == 5:
            introduction_output_data = self.__get_section_five_output_data(user_message, client_id)
        elif conversation_input_data.section == 6:
            introduction_output_data = self.__get_section_six_output_data(user_message, client_id)
        elif conversation_input_data.section == 7:
            introduction_output_data = self.__get_section_seven_output_data(user_message, client_id)
        elif conversation_input_data.section == 8:
            introduction_output_data = self.__get_section_eight_output_data(user_message, client_id)
        elif conversation_input_data.section == 9:
            introduction_output_data = self.__get_section_nine_output_data(user_message, client_id)
        elif conversation_input_data.section == 10:
            introduction_output_data = self.__get_section_ten_output_data(user_message, client_id)
        elif conversation_input_data.section == 11:
            introduction_output_data = self.__get_section_eleven_output_data(initial_happiness_score)
        
        return introduction_output_data

    def __get_section_one_output_data(self, initialHappinessScore, client_id):
        """
        Gets the output data for section one of the introduction
        """
        abort_conversation = False
        response = ""
        introduction_output_data = ""

        if initialHappinessScore > 7:
            response = ["Sounds like you're feeling OK! I'm designed for people who are feeling low \
            and have something on their mind. But you're feeling good, which is great! :-)", \
            "Or maybe you're just here to check out this site, which is cool. Why don't you refresh the page, but pretend you're feeling sad this time!"]
            abort_conversation = True
        elif initialHappinessScore > 3:
            response = "Thanks for sharing. Sounds like you're not quite on top of the world - shame about that. \
                Is there anything specific on your mind at the moment?"
        else:
            response = ["Oh dear, sounds like you're feeling really low, I'm sorry to hear that. ",
            "Is there something specific that's triggered this?"]

        if abort_conversation == False:
            next_user_options = ["Yes", "No"]

            next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it
            
            introduction_output_data = output_data.OutputData(response, 2, next_user_options, next_user_input, "userInputButton")
        
        elif abort_conversation == True:
            introduction_output_data = output_data.OutputData(response, -3, [""], "", "earlyAbort")

        return introduction_output_data

    def __get_section_two_output_data(self, user_message, client_id):
        """
        Gets the output data for section two of the introduction
        """
        if user_message.lower() == "yes":
            response = "I'd love to hear you say more about that. Before we do that, would you like me to explain about how this chatbot works?"
            
            next_user_options = ["Yes"] # this is the option that the user can select

            next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

            introduction_output_data = output_data.OutputData(response, 4, next_user_options, next_user_input, "userInputButton")

        else:
            response = "Do you feel this way often?"
            
            next_user_options = ["Yes", "No"] # this is the option that the user can select
            
            next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it
            
            introduction_output_data = output_data.OutputData(response, 3, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_three_output_data(self, user_message, client_id):
        """
        Gets the output data for section three of the introduction
        """
       
        if user_message.lower() == "yes":
            response = "Feeling this way often sounds pretty rubbish. I'm sorry about that. How long has it been like this?"
            
            next_user_options = [""] # n/a because next user input type is not buttons

            next_user_input = self.next_user_input_option_types.next_user_input_free_text

            introduction_output_data = output_data.OutputData(response, 3.5, next_user_options, next_user_input, "freeText")
        else:
            response = "I'd like to explore this more with you. Before we do that, I'd like to quickly explain how this chatbot works, if that's OK?"
            
            next_user_options = ["Yes, tell me how this bot works"] # this is the option that the user can select
            
            next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

            introduction_output_data = output_data.OutputData(response, 4, next_user_options, next_user_input, "userInputButton")
        
        return introduction_output_data

    def __get_section_three_point_five_output_data(self, user_message, client_id):
        """
        Gets the output data for section 3.5 of the introduction
        """
        response = "I'd like to hear more about that. Before we do that, I'd like to quickly explain how this chatbot works, if that's OK?"

        next_user_options = ["Yes, tell me how this bot works"] # this is the option that the user can select
        
        next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

        introduction_output_data = output_data.OutputData(response, 4, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_four_output_data(self, user_message, client_id):
        """
        Gets the output data for section four of the introduction
        """
        response = ["I'm actually a very simple little bot. So please feel free to talk to me, \
            and sorry in advance if I don't always do a good job of understanding you. ",
            "Instead think of this as being more like writing a journal, but as you keep writing, \
            I'll be here to encourage you to keep talking."]

        next_user_options = ["OK, I will talk with you even though you are a simple bot."] # this is the option that the user can select
        
        next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

        introduction_output_data = output_data.OutputData(response, 5, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_five_output_data(self, user_message, client_id):
        """
        Gets the output data for section five of the introduction
        """
        response = "So given that I can't track you down, and also because I'm a very simple bot, \
            if you told me about an emergency/crisis situation, I wouldn't \
            be able to help."
        
        next_user_options = ["OK, I know you cannot provide emergency services."] # this is the option that the user can select
        
        next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

        introduction_output_data = output_data.OutputData(response, 6, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_six_output_data(self, user_message, client_id):
        """
        Gets the output data for section six of the introduction
        """
        response = "Next I'm going to give you the choice whether you want to use this on a confidential \
            or anonymous basis. When I say anonymous, I mean that our boffins may see your text to help \
            us improve the way this software works, but we still won't know who you are."

        next_user_options = ["OK, I know what you mean by anonymous."] # this is the option that the user can select

        next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

        introduction_output_data = output_data.OutputData(response, 7, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_seven_output_data(self, user_message, client_id):
        """
        Gets the output data for section seven of the introduction
        """
        response = "And when I say confidential, I mean that your text won't be \
            stored at all, and no human will see what you write. This does, however, mean that you will be using a more simplified bot."

        next_user_options = ["OK, I know what you mean by confidential."] # this is the option that the user can select

        next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

        introduction_output_data = output_data.OutputData(response, 8, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_eight_output_data(self, user_message, client_id):
        """
        Gets the output data for section eight of the introduction
        """
        response = "Would you like this service to be anonymous or confidential?"

        next_user_options = ["Anonymous (my words can help improve the bot)", "Confidential (no human ever sees my words)"] # this is the option that the user can select

        next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

        introduction_output_data = output_data.OutputData(response, 9, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_nine_output_data(self, user_message, client_id):
        """
        Gets the output data for section nine of the introduction
        """
        response = "Thanks! One last thing: You remember saying how you felt on a scale from 1 to 10 \
            at the start? I'd like to ask you the same thing at the end so I know if we're helping."

        next_user_options = ["Yes, I am happy to let you see how I feel at the end too"] # this is the option that the user can select

        next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

        introduction_output_data = output_data.OutputData(response, 10, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_ten_output_data(self, user_message, client_id):
        """
        Gets the output data for section ten of the introduction
        """
        response = ""
        next_user_options = ""

        if client_id == "originalJavascriptClient":
            response = ["When you're finished using the bot, please click the stop button on the right \
                or just type 'stop'; this will take you to the super-quick final survey. ", "Don't press it now, but \
                can you press this button instead of closing/exiting this window?"]

            next_user_options = ["Yes, when I am finished I will click the stop button"] # this is the option that the user can select

        elif client_id == "bootstrapJavascriptClient":
            response = ["When you're finished using the bot, please click the stop button below \
                or just type 'stop'; this will take you to the super-quick final survey. ", "Don't press it now, but \
                can you press this button instead of closing/exiting this window?"]

            next_user_options = ["Yes, when I am finished I will click the stop button"] # this is the option that the user can select
        
        else: # this is assumed to be the guided track front end
            response = ["When you're finished using the bot, please type 'stop' in the text field \
                where the responses go, this will take you to the super-quick one-question final survey. \
                Please please do this, because we want to know if we are helping."]

            next_user_options = ["Yes, I agree to fill in the quick survey at the end. I'll type 'stop' in a text field."]

        next_user_input = self._html_helper.get_next_user_input_options_html(client_id, next_user_options) # this puts a string of html around it

        introduction_output_data = output_data.OutputData(response, 11, next_user_options, next_user_input, "userInputButton")

        return introduction_output_data

    def __get_section_eleven_output_data(self, initial_happiness_score):
        """
        Gets the output data for section eleven of the introduction
        """   
        response_fragment = self.__get_response_fragment_for_section_eleven(initial_happiness_score)

        response = "OK, now we've got the intro stuff out the way... you were saying before that \
            you were feeling "+str(initial_happiness_score)+" out of 10. "+response_fragment

        next_user_input = self.next_user_input_option_types.next_user_input_free_text 

        next_user_options = [""] # n/a because next user input type is not buttons
        
        introduction_output_data = output_data.OutputData(response, 12, next_user_options, next_user_input, "freeText")

        return introduction_output_data


    def __get_response_fragment_for_section_eleven(self, initial_happiness_score):
        """
        Gets the response fragment to add to the end of the core response based on the initial happiness score
        """
        response_fragment = ""

        if initial_happiness_score > 7:
            response_fragment = "Seems like you're feeling OK, but I'm still available for you \
                to chat with if you want. Maybe just start by talking about something that's on your mind?"
        elif initial_happiness_score > 3:
            response_fragment = "Would you like to start by talking about something that's on your mind?"
        else:
            response_fragment = "Sounds like things are tough for you just now. Would you like to \
                start talking about something that's on your mind?"
        
        return response_fragment

        