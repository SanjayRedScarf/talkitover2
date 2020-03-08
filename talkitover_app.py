#import files
from flask import Flask, render_template, request, make_response
from json import dumps
from datetime import datetime
import json
import time
#from textblob import TextBlob # was using this, but it doesn't seem to be working on Sanjay's machine
#import nltk
import random
import csv
app = Flask(__name__)
my_dict = {} # shoudl this be tidied up and deleted out?
sleep_per_word = 0.04 # I don't think this is being used yet, but could use it in the future
scores = [-0.5, 0, 0.3]
encouragingNoises = ["I'm still listening, so feel free to say more.", "Go on, I'm still here.", \
"Keep talking, I'll be here for as long as you need me.", \
"I hear you. Keep going, I'm really happy for you to continue talking for as long as you need.", \
"Thanks for sharing this. Keep talking, I'm still here, and I'm still listening.", \
"I'm still here, so keep talking for as long as you need", "I'm still here, keep talking.", \
"Hmmm, thanks for sharing that. Keep talking, I'm still here", \
"Please keep on talking, I'm still here.", "Keep going, I'm still here", \
"Thanks for sharing. I'm still listening, so if you have more to say, please go on", \
"I hear you. Remember, this is like a sort of online journal, just use this as a space to write \
about what's on your mind and explore your thoughts. I'm just here to listen. Keep talking...", \
"Keep talking, I'm listening to you.", "Thanks for sharing, keep talking...", \
"I'm still listening, go on...", "I hear you, thank you for sharing, please keep talking" ]

noOfEncouragingNoises = len(encouragingNoises)
dataToStore = []

####### TODO TODO TODO ###################################
## Stopping/final survey: Imrpove the front end so that it better encourages the user to type stop (eg with somme sort of ongoing tip)
## OR (better) put in a button to implement the stopping
## Implement a separate css class for confidential text
## Maybe consider having a button which the user can press to say "you didn't understand me"
## Show a dancing ellipsis when the bot is thinking
## Enable splitting of chatbot responses into separate chunks
## Instead of the user's response being a dropdown, change it to a button so that it can be sized appropriately (i.e. not be tiny on a mobile screen)
##########################################################

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

def write_data(anonymous, userId, message, response):
    if anonymous=="true":
        message = message.replace(",", "¬")
        response = response.replace(",", "¬")

        with open('storedData.csv', 'a') as f:
            dataToStore = [str(userId), "User says:",str(message), "Chatbot says:",str(response)]
            f.write("\n" + str(dataToStore))
    return None

def next_user_input_one(buttonText):
    html_text = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='"+buttonText+"'>"+buttonText+"</option> \
    </select>"
    return html_text

def next_user_input_two(buttonText1,buttonText2):
    html_text = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
    <option>Select</option>  \
    <option value='"+buttonText1+"'>"+buttonText1+"</option> \
    <option value='"+buttonText2+"'>"+buttonText2+"</option> \
    </select>"
    return html_text

def no_of_fragments_in_str_or_list(response):
    noOfResponseFragments = 0
    if isinstance(response,list):
        noOfResponseFragments = len(response)
    elif isinstance(response,str):
        noOfResponseFragments = 1
    else:
        print("Error: expecting the response variable to be either a string or a list, otherwise don't know how to set the noOfResponseFragments variable")
    return noOfResponseFragments

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
    anonymous = _input[6]
    print("anonymous = "+anonymous) # debug, delete this
    userId = _input[7]
    initialHappinessScore = int(_input[4])
    finalHappinessScore = int(_input[5])
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
    nextUserInputFinalHappinessSurvey = "<select type='number' id='finalHappinessSurvey' onchange='getBotResponse()'>\
<option>Select</option>\
<option name='finalHappinessValue' value=1>1</option>\
<option name='finalHappinessValue' value=2>2</option>\
<option name='finalHappinessValue' value=3>3</option>\
<option name='finalHappinessValue' value=4>4</option>\
<option name='finalHappinessValue' value=5>5</option>\
<option name='finalHappinessValue' value=6>6</option>\
<option name='finalHappinessValue' value=7>7</option>\
<option name='finalHappinessValue' value=8>8</option>\
<option name='finalHappinessValue' value=9>9</option>\
<option name='finalHappinessValue' value=10>10</option>\
</select>"

    nextUserInputType = "initialHappinessSurvey" # the javascript code needs to pull in the data entered by the user in the userInput div and then spit the same data back out again. The way to retrieve this depends on whether the userinput mechanism was a button or a free text field, so this boolean helps to track that. It feeds through to a variable called currentUserInputType in the javascript code
    print("This si the get_bot_response function")

    if section==1:

        if initialHappinessScore > 7:
            response = "Sounds like you're feeling OK! I'm designed for people who are feeling low \
            and have something on their mind. But that's cool, let's talk anyway! :-) \
            Can I tell you first how this bot works?"
        elif initialHappinessScore > 3:
            response = "Thanks for sharing. I'm going to ask you to talk about whatever is on your \
            mind, but first I'm going to explain how this bot works, is that OK?"
        else:
            #response = "Oh dear, sounds like you're feeling really low, I'm sorry to hear that. \
            #I want to ask you more about that, but first can I tell you how this bot works?"
            response = ["Oh dear, sounds like you're feeling really low, I'm sorry to hear that",
            "I want to ask you more about that, but first can I tell you how this bot works?"]

        noOfResponseFragments = 0 # to assign the variable
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("Yes, happy to listen to the explanation of how this bot works")
        nextUserInputType = "userInputButton"
        next_section = section + 1

        # The next few lines prepares some inputs for the write_data function
        userId = str(datetime.now())
        responseIndex = 0
        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, userId, "initialHappinessScore (!!) = "+message, responseForWriteData)


        #dataToStore.append(message)
        #f = open("storedData.csv","w")
        #for i in range(0,len(dataToStore)):
        #    f.write(dataToStore[i])
        #f.close()

    elif section==2:

        response = ["I'm actually a very simple little bot. So please feel free to talk to me, \
        and sorry in advance if I don't always do a good job of understanding you.",
        "Instead think of this as being more like writing a journal, but as you keep writing, \
        I'll be here to encourage you to keep talking."]

        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I will talk with you even though you are a simple bot.")
        nextUserInputType = "userInputButton"

        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, userId, message, responseForWriteData)


    elif section==3:

        response = "Now let's talk about confidentiality and anonymity. \
        We offer an anonymised service. We don't have any way \
        of tracking you down, knowing who you are, or linking what you write to you."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I understand that you do not know who I am.")
        nextUserInputType = "userInputButton"

        write_data(anonymous, userId, message, response)

    elif section==4:

        response = "So given that I can't track you down, and also because I'm a very simple bot, \
        if you told me about an emergency/crisis situation, I wouldn't \
        be able to help."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I know you cannot provide emergency services.")
        nextUserInputType = "userInputButton"

        write_data(anonymous, userId, message, response)

    elif section==5:

        response = "Next I'm going to give you the choice whether you want to use this on a confidential \
        or anonymous basis. When I say anonymous, I mean that our boffins may see your text to help \
        us improve the way this software works, but we still won't know who you are."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I know what you mean by anonymous.")
        nextUserInputType = "userInputButton"

        write_data(anonymous, userId, message, response)

    elif section==6:

        response = "And when I say confidential, I mean that your text won't be \
        stored at all, and no human will see what you write."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("OK, I know what you mean by confidential.")
        nextUserInputType = "userInputButton"

        write_data(anonymous, userId, message, response)

    elif section==7:

        response = "Would you like this service to be anonymous or confidential?"
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_two("Anonymous (my words can help improve the bot)", "Confidential (no human ever sees my words)")
        nextUserInputType = "userInputButton"

        write_data(anonymous, userId, message, response)

    elif section==8:

        anonymous = "true" if message.split()[0].lower()=="anonymous" else "false"
        response = "Thanks! One last thing: You remember saying how you felt on scale from 1 to 10 \
        at the start? I'd like to ask you the same thing at the end so I know if we're helping."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("Yes, I am happy to let you see how I feel at the end too")
        nextUserInputType = "userInputButton"

        write_data(anonymous, userId, message, response)

    elif section==9:

        response = ["When you're finished using the bot, please click the stop button on the right\
        or just type 'stop'; this will take you to the super-quick final survey.", "Can you do \
        this instead of closing/exiting this window?"]
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = next_user_input_one("Yes, when I am finished I will click the stop button")
        nextUserInputType = "userInputButton"

        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, userId, message, responseForWriteData)


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
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"

        write_data(anonymous, userId, message, response)




    elif section > 10:

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

        if(message.lower()=="stop"):
            response = "Thank you for using this bot. Please rate how you feel on a scale \
            from 1 to 10, where 1 is terrible and 10 is great. As a reminder, the score you \
            gave at the start was "+str(initialHappinessScore)
            next_section = -1
            noOfResponseFragments = no_of_fragments_in_str_or_list(response)
            nextUserInput = nextUserInputFinalHappinessSurvey
            nextUserInputType = "finalHappinessSurvey"
        else:
            randomlyChosenIndex = random.randint(0,noOfEncouragingNoises-1)
            response = encouragingNoises[randomlyChosenIndex]
            next_section = section + 1
            noOfResponseFragments = no_of_fragments_in_str_or_list(response)
            nextUserInput = nextUserInputFreeText
            nextUserInputType = "freeText"

        # This isn't doing it right -- it just overwrites the previous message with the current one, and doesn't store any other useful metabdata, let alone accommodate mutliple users
        #dataToStore.append(response)
        #f = open("storedData.csv","w")
        #for i in range(0,len(dataToStore)):
        #    f.write(dataToStore[i])
        #f.close()
        write_data(anonymous, userId, message, response)


    elif section == -1: # this is the "end" (i.e. user has entered "stop") section

        # at the moment when the bot sensed that the user had entered "stop", it already immediately asked the final survey question

        happinessChange = finalHappinessScore - initialHappinessScore

        if happinessChange < 0:
            response = "Oh no! I'm so sorry you're feeling worse than you were at the start! :-(. \
            Please tell us why we made things worse, and what we could do better in future"
        elif happinessChange == 0:
            response = "We wanted to make things better for you, sorry you're feeling no better than \
            you did at the start. Optional final question - Please tell us whether we met your \
            expectations, and any suggestions for improvement."
        elif happinessChange > 0:
            response = "I'm glad you're feeling better than you did at the start. Optional final question: \
            if you have any comments to help us improve this bot, please make them here"

        next_section = -2
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"


        write_data(anonymous, userId, "finalHappinessScore (!!) = "+message, response)


    elif section == -2: # this is the "end" (i.e. user has entered "stop") section

        response="This is the end. Thank you for using the Talk It Over chatbot."
        #print("The response variable has just been set equal to "+response)

        next_section = -3
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInput = ""
        nextUserInputType = ""

        # output data
        #if anonymous=="true"
        dataToStore.append([message,response])

            #writer = csv.writer(f)
            #writer.writerow(dataToStore)

        #f = open("storedData.csv","w")
        #for i in range(0,len(dataToStore)):
        #f.write("\n" + str(dataToStore))
        #f.close()

        write_data(anonymous, userId, message, response)

    #time.sleep(min(sleep_per_word*len(response.split()), 2))  # this delay is meant to represent the bot's thinking time. I'm just finding it annoying, but perhaps if there's a better dancing ellipsis to represent typing, it might be more worthwhile having the delay in.
    print("This is the data which gets sent to the client side")
    print([response, noOfResponseFragments, next_section, score, nextUserInput, nextUserInputType, anonymous, userId])
    return make_response(dumps([response, noOfResponseFragments, next_section, score, nextUserInput, nextUserInputType, anonymous, userId]))




if __name__ == "__main__":
    app.run()
