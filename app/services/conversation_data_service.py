from flask import request
from models import conversation_data
import json

class ConversationDataService:
    def get_conversation_input_data_from_front_end(self):

        """
        Gets conversation input data from the JavaScript front end.
        """

        _input = json.loads(request.args.get('msg'))

        return conversation_data.ConversationData(_input[0], _input[1], int(_input[3]), int(_input[4]), _input[5], _input[6], _input[7])
        
