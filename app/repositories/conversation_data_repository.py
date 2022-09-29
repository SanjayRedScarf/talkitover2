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

        field_names = ['user_id','user_says','chatbot_says','version','frontend','campaign','group','geo','device','timestamp','section','response_type' ,'multi','q_heavy',
        'no_char_count','gpt3','ai_data','over_threshold','highest_score_category','highest_score_exemplar','highest_score_substring']


        version = session['version']
        multi = session['multi']
        if user_inputs.section != 12:
            user_inputs.response_type = None
        response_type = str(user_inputs.response_type)
        if user_inputs.anonymous=="true" or user_inputs.section <= 11:  

            current_directory = os.path.dirname(os.path.realpath('__file__'))


            file2 = os.path.join(current_directory,'app/storedData_v{}.csv'.format(version))


            with open(file2,'a',newline ='',encoding='utf-8') as f:
                writer = csv.DictWriter(f,fieldnames=field_names)
                if f.tell() == 0: # if the file doesnt already exist, write the field names as a header
                    writer.writeheader()  

             
                data = [{'user_id':user_inputs.conversation_id, "user_says": str(user_inputs.message), "chatbot_says": str(user_inputs.response),'version':version, 'frontend':user_inputs.client_id, "campaign": str(google_ads_data.campaign or ''), "group":  str(google_ads_data.group or ''), "geo": str(google_ads_data.geo or ''), "device": str(google_ads_data.device or ''), 
                "timestamp":str(datetime.now()),'section':(user_inputs.section) ,'response_type':response_type,'multi':multi,'q_heavy':session['qheavy'],'no_char_count':session['no_char_count'],'gpt3':session['gpt3'],'ai_data':user_inputs.ai_data or {},
                'over_threshold':user_inputs.ai_data.get('max_over_thresh', {}),'highest_score_category':user_inputs.ai_data.get('highest_max_score_category',{}),'highest_score_exemplar':user_inputs.ai_data.get('exemplar_for_max_cat',{}),
                'highest_score_substring':user_inputs.ai_data.get('substring_for_max_cat',{})}]

                writer.writerows(data)

        return None
