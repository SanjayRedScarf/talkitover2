from flask import Flask, render_template, request, make_response, jsonify, redirect, session
from flask_session import Session
from json import dumps
import random
from services import google_ads_service, conversation_data_service, bot_processing_service, sentence_encoder_service
from repositories import triggers_repository
import datetime

app = Flask(__name__)

_google_ads_service = google_ads_service.GoogleAdsService()
_conversation_data_service = conversation_data_service.ConversationDataService()
_triggers_repository = triggers_repository.TriggersRepository()
_bot_processing_service = bot_processing_service.BotProcessingService()

_sentence_encoder_service = sentence_encoder_service.SentenceEncoder()
_sentence_encoder_service.make_cat_embed()

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def home():
    homepage_name = random.choice(["home - bootstrap 2020m05.html", "home - original pre-2020m05.html"])

    session['GOOGLE_ADS_DATA'] = _google_ads_service.get_google_ads_data_from_url()

    session['TRIGGERS_DICT'] = _triggers_repository.get_triggers_dictionary()

    session['RESPONSE_DICT']= _triggers_repository.get_response_dictionary()

    session['version'] = 19 # make sure to change this number whenever changing versions




    session['uid'] = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') # unique user id, later used for data analysis
    session['user_character_count'] = 0 #total user characters throughout chat
    session['ai_repeat'] = [] # tracks which triggers have already been triggered by sentence encoder
    session['response_modifier'] = {'suicidal':False,'lonely':False,'hate_looks':False} # tracks if user is suicidal, upset, etc which can change response used
    session['short_msg_count'] = 0 #counts the number of times the short msg trigger triggers
    
    session['last_trigger'] = "" # used for multi response triggers

    #variables for a/b testing
    session['qheavy']= random.choice([True,False])
    session['multi'] = random.choice([True,False])
    session['no_char_count'] = random.choice([True,False])
    session['gpt3'] = random.choice([True,False])
    
    return render_template(homepage_name)

@app.route("/get")
def main():
    """
    Processes the user's message.
    """
    print('this is the uid from app.py in main: {}'.format(session['uid']))
    print('this is the character count, in app.py in main: {}'.format(session['user_character_count']))
    print('this is the ai_repeat in app.py in main: {}'.format(session['ai_repeat']))

    conversation_input_data = _conversation_data_service.get_conversation_input_data_from_front_end()

    tio_outputs_data = _bot_processing_service.process_user_input(conversation_input_data,_sentence_encoder_service)

    return make_response(dumps([tio_outputs_data.response, tio_outputs_data.number_of_response_fragments, tio_outputs_data.next_section, tio_outputs_data.next_user_input, tio_outputs_data.next_user_input_type, tio_outputs_data.anonymous, tio_outputs_data.conversation_id]))

if __name__ == "__main__":
    app.run()

