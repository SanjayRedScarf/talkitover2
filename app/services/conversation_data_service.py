from flask import request
import json

class ConversationDataService:
    def get_conversation_input_data_from_front_end(self):

        """
        This method gets conversation input data from the JavaScript front end.
        """

        _input = json.loads(request.args.get('msg'))

        conversation_data = {   "message" : _input[0],
                                "section" : _input[1],
                                "initialHappinessScore" : int(_input[4]),
                                "finalHappinessScore" : int(_input[5]),
                                "anonymous" : _input[6],
                                "conversationId" : _input[7],
                                "clientId" : _input[8]
                            }

        return conversation_data
        
