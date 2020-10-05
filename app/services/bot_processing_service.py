from datetime import datetime
from services import introduction_service, end_of_conversation_service, main_conversation_service
from utilities import response_fragments_helper, html_helper, data_preparation_helper
from repositories import conversation_data_repository
from models import user_inputs, tio_outputs

class BotProcessingService:

    def process_user_input(self, conversation_input_data):

        _response_fragments_helper = response_fragments_helper.ResponseFragmentsHelper()
        _html_helper = html_helper.HtmlHelper()
        _data_preparation_helper = data_preparation_helper.DataPreparationHelper()
        _conversation_data_repository = conversation_data_repository.ConversationDataRepository()

        next_user_input_option_types = _html_helper.get_next_user_input_option_types_html(conversation_input_data.client_id)
        _introduction_service = introduction_service.IntroductionService(next_user_input_option_types)
        _conversation_end_service = end_of_conversation_service.EndOfConversation(next_user_input_option_types)
        _main_conversation_service = main_conversation_service.MainConversationService(next_user_input_option_types)

        next_user_input_type = "initialHappinessSurvey" # the javascript code needs to pull in the data entered by the user in the userInput div and then spit the same data back out again. The way to retrieve this depends on whether the userinput mechanism was a button or a free text field, so this boolean helps to track that. It feeds through to a variable called currentUserInputType in the javascript code

        number_of_response_fragments = ""

        conversation_id = str(datetime.now())

        if ((conversation_input_data.section > 0) and (conversation_input_data.section <= 11)):
            
            # user_inputs_data = ""

            output_data = _introduction_service.get_introduction_output_data(conversation_input_data)

            number_of_response_fragments = _response_fragments_helper.get_response_fragments_count(output_data.response)

            prepared_response = _data_preparation_helper.prepare_response_for_data_store(output_data.response, number_of_response_fragments)            

            # Specific logic to set user_inputs_data object in section 1 of the introduction to something slightly different to the other introduction sections
            if conversation_input_data.section == 1:
                user_inputs_data = user_inputs.UserInputs(conversation_input_data.anonymous, conversation_id, "initialHappinessScore (!!) = "+conversation_input_data.message, prepared_response, conversation_input_data.section, conversation_input_data.client_id)
            else:
                user_inputs_data = user_inputs.UserInputs(conversation_input_data.anonymous, conversation_id, conversation_input_data.message, prepared_response, conversation_input_data.section, conversation_input_data.client_id)

            # Specific logic to set anonymous boolean in section 9 of the introduction
            if conversation_input_data.section == 9:
                conversation_input_data.anonymous == "true" if conversation_input_data.message.split()[0].lower()=="anonymous" else "false"

            _conversation_data_repository.insert_data(user_inputs_data)

        elif conversation_input_data.section > 11:

            user_character_count = 0
            user_character_count += len(conversation_input_data.message)

            if(conversation_input_data.message.lower()=="stop"):
                output_data = _conversation_end_service.get_initial_conversation_end_output_data(conversation_input_data.initial_happiness_score)            
            
            else:
                output_data = _main_conversation_service.get_main_conversation_output_data(conversation_input_data, user_character_count)

            number_of_response_fragments = _response_fragments_helper.get_response_fragments_count(output_data.response)

            prepared_response = _data_preparation_helper.prepare_response_for_data_store(output_data.response, number_of_response_fragments)            

            user_inputs_data = user_inputs.UserInputs(conversation_input_data.anonymous, conversation_id, conversation_input_data.message, prepared_response, conversation_input_data.section, conversation_input_data.client_id)

            _conversation_data_repository.insert_data(user_inputs_data)

        elif conversation_input_data.section == -1:
            output_data = _conversation_end_service.get_section_minus_one_output_data(conversation_input_data.initial_happiness_score, conversation_input_data.final_happiness_score)
                
            number_of_response_fragments = _response_fragments_helper.get_response_fragments_count(output_data.response)
            
            user_inputs_data = user_inputs.UserInputs("true", conversation_id, "finalHappinessScore (!!) = "+conversation_input_data.message, output_data.response, conversation_input_data.section, conversation_input_data.client_id) # the "anonymous" variable is hardcoded as true here, because we're going to store this data regardless of whether the user has said anonymous or confidential

            _conversation_data_repository.insert_data(user_inputs_data) 

        elif conversation_input_data.section == -2: # this is the "end" (i.e. user has entered "stop") section
            output_data = _conversation_end_service.get_section_minus_two_output_data()
                
            number_of_response_fragments = _response_fragments_helper.get_response_fragments_count(output_data.response)
            
            user_inputs_data = user_inputs.UserInputs("true", conversation_id, conversation_input_data.message, output_data.response, conversation_input_data.section, conversation_input_data.client_id) # the "anonymous" variable is hardcoded as true here, because we're going to store this data regardless of whether the user has said anonymous or confidential

            _conversation_data_repository.insert_data(user_inputs_data) 

        tio_outputs_data = tio_outputs.TioOutputs(output_data, number_of_response_fragments, conversation_input_data.anonymous, conversation_id)

        return tio_outputs_data