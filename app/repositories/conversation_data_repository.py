from datetime import datetime
import os
from flask import current_app, session
import csv

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
        google_ads_data = session['GOOGLE_ADS_DATA']
        field_names = ['user_id','user_says','chatbot_says','frontend','campaign','group','geo','device','timestamp','ai_data',
        'over_threshold','highest_score_category','highest_score_exemplar','highest_score_substring']

        if user_inputs.anonymous=="true" or user_inputs.section <= 11:  
            message = user_inputs.message.replace(",", "¬")
            response = user_inputs.response.replace(",", "¬")

            current_directory = os.path.dirname(os.path.realpath('__file__'))
            filename = os.path.join(current_directory, 'app/storedData.csv')

            file2 = os.path.join(current_directory,'app/storedData_v2.csv')

            with open(filename, 'a') as f:
                dataToStore = [str(user_inputs.conversation_id), "User says:", str(user_inputs.message), "Chatbot says:", str(user_inputs.response), user_inputs.client_id, "Campaign: " + str(google_ads_data.campaign or ''), "Group: " + str(google_ads_data.group or ''), "Geo: " + str(google_ads_data.geo or ''), "Device: " + str(google_ads_data.device or ''), "Timestamp: "+ str(datetime.now())]
                f.write("\n" + str(dataToStore))

            with open(file2,'a',newline ='') as f:
                writer = csv.DictWriter(f,fieldnames=field_names)
                #writer.writeheader() # not sure if I need this
                if user_inputs.ai_data != {}:
                    data = [{'user_id':user_inputs.conversation_id, "user_says": str(user_inputs.message), "chatbot_says": str(user_inputs.response), 'frontend':user_inputs.client_id, "campaign": str(google_ads_data.campaign or ''), "group":  str(google_ads_data.group or ''), "geo": str(google_ads_data.geo or ''), "device": str(google_ads_data.device or ''), "timestamp":str(datetime.now()), 'ai_data':user_inputs.ai_data,
                    'over_threshold':user_inputs.ai_data['max_over_thresh'],'highest_score_category':user_inputs.ai_data['highest_max_score_category'],'highest_score_exemplar':user_inputs.ai_data['exemplar_for_max_cat'],
                    'highest_score_substring':user_inputs.ai_data['substring_for_max_cat']}]
                else:
                    data = [{'user_id':user_inputs.conversation_id, "user_says": str(user_inputs.message), "chatbot_says": str(user_inputs.response), 'frontend':user_inputs.client_id, "campaign": str(google_ads_data.campaign or ''), "group":  str(google_ads_data.group or ''), "geo": str(google_ads_data.geo or ''), "device": str(google_ads_data.device or ''), "timestamp":str(datetime.now()), 'ai_data':user_inputs.ai_data}]
                writer.writerows(data)
        return None