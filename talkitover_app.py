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
    output = _input[2] # I don't know what this is for!
    score = _input[3]
    initialHappinessScore = int(_input[4])
    start_again = False
    nextUserInput = ""
    nextUserInputFreeText = "<input id='textInput' type='text' name='msg' placeholder='Message' />" # this is a standard choice of thing to have at the bottom of the chatbox which will allow the user to enter free text
    nextUserInputYesNo = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='yes'>Yes</option> \
    <option value='no'>No</option> \
    </select>"
    nextUserInputOneOption = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='yes'>Yes</option> \
    </select>"
    nextUserInputTwoOptions = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='yes'>Yes</option> \
    <option value='no'>No</option> \
    </select>"

    nextUserInputType = "initialHappinessSurvey" # the javascript code needs to pull in the data entered by the user in the userInput div and then spit the same data back out again. The way to retrieve this depends on whether the userinput mechanism was a button or a free text field, so this boolean helps to track that. It feeds through to a variable called currentUserInputType in the javascript code
    print("This si the get_bot_response function")

    def nextUserInputOneOption(buttonText):
        nextUserInputOneOption = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
        <option>Select</option>  \
        <option value='"+buttonText+"'>"+buttonText+"</option> \
        </select>"
        return nextUserInputOneOption

    def nextUserInputTwoOptions(buttonText1,buttonText2):
        nextUserInputTwoOptions = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
        <option>Select</option>  \
        <option value='"+buttonText1+"'>"+buttonText1+"</option> \
        <option value='"+buttonText2+"'>"+buttonText2+"</option> \
        </select>"
        return nextUserInputTwoOptions


    # not sure if we need this if section = 0 bit???????????????????? DELETE THIS?
    if section==0:
        if message.lower()=="start":
            section=2
            start_again = True
        else:
            response = "Please type start to start the chat again"
            next_section = 0
    if section==1:

        if initialHappinessScore > 7:
            response = "Sounds like you're feeling OK! I'm designed for people who are feeling low \
            and have something on their mind. But that's cool, let's talk anyway! :-) \
            Can I tell you first how this bot works?"
        elif initialHappinessScore > 3:
            response = "Thanks for sharing. I'm going to ask you to talk about whatever is on your \
            mind, but first I'm going to explain how this bot works, is that OK?"
        else:
            response = "Oh dear, sounds like you're feeling really low, I'm sorry to hear that. \
            I want to ask you more about that, but first can I tell you how this bot works?"

        #response = "Hi. So, I am a very simple piece of software and an early prototype. \
        #Thank you for trying me :-)! Whilst we are talking I'd like to store your responses to \
        #analyse them later to help improve the bot. Are you happy for me to do this? (Please reply yes or no)"

        nextUserInput = nextUserInputOneOption("Yes, happy to listen to the explanation of how this bot works")
        nextUserInputType = "userInputButton"
        next_section = section + 1
    elif section==2:

        response = "I'm actually a very simple little bot. So please feel free to talk to me, \
        and sorry in advance if I don't always do a good job of understanding you. Instead \
        think of this as being more like writing a journal, but as you keep writing, \
        I'll be here to encourage you to keep talking."
        next_section = section + 1
        nextUserInput = nextUserInputOneOption("OK, I will talk with you even though you are a simple bot.")
        nextUserInputType = "userInputButton"

        # REMINDER these are the outputs required at the end:
        # response, next_section, output, score, nextUserInput, nextUserInputType

        # We offer an anonymised service. We don't have any way \
        #of tracking you down, knowing who you are, or linking what you write to you.


    elif section==3:

        response = "Now let's talk about confidentiality and anonymity. \
        We offer an anonymised service. We don't have any way \
        of tracking you down, knowing who you are, or linking what you write to you."
        next_section = section + 1
        nextUserInput = nextUserInputOneOption("OK, I understand that you do not know who I am.")
        nextUserInputType = "userInputButton"


    elif section==4:

        response = "So given that I can't track you down, and also because I'm a very simple bot, \
        if you told me about an emergency/crisis situation, I wouldn't \
        be able to help."
        next_section = section + 1
        nextUserInput = nextUserInputOneOption("OK, I know you cannot provide emergency services.")
        nextUserInputType = "userInputButton"


    elif section==5:

        response = "Next I'm going to give you the choice whether you want to use this on a confidential \
        or anonymous basis. When I say anonymous, I mean that our boffins may see your text to help \
        us improve the way this software works, but we still won't know who you are."
        next_section = section + 1
        nextUserInput = nextUserInputOneOption("OK, I know what you mean by anonymous.")
        nextUserInputType = "userInputButton"


    elif section==6:

        response = "And when I say confidential, I mean that your text won't be \
        stored at all, and no human will see what you write."
        next_section = section + 1
        nextUserInput = nextUserInputOneOption("OK, I know what you mean by confidential.")
        nextUserInputType = "userInputButton"


    elif section==7:

        response = "Would you like this service to be anonymous or confidential?"
        next_section = section + 1
        nextUserInput = nextUserInputTwoOptions("Anonymous (my words can help improve the bot)", "Confidential (no human ever sees my words)")
        nextUserInputType = "userInputButton"


    elif section==8:

        response = "Thanks! One last thing: You remember saying how you felt on scale from 1 to 10 \
        at the start? I'd like to ask you the same thing at the end so I know if we're helping."
        next_section = section + 1
        nextUserInput = nextUserInputOneOption("Yes, I am happy to let you see how I feel at the end too")
        nextUserInputType = "userInputButton"


    elif section==9:

        response = "When you're finished using the bot, please type 'stop' in the text field \
        where the responses go, this will take you to the super-quick final survey. I'll do \
        this instead of closing/exiting this window."
        next_section = section + 1
        nextUserInput = nextUserInputOneOption("Yes, I will type stop as my response when I am done")
        nextUserInputType = "userInputButton"



    elif section==10:

        responseFragmentBasedOnScore =""

        if initialHappinessScore > 7:
            responseFragmentBasedOnScore = "Seems like you're feeling OK, but I'm still available for you \
            to chat with if you want. Maybe just start by talking about something that's on your mind?"
        elif initialHappinessScore > 3:
            responseFragmentBasedOnScore = "Would you like to start by talking about something that's on your mind?"
        else:
            responseFragmentBasedOnScore = "Sounds like things are tough for you just now. Would you like to \
            start talking about something that's on your mind?"

        response = "OK, now we've got the intro stuff out the way... you were saying before that \
        you were feeling "+str(initialHappinessScore)+" out of 10. "+responseFragmentBasedOnScore

        next_section = section + 1
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"





    elif section > 9:
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


    # the bot gives an answer based on textblob. they carry on talking...
#    elif section == 4:
#        words = [i.lower() for i in message.split()]
#        if (words[0]=="no") or (" ".join(words[:2])=="not really"):
#            response = "That's ok. Would you like to talk about something else?"
#            next_section = 6
#        else:
#            responses = ["Sounds like things are really rough at the moment. Can I ask what is making you feel this way?", \
#            "Sounds like things are not too easy at the moment. Can I ask what is making you feel this way?", \
#            "Sounds like things could be a bit better. Can I ask what is making you feel this way?", \
#            "To me it sounds like things are going ok for you, but I may be mistaken! Would you like to tell me more about it?"]
#            response = responses[bisect_left(scores, score)]
#            next_section = 5
#
#    # this is the section of encouraging noises
#    elif section == 5:
#        words = [i.lower() for i in message.split()]
#        if (words[0]=="no") or (" ".join(words[:2])=="not really"):
#            response = "Ok, Is there anything else you would like to talk about?"
#            next_section = 6
#        else:
#            responses = ["Go on, I'm still listening", "Can you say more about that?"]
#            response_num = 1 if random.uniform(0, 1)>0.5 else 0
#            response = responses[response_num]
#            next_section = 5
#
#    # this is the section to gauge how they're feeling on a scale from 1 to 10
#    elif section == 6:
#        words = [i.lower() for i in message.split()]
#        if (words[0]=="no") or (" ".join(words[:2])=="not really"):
#            response = "Ok thanks for speaking to me. Have you found talking useful?"
#            next_section = 7
#        else:
#            responses = ["Go on, I'm still listening", "Can you say more about that?"]
#            response_num = 1 if random.uniform(0, 1)>0.5 else 0
#            response = responses[response_num]
#            next_section = 5
#    elif section == 7:
#        get_response = get_yes_no(message, ("That's great! I'm glad to hear it. \
#        Do you have any suggestions about how I could improve?",1),
#        ("Sorry to hear that. Do you have any suggestions about how I can improve?",1), \
#        ("Sorry I didn't understand that",0), section)
#        response = get_response[0]
#        next_section = get_response[1]
#    elif section == 8:
#        words = [i.lower() for i in message.split()]
#        if words[0]=="no" or " ".join(words[:2])=="not really" or " ".join(words[:3])=="i'd rather not":
#            response = "Ok thanks anyway. Do chat again if you'd like to"
#        else:
#            response = "Thanks for the feedback. Do chat again if you'd like to"
#        next_section=0


            response = "Sorry to hear that. I'm still here, feel free to keep talking"
            next_section = section + 1
            nextUserInput = nextUserInputFreeText
            nextUserInputType = "freeText"


    #time.sleep(min(sleep_per_word*len(response.split()), 2))  # this delay is meant to represent the bot's thinking time. I'm just finding it annoying, but perhaps if there's a better dancing ellipsis to represent typing, it might be more worthwhile having the delay in.
    print("This is the data which gets sent to the client side")
    print([response, next_section, output, score, nextUserInput, nextUserInputType])
    return make_response(dumps([response, next_section, output, score, nextUserInput, nextUserInputType]))




if __name__ == "__main__":
    app.run()
