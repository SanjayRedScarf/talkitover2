from datetime import datetime
import os
from flask import current_app

class ConversationDataRepository:
    def insert_data(self, user_inputs):
        """
        Stores the messages to file, if the user agrees, or if it's something inoffensive
        More precisely, if the anonymous variable is set to true (i.e. the user has given permission not to be totally confidential)...
        ... or if we're in the initial section where gathering data is inoffensive anyway...
        ... then store the data.
        Note: I considered using a different decision criterion, namely what the nextUserInputType was (although tha'ts off by one, should be currentUserInputType)
        However for futureproofing reasons I decided against this.
        This is because in the future we might have dropdowns or buttons occurring during the body of the conversation.
        And those might be more sensitive.
        """
        google_ads_data = current_app.config['GOOGLE_ADS_DATA']

        if user_inputs.anonymous=="true" or user_inputs.section <= 10:  
            message = user_inputs.message.replace(",", "¬")
            response = user_inputs.response.replace(",", "¬")

            current_directory = os.path.dirname(os.path.realpath('__file__'))
            filename = os.path.join(current_directory, 'app/storedData.csv')

            with open(filename, 'a') as f:
                dataToStore = [str(user_inputs.conversation_id), "User says:", str(user_inputs.message), "Chatbot says:", str(user_inputs.response), user_inputs.client_id, "Campaign: " + str(google_ads_data.campaign or ''), "Group: " + str(google_ads_data.group or ''), "Geo: " + str(google_ads_data.geo or ''), "Device: " + str(google_ads_data.device or ''), "Timestamp: "+ str(datetime.now())]
                f.write("\n" + str(dataToStore))
        return None