from flask import current_app,session
from services import string_cleansing_service

class TriggerCheckService:
    def __init__(self):
        self.triggers_dictionary = session['TRIGGERS_DICT']
        print(len(self.triggers_dictionary))
        # The exclusion list below is for arrays that don't need to be checked as they are for other functionality or have their own specific checking function
        self.exclusion_list = ["encouragingNoises", "itsNotThat", "leadString", "thisBotIsBadtight", "hello", "msgIsQuestion", "help","stopSynonyms"] 
        # The exclusion list below is for arrays that don't need the lead string check
        self.lead_string_exclusion_list = ["imUseless", "imWorthless"]
        # The exclusion list below is for arrays that have a different way of checking the negating string
        self.negating_string_exclusion_list = ["letMyselfDown", "abandonedMe"]
        self._string_cleansing_service = string_cleansing_service.StringCleansingService()

    def get_trigger(self, message, uncleaned_message):
        """
        Determines the trigger for the user's message.
        """
        # if nothing is triggered, encouraging noises array will be used by default
        trigger = "encouragingNoises"
        has_triggered = False

        for (key, value) in self.triggers_dictionary.items():
            if key not in self.exclusion_list:
                has_triggered = self.__check_user_message(key, value, message, has_triggered)
            elif key == "thisBotIsBadtight":
                has_triggered = self.__check_this_bot_is_bad_tight(message, has_triggered)
            elif key == "hello":
                for item in self.triggers_dictionary["hello"]:
                    if item == message:
                        has_triggered = True
            elif key == "help":
                for item in self.triggers_dictionary["help"]:
                    if item == message:
                        has_triggered = True
            elif key == "stopSynonyms":
                for item in self.triggers_dictionary["stopSynonyms"]:
                    if item == message:
                        has_triggered = True
            elif key == "msgIsQuestion":
                has_triggered = self.__check_message_is_question(uncleaned_message, has_triggered)
            if has_triggered:
                trigger = key
                break

        return trigger
    

    def __check_user_message(self, trigger_name, trigger_synonyms_array, message, has_triggered):
        """
        Checks the user's message against the given trigger array.
        """
        for string in trigger_synonyms_array:
            clean_string = self._string_cleansing_service.clean_string(string)

            if clean_string.lower().replace(" ","") in message.lower().replace(" ","") or clean_string.lower().replace(" ","") == message.lower().replace(" ",""):
                has_triggered = True

            has_triggered = self.__check_negating_string(trigger_name, has_triggered, message, clean_string)
            
            has_triggered = self.__check_lead_string(trigger_name, has_triggered, message, clean_string, trigger_synonyms_array)


            if has_triggered:
                break
            
        return has_triggered

    def __check_negating_string(self, trigger_name, has_triggered, message, string):
        """
        Checks if the string has "it's not that" or something similar before it.
        """
        its_not_that_array = self.triggers_dictionary['itsNotThat']

        for negating_string in its_not_that_array:

            negated_string_array = []

            if trigger_name not in self.negating_string_exclusion_list:
                negated_string_array = [negating_string.lower() + string]
            else:
                negated_string_array = [negating_string.lower()+string, negating_string.lower() + "i" + string] 
            
            for negated_string in negated_string_array:
                clean_negated_string = self._string_cleansing_service.clean_string(negated_string)
                if clean_negated_string.replace(" ","") in message.lower().replace(" ",""):
                    has_triggered = False

        return has_triggered

    def __check_lead_string(self, trigger_name, has_triggered, message, string, trigger_synonyms_array):
        """
        If the trigger is hit even when a lead string (like "I'm") is omitted, then that still counts
        """
        if trigger_name not in self.lead_string_exclusion_list:
            lead_string_array = self.triggers_dictionary['leadString']

            for lead_string in lead_string_array:
                if string.startswith(lead_string.lower()):
                    shortened_string = string.replace(lead_string,"")
                    if message.lower().replace(" ","").startswith(shortened_string.replace(" ","")):
                        has_triggered = True

        return has_triggered

    def __check_this_bot_is_bad_tight(self, message, has_triggered):
        """
        Checks the user's message against the thisBotIsBadTight array.
        """
        this_bot_is_bad_tight_array = self.triggers_dictionary['thisBotIsBadtight']

        cleaned_message = self.__remove_extra_words(message)

        this_bot_is_bad_array_tight_without_spaces = []

        for string in this_bot_is_bad_tight_array:
            this_bot_is_bad_array_tight_without_spaces.append(string.lower().replace(" ",""))

        for string in this_bot_is_bad_array_tight_without_spaces:
            if cleaned_message.lower().startswith(string.lower()):
                has_triggered = True

        return has_triggered

    def __check_message_is_question(self, message, has_triggered):
        if message[-1] == '?':
            has_triggered = True
        return has_triggered

    def __remove_extra_words(self, message):
        """
        Removes extra words from the message.
        """
        extra_words_to_delete = ["ok", "well", "right", "see", "bye"]

        message_words = message.split()

        # Creates a new list with all the words of which the lower-case variant is not found in extra_words_to_delete. 
        result_words  = [word for word in message_words if word.lower() not in extra_words_to_delete]
        
        result = ''.join(result_words)

        return result