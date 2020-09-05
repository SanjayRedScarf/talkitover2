from flask import Flask, render_template, request, make_response, jsonify, redirect
import random
from services.google_ads_service import GoogleAdsService
from services.conversation_data_service import ConversationDataService

app = Flask(__name__)
google_ads_service = GoogleAdsService()
conversation_data_service = ConversationDataService()

@app.route('/')
def home():
    homepage_name = random.choice(["home - bootstrap 2020m05.html", "home - original pre-2020m05.html"])
    google_ads_data = google_ads_service.get_google_ads_data_from_url()
    return render_template(homepage_name)

@app.route("/get")
def main():
    
    """
    This function pulls in the conversation input data from the javascript frontend.
    It then processes the user's message and returns the conversation output data back to the front end.
    """

    conversation_input_data = conversation_data_service.get_conversation_input_data_from_front_end()

    # outputs_dict = bot_processing(inputs_dict)

    # response = outputs_dict["response"]
    # noOfResponseFragments = outputs_dict["noOfResponseFragments"]
    # next_section = outputs_dict["next_section"]
    # score = "" # not being used
    # nextUserInput = outputs_dict["nextUserInput"]
    # nextUserInputType = outputs_dict["nextUserInputType"]
    # anonymous = outputs_dict["anonymous"]
    # conversationId = outputs_dict["conversationId"]

    # return make_response(dumps([response, noOfResponseFragments, next_section, score, nextUserInput, nextUserInputType, anonymous, conversationId]))

if __name__ == "__main__":
    app.run()