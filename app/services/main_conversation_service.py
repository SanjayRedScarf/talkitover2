from services import string_cleansing_service, trigger_check_service, trigger_response_service
from repositories import triggers_repository
from threading import Thread
from models import output_data
import ast

class MainConversationService:

    def __init__(self, next_user_input_option_types):
        self.next_user_input_option_types = next_user_input_option_types

    def get_main_conversation_output_data(self, conversation_input_data, user_character_count,sentence_encoder):
        
        _string_cleansing_service = string_cleansing_service.StringCleansingService()
        _trigger_check_service = trigger_check_service.TriggerCheckService()
        _trigger_response_service = trigger_response_service.TriggerResponseService()
        _trigger_repository = triggers_repository.TriggersRepository()

        cleaned_message = _string_cleansing_service.clean_string(conversation_input_data.message)

        trigger = _trigger_check_service.get_trigger(cleaned_message)
        response = _trigger_response_service.get_response_for_trigger(cleaned_message, trigger, user_character_count)            

        if trigger == 'encouragingNoises':
            try:
                ai_data = sentence_encoder.get_cat(cleaned_message)
                trigger = ai_data['max_over_thresh']
                out_cat, response = sentence_encoder.guse_response(trigger)
                #if out_cat not in ai_repeat:
                if out_cat == 'Abuse':
                    response = ast.literal_eval(response)
                    #ai_repeat.append(out_cat)
                elif out_cat == None:
                    trigger == 'encouragingNoises'
                    response = _trigger_response_service.get_response_for_trigger(cleaned_message, trigger, user_character_count)
            except Exception as e:
                print(e)
                trigger == 'encouragingNoises'
                response = _trigger_response_service.get_response_for_trigger(cleaned_message, trigger, user_character_count)

        # Remove from dictionary as response has now been used and we do not want it to be repeated.
        if type(trigger) != dict:
            Thread(target=_trigger_repository.remove_used_trigger(trigger)).start()

        next_user_input = self.next_user_input_option_types.next_user_input_free_text

        return output_data.OutputData(response, conversation_input_data.section, [""], next_user_input, "freeText")

        