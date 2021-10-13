from flask import Flask, render_template, request, make_response, jsonify, redirect, session
from flask_session import Session
from json import dumps
import random
from services import google_ads_service, conversation_data_service, bot_processing_service, sentence_encoder_service
from repositories import triggers_repository

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

    app.config['GOOGLE_ADS_DATA'] = _google_ads_service.get_google_ads_data_from_url()

    app.config['TRIGGERS_DICT'] = _triggers_repository.get_triggers_dictionary()
    
    session['uid'] = random.randint(0,100)
    session['user_character_count'] = 0
    session['ai_repeat'] = []
    session['response_modifier'] = []

    return render_template(homepage_name)

@app.route("/get")
def main():
    """
    Processes the user's message.
    """
    print('this is the uid from app.py in main: {}'.format(session['uid']))

    conversation_input_data = _conversation_data_service.get_conversation_input_data_from_front_end()

    tio_outputs_data = _bot_processing_service.process_user_input(conversation_input_data,_sentence_encoder_service)

    return make_response(dumps([tio_outputs_data.response, tio_outputs_data.number_of_response_fragments, tio_outputs_data.next_section, tio_outputs_data.next_user_input, tio_outputs_data.next_user_input_type, tio_outputs_data.anonymous, tio_outputs_data.conversation_id]))

if __name__ == "__main__":
    app.run()

