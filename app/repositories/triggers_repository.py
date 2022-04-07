import os, json
from flask import current_app, session
import random


class TriggersRepository:

    def get_triggers_dictionary(self):
        """
        Creates a dictionary of triggers.
        """
        current_directory = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(current_directory, 'app/multi_triggers.json')

        triggers = ""

        with open(filename) as json_file: 
            triggers = json.load(json_file) 

        return triggers
            

    def get_encouraging_noises_random_response(self):
        """
        Gets a random response from the encouraging noises array.
        """
        triggers_dict = session['TRIGGERS_DICT']

        encouraging_noises_array = triggers_dict["encouragingNoises"]['triggers']

        return random.choice(encouraging_noises_array)
        
    def remove_used_trigger(self, trigger):
        """
        Removes a given trigger from the trigger dictionary so that it is not repeated.
        """
        triggers_dict = session['TRIGGERS_DICT']

        # The below list exists as some of the triggers should not be removed due to the importance of them or because they have common everyday responses.
        removal_exclusion_list = ["encouragingNoises"]

        if trigger not in removal_exclusion_list:
            del triggers_dict[trigger]
            session['TRIGGERS_DICT'] = triggers_dict
        
        return None