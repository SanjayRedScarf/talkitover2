from http.client import ResponseNotReady
from pydoc import resolve
import random
from sklearn.model_selection import StratifiedShuffleSplit

from torch import heaviside
from repositories import triggers_repository
from flask import session

class TriggerResponseService:

    def get_response_for_trigger(self, user_message, trigger, user_character_count):
        """
        Gets the response for a given trigger.
        """
        response = self.__find_response(user_message, trigger, user_character_count)

        if not response:
            _triggers_repository = triggers_repository.TriggersRepository()

            response = _triggers_repository.get_encouraging_noises_random_response()

        return response


    def __find_response(self, user_message, trigger, user_character_count):
        """
        Finds the response for a given trigger.
        """
        if not session['response_modifier']['suicidal']:
            session['response_modifier']['suicidal'] = self.__is_user_suicidal(trigger)

        if not session['response_modifier']['lonely']:
            session['response_modifier']['lonely'] = self.__is_user_lonely(trigger)

        if not session['response_modifier']['hate_looks']:
            session['response_modifier']['hate_looks'] = self.__is_user_hates_looks(trigger)
 
        response_dict = session['RESPONSE_DICT']

        response = ""


        flags = {k:v for k,v in session['response_modifier'].items() if v}
    
        if trigger != 'encouragingNoises':
            trigger_flags = [response_dict[trigger][x]['flag'] for x in range(len(response_dict[trigger])) if response_dict[trigger][x]['flag'] != None]

            single_response_dict = list(filter(lambda x:(user_character_count in range(x['char_count'][0],x['char_count'][1])) and 
            (len(user_message) in range(x['msg_len'][0],x['msg_len'][1])),response_dict[trigger]))
            
            if any(x in trigger_flags for x in flags) and len(single_response_dict)> 1:
                single_response_dict = list(filter(lambda x:flags.get(x['flag'],False),single_response_dict))
            
            elif len(single_response_dict)> 1:
                single_response_dict = list(filter(lambda x:x['flag']==None,single_response_dict))

            if trigger[:12] == 'thisBotIsBad' and not user_message.isupper():
                single_response_dict = single_response_dict[1]
            else:
                try:
                    single_response_dict = single_response_dict[0]
                except:
                    response = ""


            if len(single_response_dict) > 0:
                if session['qheavy']:
                    if session['no_char_count']:
                        response = single_response_dict['qheavy_nochar_response']
                    else:
                        response = single_response_dict['qheavy_response']
                else:
                    if session['no_char_count']:
                        response = single_response_dict['qlight_nochar_response']
                    else:
                        response = single_response_dict['qlight_response']

                if single_response_dict['random'] == 'random':
                    response = random.choice(response)


        elif (" i deserve" in user_message.lower() or user_message.lower()[:9] == "i deserve"):
            response = "I just want to take a moment to assert that you are a valuable human being in your right, no matter what"

        elif " feeling " in user_message.lower():
            response = "Thank you for sharing this. Could you tell me more about your feelings please?"
        
        elif (" " not in user_message or len(user_message) < 10) and (user_character_count < 40 and session['short_msg_count'] < 2):
            ### If it's the user's first written response and they've given  (essentially) a one-word message, or maybe something without spaces (e.g. typing gibberish like usanvoiudvuvufdsiudsbca)
            ### When I say one-word message, I mean that either it is short, or something that might be longer but has no space characters (this includes someone typing gibberish)
            response = "I see you've said something very short there, which is cool :-). But feel free to type full sentences if you want. Just write about whatever's on your mind -- I'm here to listen."
            
            session['short_msg_count'] += 1
        
        
        return response

    def __is_user_suicidal(self, trigger):
        """
        Checks if the user is suicidal.
        """

        is_suicidal_triggers_list = ["iWantToKillMyself", "iWantToDie", "imFeelingSuicidal", "imFeelingQuiteSuicidal", "suicidalThoughts", "iveBecomeSuicidal"]

        if trigger in is_suicidal_triggers_list:
            return True
        
        return False
    def __is_user_lonely(self,trigger):
        '''
        Checks if the user is lonely
        '''
        lonely_list = ['feelingLonely']

        if trigger in lonely_list:
            return True
        False
        
    def __is_user_hates_looks(self,trigger):
        '''
        Checks if the user hates their looks/feels ugly
        '''
        hate_looks_list = ['iHateHowILook']

        if trigger in hate_looks_list:
            return True
        return False
