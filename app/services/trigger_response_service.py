import random
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

    
        if trigger != 'encouragingNoises':
            response = list(filter(lambda x:(x['char_count_condition'] == '<1000'),response_dict[trigger]))[0]['response']

        elif (" " not in user_message or len(user_message) < 10) and (user_character_count < 40 and session['short_msg_count'] < 2):
            ### If it's the user's first written response and they've given  (essentially) a one-word message, or maybe something without spaces (e.g. typing gibberish like usanvoiudvuvufdsiudsbca)
            ### When I say one-word message, I mean that either it is short, or something that might be longer but has no space characters (this includes someone typing gibberish)
            response = "I see you've said something very short there, which is cool :-). But feel free to type full sentences if you want. Just write about whatever's on your mind -- I'm here to listen."
            
            print ('user_character_count in trigger_response_service in elif:',user_character_count)
            print('short_msg_count:',session['short_msg_count'])
            
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
