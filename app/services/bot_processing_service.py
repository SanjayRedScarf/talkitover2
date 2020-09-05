from datetime import datetime

class BotProcessingService:
    def bot_processing(self, conversation_input_data):
        
    dataToStore = []
    USER_CHARACTER_COUNT = 0
    conversationId = str(datetime.now())

    message = conversation_input_data["message"]
    section = conversation_input_data["section"]
    initialHappinessScore = int(conversation_input_data["initialHappinessScore"])
    finalHappinessScore = int(conversation_input_data["finalHappinessScore"])
    anonymous = conversation_input_data["anonymous"]
    conversationId = conversation_input_data["conversationId"]
    clientId = conversation_input_data["clientId"]

    nextUserInput = ""
    if clientId == "originalJavascriptClient":
        nextUserInputFreeText = "<input id='textInput' type='text' name='msg' placeholder='Type your message here' />" # this is a standard choice of thing to have at the bottom of the chatbox which will allow the user to enter free text
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
    elif clientId == "bootstrapJavascriptClient":
        nextUserInputFreeText = "<input class='message_input' placeholder='Type your message here...'>" # this is a standard choice of thing to have at the bottom of the chatbox which will allow the user to enter free text
        #nextUserInputYesNo = "<select class='message_input' type='text' id='userInputButton' onchange='sendMessage()> \
        nextUserInputYesNo = "<select class='message_input' type='text' id='userInputButton' > \
        <option selected disabled>Select</option>  \
        <option value='yes'>Yes</option> \
        <option value='no'>No</option> \
        </select>"
        #nextUserInputOneOption = "<select class='message_input' type='text' id='userInputButton' onchange='sendMessage()> \
        nextUserInputOneOption = "<select class='message_input' type='text' id='userInputButton' > \
        <option selected disabled>Select</option>  \
        <option value='yes'>Yes</option> \
        </select>"
        #nextUserInputTwoOptions = "<select class='message_input' type='text' id='userInputButton' onchange='sendMessage()> \
        nextUserInputTwoOptions = "<select class='message_input' type='text' id='userInputButton' > \
        <option selected disabled>Select</option>  \
        <option value='yes'>Yes</option> \
        <option value='no'>No</option> \
        </select>"
        #nextUserInputFinalHappinessSurvey = "<select class='message_input' type='number' id='finalHappinessSurvey' onchange='sendMessage()'>\
        nextUserInputFinalHappinessSurvey = "<select class='message_input' type='number' id='finalHappinessSurvey' >\
        <option selected disabled>Select</option>\
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
    else: # i.e. anticipating this scenario is where the API is using the server
    # if the API is being used, these strings of HTML are not expected ot be needed
        nextUserInputFreeText = ""
        nextUserInputYesNo = ""
        nextUserInputOneOption = ""
        nextUserInputTwoOptions = ""
        nextUserInputFinalHappinessSurvey = ""

    nextUserInputType = "initialHappinessSurvey" # the javascript code needs to pull in the data entered by the user in the userInput div and then spit the same data back out again. The way to retrieve this depends on whether the userinput mechanism was a button or a free text field, so this boolean helps to track that. It feeds through to a variable called currentUserInputType in the javascript code

    if section==1:

        abortConversation = False
        noOfResponseFragments = 0 # to assign the variable

        if initialHappinessScore > 7:
            response = ["Sounds like you're feeling OK! I'm designed for people who are feeling low \
            and have something on their mind. But you're feeling good, which is great! :-)", \
            "Or maybe you're just here to check out this site, which is cool. Why don't you refresh the page, but pretend you're feeling sad this time!"]
            abortConversation = True
        elif initialHappinessScore > 3:
            response = "Thanks for sharing. Sounds like you're not quite on top of the world - shame about that. \
                Is there anything specific on your mind at the moment?"
        else:
            #response = "Oh dear, sounds like you're feeling really low, I'm sorry to hear that. \
            #I want to ask you more about that, but first can I tell you how this bot works?"
            response = ["Oh dear, sounds like you're feeling really low, I'm sorry to hear that. ",
            "Is there something specific that's triggered this?"]


        if abortConversation == False:
            noOfResponseFragments = no_of_fragments_in_str_or_list(response)
            nextUserOptions = ["Yes", "No"]
            nextUserInput = next_user_input_two(nextUserOptions,clientId) # this puts a string of html around it
            nextUserInputType = "userInputButton"
            next_section = section + 1
            #next_section = 9 # DEBUG CHEAT: for debugging purposes when you want to skip the intro. This shouldn't apply normally

            # The next few lines prepares some inputs for the write_data function
            conversationId = str(datetime.now())
            initialiseResponseAlreadyUsedVariables()
            responseIndex = 0 # I don't think this declaration is needed
            responseForWriteData = ""
            for responseIndex in range(0,noOfResponseFragments):
                responseForWriteData = responseForWriteData + response[responseIndex]
            write_data(anonymous, conversationId, "initialHappinessScore (!!) = "+message, responseForWriteData, section, clientId)
        elif abortConversation == True:
            next_section = -3
            noOfResponseFragments = no_of_fragments_in_str_or_list(response)
            nextUserOptions = [""] # n/a because next user input type is not buttons
            nextUserInput = ""
            nextUserInputType = "earlyAbort"

        # The next few lines prepares some inputs for the write_data function
        conversationId = str(datetime.now())
        initialiseResponseAlreadyUsedVariables()
        responseIndex = 0 # I don't think this declaration is needed
        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, "initialHappinessScore (!!) = "+message, responseForWriteData, section, clientId)

    elif section==2:

        if message.lower()=="yes":
            response = "I'd love to hear you say more about that. Before we do that, would you like me to explain about how this chatbot works?"
            nextUserOptions = ["Yes"] # this is the option that the user can select
            nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
            next_section = section + 2
        else:
            response = "Do you feel this way often?"
            nextUserOptions = ["Yes", "No"] # this is the option that the user can select
            nextUserInput = next_user_input_two(nextUserOptions,clientId) # this puts a string of html around it
            next_section = section + 1

        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserInputType = "userInputButton"

        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, message, responseForWriteData, section, clientId)

    elif section==3:
        if message.lower() == "yes":
            response = "Feeling this way often sounds pretty rubbish. I'm sorry about that. How long have been like this?"
        next_section = 35
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = [""] # n/a because next user input type is not buttons
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"

        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, message, responseForWriteData, section, clientId)

    # 35 might seem like an odd choice of section number
    # we were previously using 3.5, but using a non-integer-typed number caused errors in the guided track bot on the other side of the API
    elif section==35:
        response = "I'd like to hear more about that. Before we do that, I'd like to quickly explain how this chatbot works, if that's OK?"
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["Yes, tell me how this bot works"] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"
        next_section = 4
        responseForWriteData = ""

        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, message, responseForWriteData, section, clientId)

    elif section==4:
        response = ["I'm actually a very simple little bot. So please feel free to talk to me, \
        and sorry in advance if I don't always do a good job of understanding you. ",
        "Instead think of this as being more like writing a journal, but as you keep writing, \
        I'll be here to encourage you to keep talking."]

        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["OK, I will talk with you even though you are a simple bot."] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, message, responseForWriteData, section, clientId)

    elif section==5:

        response = "So given that I can't track you down, and also because I'm a very simple bot, \
        if you told me about an emergency/crisis situation, I wouldn't \
        be able to help."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["OK, I know you cannot provide emergency services."] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==6:

        response = "Next I'm going to give you the choice whether you want to use this on a confidential \
        or anonymous basis. When I say anonymous, I mean that our boffins may see your text to help \
        us improve the way this software works, but we still won't know who you are."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["OK, I know what you mean by anonymous."] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==7:

        response = "And when I say confidential, I mean that your text won't be \
        stored at all, and no human will see what you write."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["OK, I know what you mean by confidential."] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==8:

        response = "Would you like this service to be anonymous or confidential?"
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["Anonymous (my words can help improve the bot)", "Confidential (no human ever sees my words)"] # this is the option that the user can select
        nextUserInput = next_user_input_two(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==9:

        anonymous = "true" if message.split()[0].lower()=="anonymous" else "false"
        response = "Thanks! One last thing: You remember saying how you felt on a scale from 1 to 10 \
        at the start? I'd like to ask you the same thing at the end so I know if we're helping."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["Yes, I am happy to let you see how I feel at the end too"] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==10:

        if clientId == "originalJavascriptClient":
            response = ["When you're finished using the bot, please click the stop button on the right \
            or just type 'stop'; this will take you to the super-quick final survey. ", "Don't press it now, but \
            can you press this button instead of closing/exiting this window?"]
        elif clientId == "bootstrapJavascriptClient":
            response = ["When you're finished using the bot, please click the stop button below \
            or just type 'stop'; this will take you to the super-quick final survey. ", "Don't press it now, but \
            can you press this button instead of closing/exiting this window?"]
        else: # this is assumed to be the guided track front end
            response = ["When you're finished using the bot, please type 'stop' in the text field \
            where the responses go, this will take you to the super-quick one-question final survey. \
            Please please do this, because we want to know if we are helping."]
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        if clientId == "originalJavascriptClient":
            nextUserOptions = ["Yes, when I am finished I will click the stop button"] # this is the option that the user can select
        elif clientId == "bootstrapJavascriptClient":
            nextUserOptions = ["Yes, when I am finished I will click the stop button"] # this is the option that the user can select
        else: # this is assumed to be the guided track front end
            nextUserOptions = ["Yes, I agree to fill in the quick survey at the end. I'll type 'stop' in a text field."]
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        responseForWriteData = ""
        for responseIndex in range(0,noOfResponseFragments):
            responseForWriteData = responseForWriteData + response[responseIndex]
        write_data(anonymous, conversationId, message, responseForWriteData, section, clientId)


    elif section==11:

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
        nextUserOptions = [""] # n/a because next user input type is not buttons
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"

        write_data(anonymous, conversationId, message, response, section, clientId)




    elif section > 11:

        USER_CHARACTER_COUNT += len(message)

        if(message.lower()=="stop"):
            response = "Thank you for using this bot. Please rate how you feel on a scale \
            from 1 to 10, where 1 is terrible and 10 is great. As a reminder, the score you \
            gave at the start was "+str(initialHappinessScore)
            next_section = -1
            noOfResponseFragments = no_of_fragments_in_str_or_list(response)
            nextUserOptions = [""] # n/a because next user input type is not buttons
            nextUserInput = nextUserInputFinalHappinessSurvey
            nextUserInputType = "finalHappinessSurvey"
        else:
            response = choose_bot_wordy_response(message, clientId)
            next_section = section + 1
            noOfResponseFragments = no_of_fragments_in_str_or_list(response)
            nextUserOptions = [""] # n/a because next user input type is not buttons
            nextUserInput = nextUserInputFreeText
            nextUserInputType = "freeText"

        responseForWriteData = ""

        responseForWriteData = convert_array_or_string_to_string(response)
        # if isinstance(response,str):
        #     responseForWriteData = response
        # elif isinstance(response, list):
        #     for responseIndex in range(0,noOfResponseFragments):
        #         responseForWriteData = responseForWriteData + response[responseIndex]

        write_data(anonymous, conversationId, message, responseForWriteData, section, clientId)


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
        nextUserOptions = [""] # n/a because next user input type is not buttons
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"


        write_data("true", conversationId, "finalHappinessScore (!!) = "+message, response, section, clientId) # the "anonymous" variable is hardcoded as true here, because we're going to store this data regardless of whether the user has said anonymous or confidential


    elif section == -2: # this is the "end" (i.e. user has entered "stop") section

        response="Thank you for your feedback, and thank you for using the Talk It Over chatbot."

        next_section = -3
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = [""] # n/a because next user input type is not buttons
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

        write_data("true", conversationId, message, response, section, clientId) # the "anonymous" variable is hardcoded as true here, because we're going to store this data regardless of whether the user has said anonymous or confidential

    print("This is the data which gets sent to the client side")
    print([response, noOfResponseFragments, next_section, nextUserInput, nextUserInputType, anonymous, conversationId])
    outputs_dict = {"response" : response,
                    "noOfResponseFragments" : noOfResponseFragments,
                    "next_section" : next_section,
                    "nextUserOptions" : nextUserOptions,
                    "nextUserInput" : nextUserInput,
                    "nextUserInputType" : nextUserInputType,
                    "anonymous" : anonymous,
                    "conversationId" : conversationId}
    #return make_response(dumps([response, noOfResponseFragments, next_section, score, nextUserInput, nextUserInputType, anonymous, conversationId]))
    return outputs_dict