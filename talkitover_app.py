#import files
from flask import Flask, render_template, request, make_response
from json import dumps
import json
import time
#from textblob import TextBlob # was using this, but it doesn't seem to be working on Sanjay's machine
#import nltk
import random
app = Flask(__name__)
my_dict = {} # shoudl this be tidied up and deleted out?
sleep_per_word = 0.04 # I don't think this is being used yet, but could use it in the future
scores = [-0.5, 0, 0.3]

# returns the first index where an element occurs.
def bisect_left(a, x):

    hi = len(a)
    lo = 0
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] >= x: hi = mid
        else: lo+=1
    return lo

# get a response message from a yes, no answer
def get_yes_no(message, yes_message, no_message, not_understand_message, section):
    print("message ="+str(message))
    words = [i.lower() for i in message.split()]
    next_section = section
    print("this si the get_yes_no function")
    print(words, "sure" in words)
    if (("yes" in words) or ("yeah" in words) or ("yep" in words) or ("sure" in words)) and (("no" in words) or (" ".join(words[:2])=="not really")):
        response = not_understand_message[0]
        next_section += not_understand_message[1]
    elif ((("yes" not in words) and ("yeah" not in words))  and ("yep" not in words) and ("sure" not in words) and (" ".join(words[:2])!="not really") and ("no" not in words)):
        response = not_understand_message[0]
        next_section += not_understand_message[1]
    elif ("yes" in words) or ("yeah" in words) or ("yep" in words) or ("sure" in words):
        response = yes_message[0]
        next_section +=yes_message[1]
    elif ("no" in words) or " ".join(words[:2])=="not really":
        response = no_message[0]
        next_section += no_message[1]
    else:
        response="Error"
    return [response, next_section]

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/get")
def get_bot_response():
    time.sleep(1)
    _input = json.loads(request.args.get('msg'))
    message = _input[0]
    section = _input[1]
    output = _input[2]
    score = _input[3]
    start_again = False
    nextUserInput = ""
    nextUserInputFree = "<input id='textInput' type='text' name='msg' placeholder='Message' />" # this is a standard choice of thing to have at the bottom of the chatbox which will allow the user to enter free text
    nextUserInputYesNo = "<button class='textInput' id='userInputButton' type='button' onclick='getBotResponse()' value='yes'>Yes</button> \
          <button class='textInput' id='userInputButton' type='button' onclick='getBotResponse()' value='no'>No</button>"
    nextUserInputIsFreeText = False # the javascript code needs to pull in the data entered by the user in the userInput div and then spit the same data back out again. The way to retrieve this depends on whether the userinput mechanism was a button or a free text field, so this boolean helps to track that. It feeds through to a variable called currentUserInputIsFreeText in the javascript code
    print("this si the get_bot_response function")
    if section==0:
        if message.lower()=="start":
            section=2
            start_again = True
        else:
            response = "Please type start to start the chat again"
            next_section = 0
    if section==1:
        response = "Hi. So, I am a very simple piece of software and an early prototype. \
        Thank you for trying me :-)! Whilst we are talking I'd like to store your responses to \
        analyse them later to help improve the bot. Are you happy for me to do this? (Please reply yes or no)"

        nextUserInput = nextUserInputYesNo
        nextUserInputIsFreeText = "false"
        next_section = 2
    elif section==2:
        if start_again:
            response = "Hi there! Can I ask how you're feeling today?"
            next_section = 3
        else:
            yes_message = "Thanks a lot! So firstly can I ask how you are feeling today?"
            no_message = "That's ok. I won't be storing any of your responses. \
                So to begin, can I ask how you're feeling today?"
            not_understand_message = "Sorry, I didn't understand that"
            get_response = get_yes_no(message, (yes_message,1), (no_message,1), (not_understand_message,0), section)
            response = get_response[0]
            next_section = get_response[1]
            nextUserInput = nextUserInputFree
            nextUserInputIsFreeText = "true"


    elif section > 2:
        words = [i.lower() for i in message.split()]
        if (words[0]=="no") or (" ".join(words[:2])=="not really"):
            # I DON'T THINK this is making sense, so need to rework this if statement
            response = "That's ok. Is there anything else you would like to talk about?"
            next_section = 6
        else:

            """
# This section was here and used textblob nlp. However it seem to be causing errors when using this locally on my laptop so I took it out
            try:
                sentence = TextBlob(message)
                score = sentence.sentiment.polarity
            except:
                score = 0

            responses = ["Sounds like things are really rough at the moment. Can I ask what is making you feel this way?", \
            "Sounds like things are not too easy at the moment. Can I ask what is making you feel this way?", \
            "Sounds like things could be a bit better. Can I ask what is making you feel this way?", \
            "To me it sounds like things are going ok for you, but I may be mistaken! Would you like to tell me more about it?"]
            response = responses[bisect_left(scores, score)]
            #next_section = 4
            """
            response = "Sorry to hear that. I'm still here, feel free to keep talking"
            next_section = section + 1
            nextUserInputIsFreeText = "true"


    time.sleep(min(sleep_per_word*len(response.split()), 2))
    print([response, next_section, output, score, nextUserInput, nextUserInputIsFreeText])
    return make_response(dumps([response, next_section, output, score, nextUserInput, nextUserInputIsFreeText]))




if __name__ == "__main__":
    app.run()
