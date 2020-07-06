#import files
from flask import Flask, render_template, request, make_response, jsonify
from json import dumps
from datetime import datetime
import json
import time
#from textblob import TextBlob # was using this, but it doesn't seem to be working on Sanjay's machine
#import nltk
import random
import csv #check if this is still being used. i have a feeling we were going to use it but then decided against
app = Flask(__name__)
my_dict = {} # shoudl this be tidied up and deleted out?
sleep_per_word = 0.04 # I don't think this is being used yet, but could use it in the future
scores = [-0.5, 0, 0.3]
# The frontEnd variable is to switch the html text strings between the old and new versions
# frontEnd = "pre2020m04" # can take the values "pre2020m04" or "2020m04"
# At some point it would make sense to refactor out the frontEnd variable, because it's really a transitional thing
# the below encouragingNoises are things the bot might say to the user
encouragingNoises = ["I'm still listening, so feel free to say more.", "Go on talking, I'm still here.", \
"Keep talking, I'll be here for as long as you need me.", \
"I hear you. Keep going, I'm really happy for you to continue talking for as long as you need.", \
"Thanks for sharing this. Keep talking, I'm still here, and I'm still listening.", \
"I'm still here, so keep talking for as long as you need", "I'm still here, keep talking.", \
"Hmmm, thanks for sharing that. Keep talking, I'm still here", \
"Please keep on talking, I'm still here.", "Keep going, I'm still here", \
"Thanks for sharing. I'm still listening, so if you have more to say, please go on", \
"I hear you. Keep talking...", \
"Keep talking, I'm listening to you.", "Thanks for sharing, keep talking...", \
"I'm still listening, go on...", "I hear you, thank you for sharing, please keep talking", \
"Mhm, thanks for sharing this, please keep going", "Mhm, I hear you, go on talking",\
"I'm still here, feel free to continue talking as long as it's helping you", "Mhm, I hear you...",\
"Thank you for sharing. I'm still listening...", "I hear you. I'm still here...", "I hear you...",\
"Mhm, I hear you, thank you for sharing"]

noOfEncouragingNoises = len(encouragingNoises)
section = 0
dataToStore = []
USER_CHARACTER_COUNT = 0
conversationId = str(datetime.now())
iWantToKillMyselfResponseAlreadyUsed = [conversationId,False]
imGoingToKillMyselfResponseAlreadyUsed = [conversationId,False]
iWillDieTodayResponseAlreadyUsed = [conversationId,False]
iWantToDieResponseAlreadyUsed = [conversationId,False]
imFeelingSuicidalResponseAlreadyUsed = [conversationId,False]
#feelingQuiteSuicidalResponseAlreadyUsed : this varirable isn't being used
suicidalThoughtsResponseAlreadyUsed = [conversationId,False]
contemplatedSuicideButResponseAlreadyUsed = [conversationId,False]
iWishIWasDeadResponseAlreadyUsed = [conversationId,False]
betterOffDeadResponseAlreadyUsed = [conversationId,False]
iDontWantToLiveResponseAlreadyUsed = [conversationId,False]
sleepForeverResponseAlreadyUsed = [conversationId,False]
shouldIEndItResponseAlreadyUsed = [conversationId,False]
shouldIKillMyselfResponseAlreadyUsed = [conversationId,False]
suicideIsOnlyOptionResponseAlreadyUsed = [conversationId,False]
feelLikeEndingItResponseAlreadyUsed = [conversationId,False]
iWasRapedResponseAlreadyUsed = [conversationId,False]
cryingResponseAlreadyUsed = [conversationId,False]
iWantToCryResponseAlreadyUsed = [conversationId,False]
nothingToLiveForResponseAlreadyUsed = [conversationId,False]
singleWordDepressionResponseAlreadyUsed = [conversationId,False]
feelingDepressedResponseAlreadyUsed = [conversationId,False]
treatDepressionResponseAlreadyUsed = [conversationId,False]
iHaveDepressionResponseAlreadyUsed = [conversationId,False]
iMightHaveDepressionResponseAlreadyUsed = [conversationId, False]
iHaveNoWayOutResponseAlreadyUsed = [conversationId,False]
hadEnoughOfLifeResponseAlreadyUsed = [conversationId,False]
iWantToGiveUpOnLifeResponseAlreadyUsed = [conversationId,False]
nothingToLookForwardToResponseAlreadyUsed = [conversationId,False]
imUselessResponseAlreadyUsed = [conversationId,False]
imWorthlessResponseAlreadyUsed = [conversationId,False]
imNotLovedResponseAlreadyUsed = [conversationId,False]
imNotSpecialToAnyoneResponseAlreadyUsed = [conversationId,False]
iWantSomeoneToLoveMeResponseAlreadyUsed = [conversationId,False]
feelingLonelyResponseAlreadyUsed = [conversationId,False]
nobodyUnderstandsMeResponseAlreadyUsed = [conversationId,False]
imSickOfLockdownResponseAlreadyUsed = [conversationId,False]
iDontSleepResponseAlreadyUsed = [conversationId,False]
dontHaveAnyoneICanTalkToResponseAlreadyUsed = [conversationId,False]
iHateHowILookResponseAlreadyUsed = [conversationId,False]
loseWeightResponseAlreadyUsed = [conversationId, False]
feelOverwhelmedResponseAlreadyUsed = [conversationId,False]
aLotOnMyMindResponseAlreadyUsed = [conversationId,False]
feelingAwfulResponseAlreadyUsed = [conversationId,False]
feelLikeCryingResponseAlreadyUsed = [conversationId,False]
imAFailureResponseAlreadyUsed = [conversationId,False]
imALetdownResponseAlreadyUsed = [conversationId,False]
letMyselfDownResponseAlreadyUsed = [conversationId,False]
hardLifeResponseAlreadyUsed = [conversationId,False]
iHaveRegretsResponseAlreadyUsed = [conversationId,False]
underAchievedResponseAlreadyUsed = [conversationId,False]
hurtsMyFeelingsResponseAlreadyUsed = [conversationId,False]
hurtsToKnowThatResponseAlreadyUsed = [conversationId,False]
feelOutOfControlResponseAlreadyUsed = [conversationId,False]
feelLostResponseAlreadyUsed = [conversationId,False]
feelEmptyResponseAlreadyUsed = [conversationId,False]
inABadPlaceResponseAlreadyUsed = [conversationId,False]
imTrappedResponseAlreadyUsed = [conversationId,False]
nobodyCaresResponseAlreadyUsed = [conversationId,False]
noOneCaresAboutMeResponseAlreadyUsed = [conversationId,False]
deserveResponseAlreadyUsed = [conversationId,False]
iHateHowIFeelResponseAlreadyUsed = [conversationId,False]
imSadResponseAlreadyUsed = [conversationId,False]
feelingLowDownTerribleResponseAlreadyUsed = [conversationId,False]
iWantThisFeelingToGoAwayResponseAlreadyUsed = [conversationId,False]
imUpsetResponseAlreadyUsed = [conversationId,False]
hurtFeelingsResponseAlreadyUsed = [conversationId,False]
beingBulliedResponseAlreadyUsed = [conversationId,False]
iFeelHelplessResponseAlreadyUsed = [conversationId,False]
imAddictedResponseAlreadyUsed = [conversationId,False]
iHateCoronavirusResponseAlreadyUsed = [conversationId,False]
feelingRubbishResponseAlreadyUsed = [conversationId,False]
panicAttacksResponseAlreadyUsed = [conversationId,False]
iHaveAnxietyResponseAlreadyUsed = [conversationId,False]
imAnxiousResponseAlreadyUsed = [conversationId,False]
initial_imWorriedResponseAlreadyUsed = [conversationId,False]
second_imWorriedResponseAlreadyUsed = [conversationId,False]
iDontKnowWhatToDoResponseAlreadyUsed = [conversationId,False]
whatToDoWithMyselfResponseAlreadyUsed = [conversationId,False]
initial_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, False]
second_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, False]
personalHygieneResponseAlreadyUsed = [conversationId, False]
iSmellResponseAlreadyUsed = [conversationId, False]
wantToBeHappyResponseAlreadyUsed = [conversationId, False]
imNotHappyResponseAlreadyUsed = [conversationId,False]
iFeelNumbResponseAlreadyUsed = [conversationId,False]
iFeelStuckResponseAlreadyUsed = [conversationId, False]
imNotHappyResponseAlreadyUsed = [conversationId,False]
imNotSureWhereToTurnResponseAlreadyUsed = [conversationId,False]
iHateMyselfResponseAlreadyUsed = [conversationId,False]
abandonedMeResponseAlreadyUsed = [conversationId,False]
imStuckAtHomeResponseAlreadyUsed = [conversationId,False]
waitingToSeeIfPoliceAreGoingToChargeMeWithAnOffenceResponseAlreadyUsed = [conversationId,False]
imHomelessResponseAlreadyUsed = [conversationId,False]
iHaventSeenMyKidsResponseAlreadyUsed = [conversationId,False]
difficultDayResponseAlreadyUsed = [conversationId,False]
# stressingMeOutResponseAlreadyUsed = [conversationId,False]
familyProblemsResponseAlreadyUsed = [conversationId,False]
gotDumpedResponseAlreadyUsed = [conversationId,False]
brokeUpWithPartnerResponseAlreadyUsed = [conversationId,False]
canYouHelpResponseAlreadyUsed = [conversationId,False]
feelLostResponseAlreadyUsed = [conversationId,False]
iWantFreedomResponseAlreadyUsed = [conversationId,False]
whoCanITalkToResponseAlreadyUsed = [conversationId,False]
howAreYouResponseAlreadyUsed = [conversationId,False]
whatDoYouThinkResponseAlreadyUsed = [conversationId,False]
imPregnantResponseAlreadyUsed = [conversationId,False]
imBeingTakenForGrantedResponseAlreadyUsed = [conversationId,False]
itsStressingMeOutResponseAlreadyUsed = [conversationId,False]
familyProblemsResponseAlreadyUsed = [conversationId,False]
fallOutResponseAlreadyUsed = [conversationId,False]
abuseResponseAlreadyUsed = [conversationId,False]
heartBreakResponseAlreadyUsed = [conversationId,False]
iWantAFriendResponseAlreadyUsed = [conversationId,False]
iDontSeeManyPeopleResponseAlreadyUsed = [conversationId,False]
feelLostResponseAlreadyUsed = [conversationId,False]
helpResponseAlreadyUsed = [conversationId,False]
# iWantFreedomResponseAlreadyUsed = [conversationId,False]
# whoCanITalkToResponseAlreadyUsed = [conversationId,False]
howAreYouResponseAlreadyUsed = [conversationId,False]
doYouGiveAdviceResponseAlreadyUsed = [conversationId,False]
dontKnowResponseAlreadyUsed = [conversationId,False]
whatDoYouThinkResponseAlreadyUsed = [conversationId,False]
imGoingToGoNowResponseAlreadyUsed = [conversationId,False]
areYouReadingResponseAlreadyUsed = [conversationId,False]
lettingMeGetMyThoughtsOutOfMyHeadResponseAlreadyUsed = [conversationId,False]
idkWhatElseToSayToYouResponseAlreadyUsed = [conversationId,False]
thankYouResponseAlreadyUsed = [conversationId, False]
shortResponseAlreadyUsed = [conversationId,False]
areYouABotResponseAlreadyUsed = [conversationId,False]
willYouConverseWithMeResponseAlreadyUsed = [conversationId,False]
thisBotIsBadResponseAlreadyUsed = [conversationId,False]

####### TODO TODO TODO ###################################
## Implement a separate css class for confidential text
## Maybe consider having a button which the user can press to say "you didn't understand me"
## Instead of the user's response being a dropdown, change it to a button so that it can be sized appropriately (i.e. not be tiny on a mobile screen)
## Correct the current bug: currently the system won't choose responses correctly if multiple users in parallel (or even in series)
## Do a refactor (maybe use more object oriented programming????)
## One thing to refactor: all the blahblahAlreadyUsed variables could be replaced with a dict?
## Currently have hardcoded "if section == 11" statements. replace these by having a variable for "numberOfInitialSections" = 10. Make sure it's global. If the user's first message is "hello", then increment the number of initial sections variable
## Stop button sometimes gets hit the moment it appears. Current fix is to add some wording; could consider something better?
## ADD IN WILDCARD BETWEEN "ITS NOT THAT" AND "STRING" WHERE APPLICABLE
## ADD IN SOMETHING FOR "YOU ARE NOT HELPING" OR "THIS IS NOT HELPING" OR "YOU ARE USELESS"
## Rules around selfharm / DSH / cutting -- this is still a gap
## Rules for relationships -- this comes up a lot, and I currently can't think of something good to say
## Rule for pandemic/corona/covid
## Longer term: would be great to be able to summarise back what the user has said (but this is hard!)
##########################################################



def initialiseResponseAlreadyUsedVariables():
    ## this function gets called *within* the app route, to make sure that the variables get initialised correctly
    ## note the structure of the variables: it includes the conversationId; this is to ensure that
    ## the app doesn't get confused when two users are using the bot concurrently (or, indeed, one after the other?)
    global conversationId
    print("This statement is in initialiseResponseAlreadyUsedVariables. conversationId = "+conversationId)
    iWantToKillMyselfResponseAlreadyUsed = [conversationId,False]
    imGoingToKillMyselfResponseAlreadyUsed = [conversationId,False]
    iWillDieTodayResponseAlreadyUsed = [conversationId,False]
    iWantToDieResponseAlreadyUsed = [conversationId,False]
    imFeelingSuicidalResponseAlreadyUsed = [conversationId,False]
    #feelingQuiteSuicidalResponseAlreadyUsed : this varirable isn't being used
    suicidalThoughtsResponseAlreadyUsed = [conversationId,False]
    contemplatedSuicideButResponseAlreadyUsed = [conversationId,False]
    iWishIWasDeadResponseAlreadyUsed = [conversationId,False]
    betterOffDeadResponseAlreadyUsed = [conversationId,False]
    iDontWantToLiveResponseAlreadyUsed = [conversationId,False]
    sleepForeverResponseAlreadyUsed = [conversationId,False]
    shouldIEndItResponseAlreadyUsed = [conversationId,False]
    shouldIKillMyselfResponseAlreadyUsed = [conversationId,False]
    suicideIsOnlyOptionResponseAlreadyUsed = [conversationId,False]
    feelLikeEndingItResponseAlreadyUsed = [conversationId,False]
    iWasRapedResponseAlreadyUsed = [conversationId,False]
    cryingResponseAlreadyUsed = [conversationId,False]
    iWantToCryResponseAlreadyUsed = [conversationId,False]
    nothingToLiveForResponseAlreadyUsed = [conversationId,False]
    singleWordDepressionResponseAlreadyUsed = [conversationId,False]
    feelingDepressedResponseAlreadyUsed = [conversationId,False]
    treatDepressionResponseAlreadyUsed = [conversationId,False]
    iHaveDepressionResponseAlreadyUsed = [conversationId,False]
    iMightHaveDepressionResponseAlreadyUsed = [conversationId,False]
    iHaveNoWayOutResponseAlreadyUsed = [conversationId,False]
    hadEnoughOfLifeResponseAlreadyUsed = [conversationId,False]
    iWantToGiveUpOnLifeResponseAlreadyUsed = [conversationId,False]
    nothingToLookForwardToResponseAlreadyUsed = [conversationId,False]
    imUselessResponseAlreadyUsed = [conversationId,False]
    imWorthlessResponseAlreadyUsed = [conversationId,False]
    imNotLovedResponseAlreadyUsed = [conversationId,False]
    imNotSpecialToAnyoneResponseAlreadyUsed = [conversationId,False]
    iWantSomeoneToLoveMeResponseAlreadyUsed = [conversationId,False]
    feelingLonelyResponseAlreadyUsed = [conversationId,False]
    nobodyUnderstandsMeResponseAlreadyUsed = [conversationId,False]
    imSickOfLockdownResponseAlreadyUsed = [conversationId,False]
    iDontSleepResponseAlreadyUsed = [conversationId,False]
    dontHaveAnyoneICanTalkToResponseAlreadyUsed = [conversationId,False]
    iHateHowILookResponseAlreadyUsed = [conversationId,False]
    loseWeightResponseAlreadyUsed = [conversationId, False]
    feelOverwhelmedResponseAlreadyUsed = [conversationId,False]
    aLotOnMyMindResponseAlreadyUsed = [conversationId,False]
    feelingAwfulResponseAlreadyUsed = [conversationId,False]
    feelLikeCryingResponseAlreadyUsed = [conversationId,False]
    imAFailureResponseAlreadyUsed = [conversationId,False]
    imALetdownResponseAlreadyUsed = [conversationId,False]
    letMyselfDownResponseAlreadyUsed = [conversationId,False]
    hardLifeResponseAlreadyUsed = [conversationId,False]
    iHaveRegretsResponseAlreadyUsed = [conversationId,False]
    underAchievedResponseAlreadyUsed = [conversationId,False]
    hurtsMyFeelingsResponseAlreadyUsed = [conversationId,False]
    hurtsToKnowThatResponseAlreadyUsed = [conversationId,False]
    feelOutOfControlResponseAlreadyUsed = [conversationId,False]
    feelLostResponseAlreadyUsed = [conversationId,False]
    feelEmptyResponseAlreadyUsed = [conversationId,False]
    inABadPlaceResponseAlreadyUsed = [conversationId,False]
    imTrappedResponseAlreadyUsed = [conversationId,False]
    nobodyCaresResponseAlreadyUsed = [conversationId,False]
    noOneCaresAboutMeResponseAlreadyUsed = [conversationId,False]
    deserveResponseAlreadyUsed = [conversationId,False]
    iHateHowIFeelResponseAlreadyUsed = [conversationId,False]
    imSadResponseAlreadyUsed = [conversationId,False]
    feelingLowDownTerribleResponseAlreadyUsed = [conversationId,False]
    iWantThisFeelingToGoAwayResponseAlreadyUsed = [conversationId,False]
    imUpsetResponseAlreadyUsed = [conversationId,False]
    hurtFeelingsResponseAlreadyUsed = [conversationId,False]
    beingBulliedResponseAlreadyUsed = [conversationId,False]
    iFeelHelplessResponseAlreadyUsed = [conversationId,False]
    imAddictedResponseAlreadyUsed = [conversationId,False]
    iHateCoronavirusResponseAlreadyUsed = [conversationId,False]
    feelingRubbishResponseAlreadyUsed = [conversationId,False]
    panicAttacksResponseAlreadyUsed = [conversationId,False]
    iHaveAnxietyResponseAlreadyUsed = [conversationId,False]
    imAnxiousResponseAlreadyUsed = [conversationId,False]
    initial_imWorriedResponseAlreadyUsed = [conversationId,False]
    second_imWorriedResponseAlreadyUsed = [conversationId,False]
    iDontKnowWhatToDoResponseAlreadyUsed = [conversationId,False]
    whatToDoWithMyselfResponseAlreadyUsed = [conversationId,False]
    initial_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, False]
    second_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, False]
    personalHygieneResponseAlreadyUsed = [conversationId, False]    
    iSmellResponseAlreadyUsed = [conversationId, False]
    wantToBeHappyResponseAlreadyUsed = [conversationId, False]
    imNotHappyResponseAlreadyUsed = [conversationId,False]
    iFeelNumbResponseAlreadyUsed = [conversationId,False]
    iFeelStuckResponseAlreadyUsed = [conversationId, False]
    imNotHappyResponseAlreadyUsed = [conversationId,False]
    imNotSureWhereToTurnResponseAlreadyUsed = [conversationId,False]
    iHateMyselfResponseAlreadyUsed = [conversationId,False]
    abandonedMeResponseAlreadyUsed = [conversationId,False]
    imStuckAtHomeResponseAlreadyUsed = [conversationId,False]
    waitingToSeeIfPoliceAreGoingToChargeMeWithAnOffenceResponseAlreadyUsed = [conversationId,False]
    imHomelessResponseAlreadyUsed = [conversationId,False]
    iHaventSeenMyKidsResponseAlreadyUsed = [conversationId,False]
    difficultDayResponseAlreadyUsed = [conversationId,False]
    # stressingMeOutResponseAlreadyUsed = [conversationId,False]
    familyProblemsResponseAlreadyUsed = [conversationId,False]
    gotDumpedResponseAlreadyUsed = [conversationId,False]
    brokeUpWithPartnerResponseAlreadyUsed = [conversationId,False]
    canYouHelpResponseAlreadyUsed = [conversationId,False]
    feelLostResponseAlreadyUsed = [conversationId,False]
    iWantFreedomResponseAlreadyUsed = [conversationId,False]
    whoCanITalkToResponseAlreadyUsed = [conversationId,False]
    howAreYouResponseAlreadyUsed = [conversationId,False]
    whatDoYouThinkResponseAlreadyUsed = [conversationId,False]
    imPregnantResponseAlreadyUsed = [conversationId,False]
    imBeingTakenForGrantedResponseAlreadyUsed = [conversationId,False]
    itsStressingMeOutResponseAlreadyUsed = [conversationId,False]
    familyProblemsResponseAlreadyUsed = [conversationId,False]
    fallOutResponseAlreadyUsed = [conversationId,False]
    abuseResponseAlreadyUsed = [conversationId,False]
    heartBreakResponseAlreadyUsed = [conversationId,False]
    iWantAFriendResponseAlreadyUsed = [conversationId,False]
    iDontSeeManyPeopleResponseAlreadyUsed = [conversationId,False]
    feelLostResponseAlreadyUsed = [conversationId,False]
    helpResponseAlreadyUsed = [conversationId,False]
    # iWantFreedomResponseAlreadyUsed = [conversationId,False]
    # whoCanITalkToResponseAlreadyUsed = [conversationId,False]
    howAreYouResponseAlreadyUsed = [conversationId,False]
    doYouGiveAdviceResponseAlreadyUsed = [conversationId,False]
    dontKnowResponseAlreadyUsed = [conversationId,False]
    whatDoYouThinkResponseAlreadyUsed = [conversationId,False]
    imGoingToGoNowResponseAlreadyUsed = [conversationId,False]
    areYouReadingResponseAlreadyUsed = [conversationId,False]
    lettingMeGetMyThoughtsOutOfMyHeadResponseAlreadyUsed = [conversationId,False]
    idkWhatElseToSayToYouResponseAlreadyUsed = [conversationId,False]
    thankYouResponseAlreadyUsed = [conversationId, False]
    shortResponseAlreadyUsed = [conversationId,False]
    areYouABotResponseAlreadyUsed = [conversationId,False]
    willYouConverseWithMeResponseAlreadyUsed = [conversationId,False]
    thisBotIsBadResponseAlreadyUsed = [conversationId,False]


# returns the first index where an element occurs.
# not using this at time of writing; if we don't end up using this, could delete it out at next refactor
def bisect_left(a, x):

    hi = len(a)
    lo = 0
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] >= x: hi = mid
        else: lo+=1
    return lo

# get a response message from a yes, no answer
# currently not being used. could delete this???????
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

def write_data(anonymous, conversationId, message, response, section, clientId):
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
    if anonymous=="true" or section <= 10:  # note: this is bad practice; shouldn't hardcode the number of sections
        message = message.replace(",", "¬")
        response = response.replace(",", "¬")

        with open('storedData.csv', 'a') as f:
            dataToStore = [str(conversationId), "User says:",str(message), "Chatbot says:",str(response), clientId]
            f.write("\n" + str(dataToStore))
    return None

def next_user_input_one(buttonText_array, clientId):
    ## when we send certain strings of html to the client side, this function helps with that
    if clientId == "originalJavascriptClient":
        html_text = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
        <option>Select</option>  \
        <option value='"+buttonText_array[0]+"'>"+buttonText_array[0]+"</option> \
        </select>"
    elif clientId == "bootstrapJavascriptClient":
        #html_text = "<select class='message_input' type='text' id='userInputButton' onchange='sendMessage()'> \
        html_text = "<select class='message_input' type='text' id='userInputButton'> \
        <option selected disabled>Select</option>  \
        <option value='"+buttonText_array[0]+"'>"+buttonText_array[0]+"</option> \
        </select>"
    else:
        html_text = buttonText_array[0] # in this scenario we're expecting that the client is the API, and therefore won't need any html text
    return html_text

def next_user_input_two(buttonText_array,clientId):
    ## when we send certain strings of html to the client side, this function helps with that
    if clientId == "originalJavascriptClient":
        html_text = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
        <option>Select</option>  \
        <option value='"+buttonText_array[0]+"'>"+buttonText_array[0]+"</option> \
        <option value='"+buttonText_array[1]+"'>"+buttonText_array[1]+"</option> \
        </select>"
    elif clientId == "bootstrapJavascriptClient":
        #html_text = "<select class='message_input' type='text' id='userInputButton' onchange='sendMessage()'> \
        html_text = "<select class='message_input' type='text' id='userInputButton'> \
        <option selected disabled>Select</option>  \
        <option value='"+buttonText_array[0]+"'>"+buttonText_array[0]+"</option> \
        <option value='"+buttonText_array[1]+"'>"+buttonText_array[1]+"</option> \
        </select>"
    else:
        html_text = buttonText_array[0]+buttonText_array[1] # in this scenario we're expecting that the client is the API, and therefore won't need any html text. In fact, I'm not expecting thi s to be used at all.
    return html_text

def convert_array_or_string_to_string(array_or_string):
    """
    Takes a variable which may be either an array or a string and converts it to a string by either:
    -- if it's a string, do nothing
    -- if it's an array of strings, just concatenate all the elements of the array
    If the array contains something other htan strings, that will be problematic
    """

    output_string = ""
    if isinstance(array_or_string,str):
        output_string = array_or_string
    elif isinstance(array_or_string, list):
        for i in range(0,len(array_or_string)):
            output_string = output_string + array_or_string[i]

    return output_string

def no_of_fragments_in_str_or_list(response):
    """
    Sometimes the bot response is just one fragment; at other times one fragment will appear,...
    ... and then a typing ellipsis will appear for a moment, and then another fragment.
    This function counts the number of fragments
    """
    noOfResponseFragments = 0
    if isinstance(response,list):
        noOfResponseFragments = len(response)
    elif isinstance(response,str):
        noOfResponseFragments = 1
    else:
        print("Error: expecting the response variable to be either a string or a list, otherwise don't know how to set the noOfResponseFragments variable")
    return noOfResponseFragments

def choose_bot_wordy_response(message, clientId):
    """
    In the free text section of the bot, this function chooses what the bot says.
    This function is called in the get_bot_response function. EDIT: it's now called in the bot_processing function (changed that function's name)
    The function chooses by searching the user's message for a keyword, according to a priority ranking.
    There are specific bot responses to give for each keyword.
    If no keyword is found, a randomly generated encouraging phrase is chosen
    """

    ## KEYWORDS

    # iWantToKillMyself
    # iWantToDie
    # feelingSuicidal
    # feelingQuiteSuicidal
    # suicidalThoughts
    # contemplatedSuicideBut
    # crying
    # nothingToLiveFor
    # singleWordDepression
    # feelingDepressed
    # treatDepression
    # iHaveNoWayOut
    # hadEnoughOfLife
    # nothingToLookForwardTo
    # imUseless
    # imWorthless
    # feelingLonely
    # nobodyUnderstandsMe
    # dontHaveAnyoneICanTalkTo
    # iHateHowILook
    # loseWeight
    # feelOverwhelmed
    # aLotOnMyMind
    # feelingAwful
    # feelLikeCrying
    # letMyselfDown
    # feelOutOfControl
    # feelLost
    # inABadPlace
    # imTrapped
    # nobodyCares
    # deserve
    # imSad
    # feelingLowDownTerrible
    # imUpset
    # hurtFeelings
    # beingBullied
    # imAddicted
    # feelingRubbish
    # panicAttacks
    # iDontKnowWhatToSay
    # personalHygiene
    # iSmell
    # WantToBeHappy
    # imNotHappy
    #iFeelNumb
    # iHateMyself
    # difficultDay
    # stressingMeOut
    # familyProblems
    # gotDumped
    # brokeUpWithPartner
    # canYouHelp
    # feelLost
    # iWantFreedom
    # whoCanITalkTo
    # howAreYou
    # whatDoYouThink
    # doYouGiveAdvice



    global USER_CHARACTER_COUNT

    itsNotThatArray = ["it's not that", "its not that", "it's not tat", "its not tat",\
                        "i don't think", "i dont think", "i don't thnk", "i dont thnk",\
                        "i don't believe", "i dont believe", "i don't belive", "i dont belive",\
                        "i don't feel", "i dont feel",\
                        "i don't reckon", "i dont reckon",\
                        "i don't think that", "i dont think that", "i don't thnk that", "i dont thnk that",\
                        "i don't believe that", "i dont believe that", "i don't belive that", "i dont belive that",\
                        "i don't feel that", "i dont feel that",\
                        "i don't reckon that", "i dont reckon that", "i wouldn’t say that", "i would not say that", "i wouldn't necessarily say that",\
                        "i would not necessarily say that"]
    # this section creates arrays of synonyms relating to things which a user might say. Typically each element
    # of the array is an "equivalence class", by which I mean that they are basically the same thing, but
    # might differ only in terms of anticipating typos, or perhaps including intensifiers (like "really")
    iWantToKillMyselfArray = ["i want to commit suic", "i want to kill myself", "i want to kill my self", "i want to kill mysefl", "i want to kill my sefl", "i wanna kill myself", "i wanna kill my self", "i wanna kill mysefl", "i wanna kill my sefl",\
                            "i just want to kill myself", "i just want to kill my self", "i just want to kill mysefl", "i just want to kill my sefl", "i just wanna kill myself", "i just wanna kill my self", "i just wanna kill mysefl", "i just wanna kill my sefl",\
                            "i still just want to kill myself", "i still just want to kill my self", "i still just want to kill mysefl", "i still just want to kill my sefl", "i still just wanna kill myself", "i still just wanna kill my self", "i still just wanna kill mysefl", "i still just wanna kill my sefl",\
                            "i still want to kill myself", "i still want to kill my self", "i still want to kill mysefl", "i still want to kill my sefl", "i still wanna kill myself", "i still wanna kill my self", "i still wanna kill mysefl", "i still wanna kill my sefl",\
                            "i really want to kill myself", "i really want to kill my self", "i really want to kill mysefl", "i really want to kill my sefl", "i really wanna kill myself", "i really wanna kill my self", "i really wanna kill mysefl", "i really wanna kill my sefl",\
                            "i just really want to kill myself", "i just really want to kill my self", "i just really want to kill mysefl", "i just really want to kill my sefl", "i just really wanna kill myself", "i just really wanna kill my self", "i just really wanna kill mysefl", "i just really wanna kill my sefl",\
                            "i still just really want to kill myself", "i still just really want to kill my self", "i still just really want to kill mysefl", "i still just really want to kill my sefl", "i still just really wanna kill myself", "i still just really wanna kill my self", "i still just really wanna kill mysefl", "i still just really wanna kill my sefl",\
                            "i still really want to kill myself", "i still really want to kill my self", "i still really want to kill mysefl", "i still really want to kill my sefl", "i still really wanna kill myself", "i still really wanna kill my self", "i still really wanna kill mysefl", "i still really wanna kill my sefl",
                            "i want to take my life", "i wanna take my life", "i want to take my own life", "i wanna take my own life", "i still really want to kill myself", "i still really want to kill my self", "i still really want to kill mysefl", "i still really want to kill my sefl", "i still really wanna kill myself", \
                            "i still really wanna kill my self", "i still really wanna kill mysefl", "i still really wanna kill my sefl", "i want to end it all", "i want to commit suic"]
    imGoingToKillMyselfArray = ["going to kill myself", "going to kill my self", "oging to kill myself", "oging to kill my self", \
                                "i will kill myself", "i will kill my self","ill kill myself", "ill kill my self"]
    iWillDieTodayArray = ["i will die today", "i'll die today", "i am going to die today"]
    #imPlanningToKillMyselfArray = ["im planning to kill myself", "i am planning to kill myself"]
    # have not built in anything for imPlanningToKillMyselfArray apart from the array itself. Maybe come back to this?
    iWantToDieArray = ["i want to die", "i wanna die", "i would like to die", "i have become suic", "ive become suic"]
    imFeelingSuicidalArray = ["i feel suic", "i'm feeling suic", "im feeling suic", "i just feel suic", "i'm just feeling suic", "im just feeling suic", "i'm suic", "im suic", "i am suic",\
                            "i feel sucid", "i'm feeling sucid", "im feeling sucid", "i just feel sucid", "i'm just feeling sucid", "im just feeling sucid", "i'm sucid", "im sucid", "i am sucid",\
                            "i still feel suic", "i'm still feeling suic", "im still feeling suic", "i still just feel suic", "i'm still just feeling suic", "im still just feeling suic", "i'm still suic", "im still suic",\
                            "i still feel sucid", "i'm still feeling sucid", "im still feeling sucid", "i still just feel sucid", "i'm still just feeling sucid", "im still just feeling sucid", "i'm still sucid", "im still sucid",
                            "im starting to feel suic", "i am starting to feel suic", "i have started to feel suic",
                            "im starting to feel sucid", "i am starting to feel sucid", "i have started to feel sucid",
                            "i am feeling suic", "i am feeling sucid", "i am feeling extremely suicidal", "feeling extremely suic"]
    imFeelingQuiteSuicidalArray = ["i feel quite suic", "i'm feeling quite suic", "im feeling quite suic", "i just feel quite suic", "i'm just feeling quite suic", "im just feeling quite suic",\
                                   "i feel quite sucid", "i'm feeling quite sucid", "im feeling quite sucid", "i just feel quite sucid", "i'm just feeling quite sucid", "im just feeling quite sucid",\
                                   "i still feel quite suic", "i'm still feeling quite suic", "im still feeling quite suic", "i still just feel quite suic", "i'm still just feeling quite suic", "im still just feeling quite suic",\
                                    "i still feel quite sucid", "i'm still feeling quite sucid", "im still feeling quite sucid", "i still just feel quite sucid", "i'm still just feeling quite sucid", "im still just feeling quite sucid"]
    imThinkingAboutKillingMyselfArray = ["im thinking about killing myself", "i am thinking about killing myself", "i have had thoughts of shooting myself", "i have had some thoughts of shooting myelf"]
    # have not built in anything for imThinkingAboutKillingMyselfArray apart from the array itself. Maybe come back to this?
    iveBeenFeelingSuicidalArray = ["i've been feeling suic", "ive been feeling suic", "i've just been feeling suic", "ive just been feeling suic",\
                            "i've been feeling sucid", "ive been feeling sucid", "i've just been feeling sucid", "ive just been feeling sucid",]
    suicidalThoughtsArray = ["i have suicidal thoughts", "i have suicidal thoughts", "i have been having suicidal thoughts", "ive been having suicidal thoughts",
                            "i have suicidle  thoughts", "i have suicidle  thoughts", "i have been having suicidle  thoughts", "ive been having suicidle  thoughts"\
                            "i have had thoughts of shooting myself", "i have had some thoughts of shooting myelf"]
    contemplatedSuicideButArray = ["i have thought about killing myself but", "i have contemplated killing myself but", "i have thought about ending my life but", "i have contemplated ending my life but",\
                            "i have thought about suicide but", "i have contemplated suicide but"]
    iWishIWasDeadArray = ["i wish i could die", "i wish i was dead"]   
    betterOffDeadArray = ["i would be better off dead", "id be better off dead", "better off if I weren't alive"]                     
    iDontWantToLiveArray = ["i dont want to live", "i no longer want to live", "i dont wanna live", "i have no desire to live", "i no longer desire to live",
                            "i dont want to be alive", "i no longer want to be alive", "i dont wanna be alive", "i have no desire to be alive", "i no longer desire to be alive",
                            "i dont want to remain alive", "i no longer want to remain alive", "i dont wanna remain alive", "i have no desire to remain alive", "i no longer desire to remain alive",
                            "i dont want to stay alive", "i no longer want to stay alive", "i dont wanna stay alive", "i have no desire to stay alive", "i no longer desire to stay alive",
                            "i hate my life", "i hate being alive", "i hate the fact that im alive", "i hate living", "i hate the fact that i'm living"]
    sleepForeverArray = ["i want to go to sleep and never wake up", "i want to go to sleep and not wake up", "i go to bed hoping i won't wake up", "i go to bed hoping i don't wake up", \
                        "i sometimes go to bed hoping i won't wake up", "i sometimes go to bed hoping i don't wake up"]
    shouldIEndItArray = ["should i end it"]
    shouldIKillMyselfArray = ["should i kill myself", "should i commit suicide", "should i end my life", "should i end it all"]
    suicideIsOnlyOptionArray = ["ending my life feels like the only option", "killing myself feels like the only option", "suicide feels like the only option", "ending my life seems like the only option", \
                            "killing myself seems like the only option", "suicide seems like the only option", "ending my life feels like the only way forward", \
                            "killing myself feels like the only way forward", "suicide feels like the only way forward", "ending my life seems like the only way forward", \
                            "killing myself seems like the only way forward", "suicide seems like the only way forward"]
    feelLikeEndingItArray = ["i feel like ending it"]
    iWasRapedArray = ["raped me", "ive been raped", "i have been raped", "i was raped"]
    imCryingArray = ["i can't stop crying","i cant stop crying", "makes me want to cry", "makes me wanna cry", "i'm crying", "im crying", "i've been crying", "ive been crying", "making me want to cry", "making me wanna cry", "i cry myself"]
    ## Note: imCryingArray doesn't contain the string "i cry" because the test involves removing the space characters,
    ## so a message containing something like "mimicry" would trigger the "i cry" response
    iWantToCryArray = ["i want to cry", "i wanna cry"]
    nothingToLiveForArray = ["i have nothing to live for", "i've nothing to live for", "i have nothing left to live for", "i've nothing left to live for", "i have no reason to live", "theres no point in me living",\
                            "i have nothing to be alive for", "i've nothing to be alive for", "i have nothing left to be alive for", "i've nothing left to be alive for", "i have no reason to be alive", "theres no point in me being alive",  "theres no point in my being alive",
                            "i have nothing to stay alive for", "i've nothing to stay alive for", "i have nothing left to stay alive for", "i've nothing left to stay alive for", "i have no reason to stay alive", "theres no point in me staying alive", "theres no point in my staying alive",
                            "i have nothing to remain alive for", "i've nothing to remain alive for", "i have nothing left to remain alive for", "i've nothing left to remain alive for", "i have no reason to remain alive", \
                            "theres no point in me remaining alive", "theres no point in my remaining alive", "theres no reason for me to be alive", "there is no reason for me to be alive", "i have no reason to be alive",\
                            "there isn't any reason for me to be alive", "i don’t have a reason to be alive", "i don’t have any reason to be alive"]

    iHateMyselfArray = [" hate myself", " hate my self", " hate my sefl", " hate mysefl",]
    singleWordDepressionMessageArray = ["depression", "depressed", "depresssion", "depresssed", "dperessed", "dperession"  ]
    feelingDepressedArray = ["i feel depressed", "i just feel depressed", "i feeel depressed", "i just feeel depressed", "im feeling depressed", "i'm feeling depressed", "im just feeling depressed", "i'm just feeling depressed", "i feel very depressed", "i feel so depressed", "i am feeling depressed", "i'm feeling really depressed", "i'm feeling so depressed", "im feeling really depressed", "im feeling so depressed",\
                            "i'm depressed", "im depressed", "i am depressed", "i'm so depressed", "im so depressed", "i am so depressed", "i'm really depressed", "im really depressed", "i am really depressed",\
                            "im more depressed than ever", "i'm more depressed than ever", "i developed depression"]
    treatDepressionArray = ["what are treatments for depression", "what are the treatments for depression", "how can I treat depression", "how can I treat my depression", "whats the treatment for depression"]
    iHaveDepressionArray = ["i have depression"]
    iMightHaveDepressionArray = ["i might have depression", "i may have depression", "i possibly have depression"]
    iHaveNoWayOutArray = ["i have no way out", "i don't feel i have any way out", "i dont feel i have any way out", "i don't have any way out", "i dont have any way out", "i haven't got any way out", "ive got no way out", "ive no got any way out", "i don't feel i have any way out", "i dont feel i have any way out", "i don't feel i have got any way out", "i dont feel i have got any way out", "i don't have any way out", "i dont have any way out"]
    hadEnoughOfLifeArray = ["i've had enough of life", "ive had enough of life", "i have had enough of life", "i had enough of life"]
    iWantToGiveUpOnLifeArray = ["i want to give up on life", "i want to give up on being alive", "i wanna give up on life", "i dont want to bother with life", "i dont want to bother being alive", "there is no reason for me to be alive", "theres no reason for me to be alive", "there is no reason for me to stay alive", "theres no reason for me to stay alive", "there is no reason for me to live", "theres no reason for me to live"]
    nothingToLookForwardToArray = ["i have nothing to look forward to", "i don't have anything to look forward to", "i've got nothing to look forward to", \
                                "i literally have nothing to look forward to", "i literally don't have anything to look forward to", "i have literally nothing to look forward to", "i've literally got nothing to look forward to"\
                                "i just have nothing to look forward to", "i just don't have anything to look forward to", "i've just got nothing to look forward to",\
                                 "i've literally just got nothing to look forward to"]
    imUselessArray = ["im useless", "i'm useless", "im uselses", "i'm uselses","im usless", "i'm usless",\
                    "im so useless", "i'm so useless", "im so uselses", "i'm so uselses","im usless", "i'm usless",\
                    "im really useless", "i'm really useless", "im really uselses", "i'm really uselses","im usless", "i'm usless",\
                    "im totally useless", "i'm totally useless", "im totally uselses", "i'm totally uselses","im usless", "i'm usless",\
                    "im utterly useless", "i'm utterly useless", "im utterly uselses", "i'm utterly uselses", "im usless", "i'm usless",\
                    "im just useless", "i'm just useless", "im just uselses", "i'm just uselses","im just usless", "i'm just usless",\
                    "im just so useless", "i'm just so useless", "im just so uselses", "i'm just so uselses","im just usless", "i'm just usless",\
                    "im just really useless", "i'm just really useless", "im just really uselses", "i'm just really uselses","im just usless", "i'm just usless",\
                    "im just totally useless", "i'm just totally useless", "im just totally uselses", "i'm just totally uselses","im just usless", "i'm just usless",\
                    "im just utterly useless", "i'm just utterly useless", "im just utterly uselses", "i'm just utterly uselses", "im just usless", "i'm just usless"]
    imWorthlessArray = ["im worthless", "i'm worthless", "im worthlses", "i'm worthlses",\
                    "im so worthless", "i'm so worthless", "im so worthlses", "i'm so worthlses",\
                    "im really worthless", "i'm really worthless", "im really worthlses", "i'm really worthlses",\
                    "im totally worthless", "i'm totally worthless", "im totally worthlses", "i'm totally worthlses",\
                    "im utterly worthless", "i'm utterly worthless", "im utterly worthlses", "i'm utterly worthlses",\
                    "im just worthless", "i'm just worthless", "im just worthlses", "i'm just worthlses",\
                    "im just so worthless", "i'm just so worthless", "im just so worthlses", "i'm just so worthlses",\
                    "im just really worthless", "i'm just really worthless", "im just really worthlses", "i'm just really worthlses",\
                    "im just totally worthless", "i'm just totally worthless", "im just totally worthlses", "i'm just totally worthlses",\
                    "im just utterly worthless", "i'm just utterly worthless", "im just utterly worthlses", "i'm just utterly worthlses",\
                    "i feel worthless", "i'm just utterly worthless", "im just utterly worthlses", "i'm just utterly worthlses"]
    imNotLovedArray = ["im not loved", "nobody loves me", "i dont feel loved"]
    imNotSpecialToAnyoneArray = ["im not special to anyone", "there isn't anyone for whom im special"]
    iWantSomeoneToLoveMeArray = ["i want someone to love me", "i want to be loved"]
    feelingLonelyArray = ["i sit alone", "i feel lonely", "im feeling lonely", "i am feeling lonely","making me feel lonely", "making me lonely","makes me feel lonely", "makes me lonely",
                        "i feel alone", "im feeling alone", "i am feeling alone", "making me feel alone", "making me alone","makes me feel alone", "makes me alone",
                        "i feel sad and lonely", "im feeling sad and lonely", "i am feeling sad and lonely","making me feel sad and lonely", "making me sad and lonely", "makes me feel sad and lonely", "makes me sad and lonely",
                        "i feel low and lonely", "im feeling low and lonely", "i am feeling low and lonely", "making me feel low and lonely", "making me low and lonely", "makes me feel low and lonely", "makes me low and lonely",
                        "i feel sad and alone", "im feeling sad and alone", "i am feeling sad and alone", "making me feel sad and alone", "making me sad and alone", "makes me feel sad and alone", "makes me sad and alone",
                        "i feel low and alone", "im feeling low and alone", "i am feeling low and alone", "making me feel low and alone", "making me low and alone", "makes me feel low and alone", "makes me low and alone",
                        "i feel isolated", "im feeling isolated", "i am feeling isolated", "making me feel isolated", "making me isolated", "makes me feel isolated", "makes me isolated",
                        "i feel sad and isolated", "im feeling sad and isolated", "i am feeling sad and isolated", "making me feel sad and isolated", "making me sad and isolated", "makes me feel sad and isolated", "makes me sad and isolated",
                            "im a lonely person", "i am a lonely person", "im a sad lonely person", "i am a sad lonely person",
                        "i am lonely", "im lonely", "i am lonely","making me lonely", "making me lonely","makes me lonely", "makes me lonely",
                        "im alone", "i am alone", "making me alone", "making me alone","makes me alone", "makes me alone",
                        "im sad and lonely", "i am sad and lonely","making me sad and lonely", "making me sad and lonely", "makes me sad and lonely", "makes me sad and lonely",
                        "im low and lonely", "i am low and lonely", "making me low and lonely", "making me low and lonely", "makes me low and lonely", "makes me low and lonely",
                        "im sad and alone", "i am sad and alone", "making me sad and alone", "making me sad and alone", "makes me sad and alone", "makes me sad and alone",
                        "im low and alone", "i am low and alone", "making me low and alone", "making me low and alone", "makes me low and alone", "makes me low and alone",
                        "im isolated", "i am isolated", "making me isolated", "making me isolated", "makes me isolated", "makes me isolated",
                        "im sad and isolated", "i am sad and isolated", "making me sad and isolated", "making me sad and isolated", "makes me sad and isolated", "makes me sad and isolated"]
    nobodyUnderstandsMeArray = ["no one understands me", "no one understands how i feel", "nobody understands me", "nobody understands how i feel", "no one seems to understand me", "no one seems to understand how i feel",\
                         "nobody seems to understand me", "nobody seems to understand how i feel", "i feel misunderstood", "there is nobody who understands me", "there is no one who understands me"]
    imSickOfLockdownArray = ["im sick of lockdown", "im fed up of lockdown", "im sick to the back teeth of lockdown", "ive had enough of lockdown", "i have had enough of lockdown", "i cant cope with lockdown", "im bored of lockdown", "i am bored of lockdown"]
    iDontSleepArray = ["i dont sleep", "i have insomnia", "i suffer from insomnia", "im an insomniac", "insomnia is killing me", "i hardly ever get any sleep", "i struggle to sleep", "i cant sleep"]
    dontHaveAnyoneICanTalkToArray = ["don't have anyone i can talk to", "dont have anyone i can talk to","don't have anyone i can talk with", "dont have anyone i can talk with", \
                                    "i have no one to talk to", "i have nobody to talk to", "i have no one to talk with", "i have nobody to talk with", \
                                    "i've no one to talk to", "i've nobody to talk to", "i've no one to talk with", "i've nobody to talk with", \
                                    "ive no one to talk to", "ive nobody to talk to", "ive no one to talk with", "ive nobody to talk with", "i have no one to talk to",\
                                    "ive no one to talk to", "ive nobody to talk to", "ive no one to talk with", "ive nobody to talk with", "i have no one to talk to", \
                                    "i feel i have no one to talk to", "i feel i have no one to speak to", "i feel like i don't have anyone to talk to", "i feel like i don't have anyone to chat to"]
    iHateHowILookArray = ["i hate how i look", "i hate my looks", "i hate my appearance", "i hate the way i look",\
                        "i just hate how i look", "i just hate my looks", "i just hate my appearance", "i just hate the way i look",\
                        "i really hate how i look", "i really hate my looks", "i really hate my appearance", "i really hate the way i look",\
                        "i really just hate how i look", "i really just hate my looks", "i really just hate my appearance", "i really just hate the way i look",
                        "im ugly", "i am ugly", "i look horrible", "i look disgusting", "i look atrocious", "i feel insecure about my body", "i feel insecure about my appearance", \
                        "i hate my body", "i despise my body", "i am so humiliated that i look like this", "i feel so humiliated that i look like this"]
    loseWeightArray = ["i want to lose weight", "i don’t know how to lose weight", "i cant lose weight", "im fat", "ive been fat-shamed", "ive been fatshamed",\
                       "i have been fat-shamed", "i have been fatshamed", "has been fat-shaming me", "has been fatshaming me", "fat-shamed me", "fatshamed me"]
                        
    feelOverwhelmedArray = ["i feel overwhelmed", "im feeling overwhelmed", "i'm feeling overwhelmed", \
                            "i feel so overwhelmed", "im feeling so overwhelmed", "i'm feeling so overwhelmed",\
                            "i feel really overwhelmed", "im feeling really overwhelmed", "i'm feeling really overwhelmed", \
                            "i feel totally overwhelmed", "im feeling totally overwhelmed", "i'm feeling totally overwhelmed",\
                            "i feel utterly overwhelmed", "im feeling utterly overwhelmed", "i'm feeling utterly overwhelmed",\
                            "i just feel overwhelmed", "im just feeling overwhelmed", "i'm just feeling overwhelmed", \
                            "i just feel so overwhelmed", "im just feeling so overwhelmed", "i'm just feeling so overwhelmed",\
                            "i just feel really overwhelmed", "im just feeling really overwhelmed", "i'm just feeling really overwhelmed", \
                            "i just feel totally overwhelmed", "im just feeling totally overwhelmed", "i'm just feeling totally overwhelmed",\
                            "i just feel utterly overwhelmed", "im just feeling utterly overwhelmed", "i'm just feeling utterly overwhelmed",
                            "i am overwhelmed", "im overwhelmed"]
    aLotOnMyMindArray = ["i have a lot on my mind", "ive a lot on my mind", "ive got a lot on my mind", "i have got a lot on my mind"]
    feelingAwfulArray = ["i feel awful", "i'm feeling awful", "im feeling awful",\
                        "i feel so awful", "i'm feeling so awful", "im feeling so awful",\
                        "i feel really awful", "i'm feeling really awful", "im feeling really awful",\
                        "i just feel awful", "i'm just feeling awful", "im just feeling awful",\
                        "i just feel so awful", "i'm just feeling so awful", "im just feeling so awful",\
                        "i just feel really awful", "i'm just feeling really awful", "im just feeling really awful"]
    feelLikeCryingArray = ["i want to cry all the time", "am crying all the time", "feel like crying all the time", "im crying all the time"]                    
    imAFailureArray = ["im a failure", "i am a failure", "im a total failure", "i am a total failure", "im a total utter failure", "i am a total utter failure", "im an utter failure", "i am an utter failure",
                        "im just a failure", "i am just a failure", "im just a total failure", "i am just a total failure", "im just a total utter failure", "i am just a total utter failure", "im an utter failure", "i am an utter failure",
                        "im just a failure", "i really am just a failure", "im just a total failure", "i really am just a total failure", "im just a total utter failure", "i really am just a total utter failure", "im an utter failure", "i really am an utter failure",
                        "im a failure", "i really am a failure", "im a total failure", "i really am a total failure", "im a total utter failure", "i really am a total utter failure", "im an utter failure", "i really am an utter failure",
                        "im such a failure", "i am such a failure", "im such a total failure", "i am such a total failure", "im such a total utter failure", "i am such a total utter failure", "im such an utter failure", "i am such an utter failure",
                        "i feel like a failure", "i feel a failure", "i feel myself to be a failure",
                        "i feel like such a failure", "i feel such a failure", "i feel myself to be such a failure", "im not going to make it in life"]
    imALetdownArray = ["im a letdown", "i am a letdown", "im a total letdown", "i am a total letdown", "im a total utter letdown", "i am a total utter letdown", "im an utter letdown", "i am an utter letdown",
                        "im just a letdown", "i am just a letdown", "im just a total letdown", "i am just a total letdown", "im just a total utter letdown", "i am just a total utter letdown", "im an utter letdown", "i am an utter letdown",
                        "im just a letdown", "i really am just a letdown", "im just a total letdown", "i really am just a total letdown", "im just a total utter letdown", "i really am just a total utter letdown", "im an utter letdown", "i really am an utter letdown",
                        "im a letdown", "i really am a letdown", "im a total letdown", "i really am a total letdown", "im a total utter letdown", "i really am a total utter letdown", "im an utter letdown", "i really am an utter letdown",
                      "im a let down", "i am a let down", "im a total let down", "i am a total let down", "im a total utter let down", "i am a total utter let down", "im an utter let down", "i am an utter let down",
                        "im just a let down", "i am just a let down", "im just a total let down", "i am just a total let down", "im just a total utter let down", "i am just a total utter let down", "im an utter let down", "i am an utter let down",
                        "im just a let down", "i really am just a let down", "im just a total let down", "i really am just a total let down", "im just a total utter let down", "i really am just a total utter let down", "im an utter let down", "i really am an utter let down",
                        "im a let down", "i really am a let down", "im a total let down", "i really am a total let down", "im a total utter let down", "i really am a total utter let down", "im an utter let down", "i really am an utter let down",
                        "im such a letdown", "i am such a letdown", "im such a total letdown", "i am such a total letdown", "im such a total utter letdown", "i am such a total utter letdown", "im such an utter letdown", "i am such an utter letdown",
                        "i feel like a letdown", "i feel a letdown", "i feel myself to be a letdown",
                        "i feel like such a letdown", "i feel such a letdown", "i feel myself to be such a letdown"]
    letMyselfDownArray = ["let myself down", "let my self down", "let mysefl down", "let my sefl down"]
    hardLifeArray = ["ive had a hard life", "ive had a bad life", "ive had a hard and bad life", "i have had a hard life", "i have had a bad life", "i have had a hard and bad life"]
    iHaveRegretsArray = ["i have regrets", "i have many regrets", "my life is so full of regrets", "my life is full of regrets", "i am full of regret"]
    underAchievedArray = ["i have accomplished nothing", "i have achieved nothing", "i havent accomplished anything", "i havent achieved anything"]
    hurtsMyFeelingsArray = ["hurts my feelings", "continues to hurt my feelings"]    
    hurtsToKnowThatArray = ["it hurts to know that", "it pains me to know that", "it hurts knowing that", "i feel the pain of knowing that"]
    feelOutOfControlArray = ["i feel out of control", "i'm feeling out of control", "im feeling out of control",\
                            "i feel so out of control", "i'm feeling so out of control", "im feeling so out of control",\
                            "i feel really out of control", "i'm feeling really out of control", "im feeling really out of control",\
                            "i feel totally out of control", "i'm feeling totally out of control", "im feeling totally out of control",\
                            "i just feel out of control", "i'm just feeling out of control", "im just feeling out of control",\
                            "i just feel so out of control", "i'm just feeling so out of control", "im just feeling so out of control",\
                            "i just feel really out of control", "i'm just feeling really out of control", "im just feeling really out of control",\
                            "i just feel totally out of control", "i'm just feeling totally out of control", "im just feeling totally out of control"]
    feelLostArray = ["i feel lost", "i'm feeling lost", "im feeling lost", \
                    "i feel so lost", "i'm feeling so lost", "im feeling so lost",\
                    "i feel totally lost", "i'm feeling totally lost", "im feeling totally lost",\
                    "i feel utterly lost", "i'm feeling utterly lost", "im feeling utterly lost",\
                    "i feel really lost", "i'm feeling really lost", "im feeling really lost",\
                    "i feel very lost", "i'm feeling very lost", "im feeling very lost",\
                    "i just feel lost", "i'm just feeling lost", "im just feeling lost", \
                    "i just feel so lost", "i'm just feeling so lost", "im just feeling so lost",\
                    "i just feel totally lost", "i'm just feeling totally lost", "im just feeling totally lost",\
                    "i just feel utterly lost", "i'm just feeling utterly lost", "im just feeling utterly lost",\
                    "i just feel really lost", "i'm just feeling really lost", "im just feeling really lost",\
                    "i just feel very lost", "i'm just feeling very lost", "im just feeling very lost"]
    feelEmptyArray = ["i feel empty", "i feel empty", "i feel a sense of emptiness"]
    inABadPlaceArray = ["i am in a bad place", "i'm in a bad place", "im in a bad place",\
                        "i am in such a bad place", "i'm in such a bad place", "im in such a bad place",\
                        "i am at a bad place", "i'm at a bad place", "im at a bad place",\
                        "i am at such a bad place", "i'm at such a bad place", "im at such a bad place"]
    imTrappedArray = ["i am trapped", "i feel trapped", "im trapped"]
    nobodyCaresArray = ["no one cares about me", "noone cares about me", "no one cares for me"]
    noOneCaresAboutMeArray = ["no one cares about me", "noone cares about me", "no one cares for me", "noone cares for me", "nobody cares about me", "nobody cares for me"]
    feelingLowDownTerribleArray = ["i feel low", "i'm feeling low", "im feeling low", "i am feeling low",
                                "i feel down", "i'm feeling down", "im feeling down", "i am feeling down",
                                "i feel terrible", "i'm feeling terrible", "im feeling terrible", "i am feeling terrible",
                                "i feel horrible", "i'm feeling horrible", "im feeling horrible", "i am feeling horrible"]
    iWantThisFeelingToGoAwayArray = ["i want this feeling to go away", "i wish this feeling would go away", "i wish i didnt feel like this", "i dont want to feel like this"]
    iHateHowIFeelArray = ["hate how i feel","hate how im feeling", "hate my feelings"]
    imSadArray = ["i am sad", "i'm sad", "im sad", "i feel sad"
                "i am feeling sad", "i'm feeling sad", "im feeling sad"]
    imUpsetArray = ["im upset", "i'm upset", "im feeling upset", "i'm feeling upset", "i feel upset", "i feel upset",\
                    "im so upset", "i'm so upset", "im feeling so upset", "i'm feeling so upset", "i feel so upset", "i feel so upset",\
                    "im really upset", "i'm really upset", "im feeling really upset", "i'm feeling really upset", "i feel really upset", "i feel really upset"]
    hurtFeelingsArray = ["hurts my feelings", "hurt my feelings"]
    beingBulliedArray = ["im being bullied", "im being cyberbullied", "bullied me"]
    iFeelHelplessArray = ["I feel helpless", "im feeling helpless"]
    imAddictedArray = ["im addicted", "i'm addicted"]
    iHateCoronavirusArray = ["i hate coronavirus", "i hate the coronavirus", "i hate covid", "i hate covid19"]
    feelingRubbishArray = ["im feeling rubbish", "i'm feeling rubbish", "i feel rubbish", "i feel rubbish",\
                    "im feeling so rubbish", "i'm feeling so rubbish", "i feel so rubbish", "i feel so rubbish",\
                    "im feeling really rubbish", "i'm feeling really rubbish", "i feel really rubbish", "i feel really rubbish",\
                    "im just feeling rubbish", "i'm just feeling rubbish", "i just feel rubbish", "i just feel rubbish",\
                    "im just feeling so rubbish", "i'm just feeling so rubbish", "i just feel so rubbish", "i just feel so rubbish",\
                    "im just feeling really rubbish", "i'm just feeling really rubbish", "i just feel really rubbish", "i just feel really rubbish"\
                    "i don't feel right", "am not feeling right"]
    panicAttacksArray = ["i keep getting panic attacks", "i keep getting really bad panic attacks", "the panic attacks keep coming", \
                    "the panic attacks come back"]
    imAnxiousArray = ["im anxious", "i am anxious", "im feeling anxious", "i am feeling anxious", "i feel anxious"]
    iHaveAnxietyArray = ["i have anxiety", "i suffer from anxiety"]
    imWorriedArray = ["im worried", "i am worried", "i have worries", "making me worried", "makes me worried", "leaves me feeling worried", " i have so much to worry "]
    iFeelStuckArray = ["i feel stuck", "im feeling stuck"]
    imNotHappyArray = ["im not happy", "i'm not happy", "im just not happy", "i'm just not happy", "im really not happy", "i'm really not happy"]
    iFeelNumbArray = ["i dont feel anything right now. just numb", "i dont feel anything right now. just numb", "i feel numb",\
                    "i don't feel anything", "don't feel much", "just numb", "don't feel", "feel numb", "don't feel anything"]
    imNotSureWhereToTurnArray = ["im not sure where to turn", "i dont know where to turn"]
    abandonedMeArray = ["boyfriends abandoned me", "boyfriend has abandoned me", "girlfriends abandoned me", "girlfriend has abandoned me", "wifes abandoned me", "wife has abandoned me", "husband has abandoned me", "husbands abandoned me"]
    imStuckAtHomeArray = ["im stuck in my home", "im stuck in my house", "im stuck in my flat", "i am stuck in my home", "i am stuck in my house", "i am stuck in my flat", "im stuck in the home", "im stuck in the house", "im stuck in the flat", \
                          "i am stuck in the home", "i am stuck in the house", "i am stuck in the flat", "im stuck at my home", "im stuck at my house", "im stuck at my flat", "i am stuck at my home", "i am stuck at my house", "i am stuck at my flat", "im stuck at the home", "im stuck at the house",\
                          "im stuck at the flat", "i am stuck at the home", "i am stuck at the house", "i am stuck at the flat", "im stuck at home", "i cant leave my home", "i cant leave my house", "i cant leave my flat", "i cant leave the home", "i cant leave the house", "i cant leave the flat"]
    waitingToSeeIfPoliceAreGoingToChargeMeWithAnOffenceArray = ["waiting to see if police are going to charge me with an offence"]
    imHomelessArray = ["im homeless", "i am homeless", "ive been homeless", "i have been homeless"]
    iHaventSeenMyKidsArray = ["i havent seen my kids", "i havent seen the kids", "i havent seen my children", "i havent seen the children"]
    difficultDayArray = ["its been a tough day", "it's been a tough day", "i've had a tough day", "ive had a tough day", \
                        "its been a difficult day", "it's been a difficult day", "i've had a difficult day", "ive had a difficult day"]
    # stressingMeOutArray = ["i feel stressed", "it's stressing me out", "it's making me stressed", "it's making me feel stressed"]                    
    imPregnantArray = ["i am pregnant", "im pregnant"]
    imBeingTakenForGrantedArray = ["im being taken for granted", "i am being taken for granted", "i dont feel appreciated", "im not being appreciated", "doesn't appreciate me", "don't appreciate me"]
    itsStressingMeOutArray = ["its stressing me out", "its making me stressed", "its making me feel stressed", "i feel stressed", "im feeling stressed"]
    familyProblemsArray = ["i have family problems", "i'm having family problems", "im having family problems", "ive got family problems", \
                            "i have problems with my family", "i'm having problems with my family", "im having problems with my family", "ive got problems with my family",
                            "i have family troubles", "i'm having family troubles", "im having family troubles", "ive got family troubles", \
                            "i have troubles with my family", "i'm having troubles with my family", "im having troubles with my family", "ive got troubles with my family",
                            "i have family difficulties", "i'm having family difficulties", "im having family difficulties", "ive got family difficulties", "ive got difficulties with my family", \
                            "i have difficulties with my family", "i'm having difficulties with my family", "im having difficulties with my family", "ive got difficulties with my family", \
                            "i have family worries", "i'm having family worries", "im having family worries", "ive got family worries", "ive got worries with my family", \
                            "i have worries with my family", "i'm having worries with my family", "im having worries with my family", "ive got worries with my family"]
    gotDumpedArray = ["my ex broke up with me", "my ex dumped me", "my exboyfriend broke up with me", "my exboyfriend dumped me", "my boyfriend broke up with me",\
                        "my boyfriend dumped me", "my exgirlfriend broke up with me", "my exgirlfriend dumped me", "my girlfriend broke up with me", "my girlfriend dumped me", \
                        "my exhusband broke up with me", "my exhusband dumped me", "my husband broke up with me", "my husband dumped me", "my exwife broke up with me", "my exwife dumped me",\
                        "my wife broke up with me", "my wife dumped me"]
    BrokeUpWithPartnerArray = ["i broke up with my ex", "i broke up with my girlfriend", "i broke up with my boyfriend", "i broke up with my husband", \
                            "i broke up with my wife", "i broke up with my partner"]
    canYouHelpArray = ["can you help", "can you help", "can you help me", "help me please"]
    fallOutArray = ["and i have fallen out", "we have fallen out"]
    abuseArray = ["abuse other people", "abuse me", "abusing me"]
    heartBreakArray = ["i am going through heartbreak", "i am heartbroken", "i feel heartbroken"]
    iWantAFriendArray = ["i want a friend", "i need a friend", "i have no friends", "i don't have any friends", "i havent got any friends", "ive got no friends" "i don’t have friends"]
    iDontSeeManyPeopleArray = ["i dont see many people", "i dont see a lot of people"]
    helpArray = ["help", "help me", "i need help"]
    iDontKnowWhatToDoArray = ["i dont know what to do", "i dunno what to do", "i have no idea what to do",
                            "ive no idea what to do", "i hvaent a clue what to do", "i havent a clue what to do",
                            "i havent any idea what to do", "i dont have any idea what to do",
                            "im not sure what to do", "im not all that sure what to do", "i am not sure what to do", "im not at all sure what to do",
                            "what do you think i should do", "what do you think i shuld do", "what do u think i should do", "wat do you think i should do",
                            "what should i do", "what can i do", "what do i do"]
    whatToDoWithMyselfArray = ["i don't know what to do with myself"]
    iDontKnowWhatToSayArray = ["i dont know what to say", "i don't know what to say", "i dont know what else to say", "i don't know what else to say", "i dont know what more to say", "i don't know what more to say",
                                "i dont know what to tell you", "i don't know what to tell you", "i dont know what else to tell you", "i don't know what else to tell you", "i dont know what more to tell you", "i don't know what more to tell you",
                                "dont know what to say", "don't know what to say", "dont know what else to say", "don't know what else to say", "dont know what more to say", "don't know what more to say",
                                "dont know what to tell you", "don't know what to tell you", "dont know what else to tell you", "don't know what else to tell you", "dont know what more to tell you", "don't know what more to tell you",
                                "i dont know what to say now", "i don't know what to say now", "i dont know what else to say now", "i don't know what else to say now", "i dont know what more to say now", "i don't know what more to say now",
                                "dont know what to say now", "don't know what to say now", "dont know what else to say now", "don't know what else to say now", "dont know what more to say now", "don't know what more to say now",
                                "dunno what to say", "dunno what else to say", "dunno what more to say",
                                "i dont really know what to say", "i don't really know what to say", "i dont really know what else to say", "i don't really know what else to say", "i dont really know what more to say", "i don't really know what more to say",
                                "i dont really know what to tell you", "i don't really know what to tell you", "i dont really know what else to tell you", "i don't really know what else to tell you", "i dont really know what more to tell you", "i don't really know what more to tell you",
                                "dont really know what to say", "don't really know what to say", "dont really know what else to say", "don't really know what else to say", "dont really know what more to say", "don't really know what more to say",
                                "dont really know what to tell you", "don't really know what to tell you", "dont really know what else to tell you", "don't really know what else to tell you", "dont really know what more to tell you", "don't really know what more to tell you",
                                "i dont really know what to say now", "i don't really know what to say now", "i dont really know what else to say now", "i don't really know what else to say now", "i dont really know what more to say now", "i don't really know what more to say now",
                                "dont really know what to say now", "don't really know what to say now", "dont really know what else to say now", "don't really know what else to say now", "dont really know what more to say now", "don't really know what more to say now"]
    personalHygieneArray = ["my personal hygiene isn't the best", "my personal hygiene isn't great", "i haven't showered in days"]
    iSmellArray = ["i smell"]
    wantToBeHappyArray = ["i want to be happy again", "i wish i could be happy again"]
    helloArray = ["hello", "hi", "hey","hello!", "hi!", "hey!", "hello?", "hi?", "hey?"]
    iWantFreedomArray = ["i want freedom", "set me free", "let me be free"]
    whoCanITalkToArray = ["who can i talk to", "is there anyone i can talk to", "is there someone i can talk to"]
    whatDoYouThinkArray = ["what do you think", "what do u think"]
    # whoCanITalkToArray = ["who can i talk to", "is there anyone i can talk to "]
    howAreYouArray = ["how are you", "how r u", "how are u", "how are you doing", "how r u doing"]
    doYouGiveAdviceArray = ["do you give advice", "do you provide advice","do you offer advice"
                            "do you give any advice", "do you provide any advice","do you offer any advice",
                            "do you even give advice", "do you even provide advice", "do you even offer advice",
                            "do you even give any advice", "do you even provide any advice",  "do you even offer any advice",
                            "can you give me advice", "can you provide me advice", "can you offer me advice",
                            "can you give me any advice", "can you provide me any advice", "can you offer me any advice",
                            "can you give me some advice", "can you provide me some advice", "can you offer me some advice",
                            "have you any advice", "have you some advice", "have you advice"
                            "give me advice", "i need advice",
                            "dont you give advice", "you dont give advice",
                            "will you give me advice", "will you give advice", "can you not give advice", "can u not give advice",\
                             "i need some advice", "i need advice", "do you have tips", "do you give tips", "i wanted advice", "i just need some advice", "i just need advice"]
    dontKnowArray = ["i don't know", "i dont know", "i dunno", "idk"]
    whatDoYouThinkArray = ["what do you think", "what do u think"]
    imGoingToGoNowArray = ["im going to go now", "im going now"]
    yourNiceArray = ["youre nice", "you are nice"]
    areYouReadingArray = ["are you reading", "r u reading", "is this thing even paying attention", "are you paying attention", "are you listening", "is anyone there"]
    lettingMeGetMyThoughtsOutOfMyHeadArray = ["youre letting me get my thoughts out of my head", "are you letting me get my thoughts out of my head", "is this a place to vent", "this is a place to vent", "is this for me to let off steam", "this is for me to let off steam", "is this for me to get my thoughts out", "This is a forum for someone to speak", "This app is a forum for someone to speak", "This bot is a forum for someone to speak",  "This is a space for someone to speak", "This app is a space for someone to speak", "This bot is a space for someone to speak", ]
    # you only give default/automatic replies
    # you are useless / fuck off
    idkWhatElseToSayToYouArray = ["Idk what else to say to you", "idk what else to tell you", "idk what more to say to you", "idk what more to tell you"]
    thankYouArray = ["thank you", "thanks"]
    stopSynonymsArray = ["that's it", "thats it", "finish", "end", "nothing more to say", "no more to say", "bot stop", "bye","goodbye",\
                        "done", "i'm done", "im done", "i think im done", "im done speaking", "i think im done speaking",
                        "i have nothing more to say", "i have nothing else to say", "ive got nothing more to say", "ive got nothing else to say",
                        "i think i have nothing more to say", "i think i have nothing else to say", "i think ive got nothing more to say", "i think ive got nothing else to say",
                        "i dont want to talk any more" ]
    areYouABotArray = ["are you a bot", "is this a bot", "what is this a bot"]
    willYouConverseWithMeArray = ["are you gonna have a conversation with me or tell me to keep talking?", \
                        "are you gonna have a conversation with me", "are you going to have a conversation with me", \
                        "are you going to tell me to keep talking", "are you gonna tell me to keep talking"]
    thisBotIsBadArray_loose = ["this bot is bad", "this bot is awful", "this bot is terrible", "this bot is atrocious", "this bot is shit", "this bot is crap"
                        "you are a bad bot", "you are an awful bot", "you are a terrible bot", "you are an atrocious bot", "you are a shit bot", "you are a crap bot",
                        "you are such a bad bot", "you are such an awful bot", "you are such a terrible bot", "you are such an atrocious bot", "you are such a shit bot", "you are such a crap bot",
                        "this is a bad bot", "this is an awful bot", "this is a terrible bot", "this is an atrocious bot", "this is a shit bot", "this is a crap bot",
                        "this is such a bad bot", "this is such an awful bot", "this is such a terrible bot", "this is such an atrocious bot", "this is such a shit bot", "this is such a crap bot",
                        "this bot is not helping", "this bot isnt helping", "this bot is no help", "this bot is no use", "this bot aint helping",
                        "i need to talk to a human", "i need to talk to a real person", "i need to talk to a real human",
                        "i need to speak to a human", "i need to speak to a real person", "i need to speak to a real human",
                         "are you even gonna actually have a conversation with me or just tell me to keep talking?", "is this all you do"]
    thisBotIsBadArray_tight = ["you are bad", "you are awful", "you are terrible", "you are atrocious", "you are shit", "you are crap",
                        "this isnt helping", "this is not helping", "this aint helping",
                        "youre not helping", "your not helping", "you are not helping", "you arent helping", "you aint helping", "your no help", "youre no help", "your not a help", "youre not a help",
                        "this is useless", "this is worthless", "this is crap", "this is rubbish", "this is trash", "this is annoying", "this is pointless",
                        "you are useless", "you are worthless", "you are crap", "you are rubbish", "you are trash", "you are annoying", "you are pointless",
                        "what a waste of time", "what a pointless waste of time", "what a useless waste of time", "bye, you're useless", "bye, your useless", "bye, you are useless"]
    


    # these variables are to keep track of whether a response has already been given (to avoid repeating it).
    # Just asserting here that they are global
    global iWantToKillMyselfResponseAlreadyUsed
    global imGoingToKillMyselfResponseAlreadyUsed
    global iWillDieTodayResponseAlreadyUsed
    global iWantToDieResponseAlreadyUsed
    global imFeelingSuicidalResponseAlreadyUsed
    #global feelingQuiteSuicidalResponseAlreadyUsed : this varirable isn't being used
    global suicidalThoughtsResponseAlreadyUsed
    global contemplatedSuicideButResponseAlreadyUsed
    global iWishIWasDeadResponseAlreadyUsed
    global betterOffDeadResponseAlreadyUsed
    global iDontWantToLiveResponseAlreadyUsed
    global sleepForeverResponseAlreadyUsed
    global shouldIEndItResponseAlreadyUsed
    global shouldIKillMyselfResponseAlreadyUsed
    global suicideIsOnlyOptionResponseAlreadyUsed
    global feelLikeEndingItResponseAlreadyUsed
    global iWasRapedResponseAlreadyUsed
    global cryingResponseAlreadyUsed
    global iWantToCryResponseAlreadyUsed
    global nothingToLiveForResponseAlreadyUsed
    global singleWordDepressionResponseAlreadyUsed
    global feelingDepressedResponseAlreadyUsed
    global treatDepressionResponseAlreadyUsed
    global iHaveDepressionResponseAlreadyUsed
    global iMightHaveDepressionResponseAlreadyUsed
    global iHaveNoWayOutResponseAlreadyUsed
    global hadEnoughOfLifeResponseAlreadyUsed
    global iWantToGiveUpOnLifeResponseAlreadyUsed
    global nothingToLookForwardToResponseAlreadyUsed
    global imUselessResponseAlreadyUsed
    global imWorthlessResponseAlreadyUsed
    global imNotLovedResponseAlreadyUsed
    global imNotSpecialToAnyoneResponseAlreadyUsed
    global iWantSomeoneToLoveMeResponseAlreadyUsed
    global feelingLonelyResponseAlreadyUsed
    global nobodyUnderstandsMeResponseAlreadyUsed
    global imSickOfLockdownResponseAlreadyUsed
    global iDontSleepResponseAlreadyUsed
    global dontHaveAnyoneICanTalkToResponseAlreadyUsed
    global iHateHowILookResponseAlreadyUsed
    global loseWeightResponseAlreadyUsed
    global feelOverwhelmedResponseAlreadyUsed
    global aLotOnMyMindResponseAlreadyUsed
    global feelingAwfulResponseAlreadyUsed
    global feelLikeCryingResponseAlreadyUsed
    global imAFailureResponseAlreadyUsed
    global imALetdownResponseAlreadyUsed
    global letMyselfDownResponseAlreadyUsed
    global hardLifeResponseAlreadyUsed
    global iHaveRegretsResponseAlreadyUsed
    global underAchievedResponseAlreadyUsed
    global hurtsMyFeelingsResponseAlreadyUsed
    global hurtsToKnowThatResponseAlreadyUsed
    global feelOutOfControlResponseAlreadyUsed
    global feelLostResponseAlreadyUsed
    global feelEmptyResponseAlreadyUsed
    global inABadPlaceResponseAlreadyUsed
    global imTrappedResponseAlreadyUsed
    global nobodyCaresResponseAlreadyUsed
    global noOneCaresAboutMeResponseAlreadyUsed
    global deserveResponseAlreadyUsed
    global iHateHowIFeelResponseAlreadyUsed
    global imSadResponseAlreadyUsed
    global feelingLowDownTerribleResponseAlreadyUsed
    global iWantThisFeelingToGoAwayResponseAlreadyUsed
    global imUpsetResponseAlreadyUsed
    global hurtFeelingsResponseAlreadyUsed
    global beingBulliedResponseAlreadyUsed
    global iFeelHelplessResponseAlreadyUsed
    global imAddictedResponseAlreadyUsed
    global iHateCoronavirusResponseAlreadyUsed
    global feelingRubbishResponseAlreadyUsed
    global panicAttacksResponseAlreadyUsed
    global iHaveAnxietyResponseAlreadyUsed
    global imAnxiousResponseAlreadyUsed
    global initial_imWorriedResponseAlreadyUsed
    global second_imWorriedResponseAlreadyUsed
    global iDontKnowWhatToDoResponseAlreadyUsed
    global whatToDoWithMyselfResponseAlreadyUsed
    global initial_iDontKnowWhatToSayResponseAlreadyUsed
    global second_iDontKnowWhatToSayResponseAlreadyUsed
    global personalHygieneResponseAlreadyUsed
    global iSmellResponseAlreadyUsed
    global wantToBeHappyResponseAlreadyUsed
    global imNotHappyResponseAlreadyUsed
    global iFeelNumbResponseAlreadyUsed
    global iFeelStuckResponseAlreadyUsed
    global imNotHappyResponseAlreadyUsed
    global imNotSureWhereToTurnResponseAlreadyUsed
    global iHateMyselfResponseAlreadyUsed
    global abandonedMeResponseAlreadyUsed
    global imStuckAtHomeResponseAlreadyUsed
    global waitingToSeeIfPoliceAreGoingToChargeMeWithAnOffenceResponseAlreadyUsed
    global imHomelessResponseAlreadyUsed
    global iHaventSeenMyKidsResponseAlreadyUsed
    global difficultDayResponseAlreadyUsed
    # global StressingMeOutResponseAlreadyUsed
    # global familyProblemsResponseAlreadyUsed
    global gotDumpedResponseAlreadyUsed
    global brokeUpWithPartnerResponseAlreadyUsed
    global canYouHelpResponseAlreadyUsed
    global feelLostResponseAlreadyUsed
    global iWantFreedomResponseAlreadyUsed
    global whoCanITalkToResponseAlreadyUsed
    global howAreYouResponseAlreadyUsed
    global whatDoYouThinkResponseAlreadyUsed
    global imPregnantResponseAlreadyUsed
    global imBeingTakenForGrantedResponseAlreadyUsed
    global itsStressingMeOutResponseAlreadyUsed
    global familyProblemsResponseAlreadyUsed
    global fallOutResponseAlreadyUsed
    global abuseResponseAlreadyUsed
    global heartBreakResponseAlreadyUsed
    global iWantAFriendResponseAlreadyUsed
    global iDontSeeManyPeopleResponseAlreadyUsed
    global feelLostResponseAlreadyUsed
    global helpResponseAlreadyUsed
    # global iWantFreedomResponseAlreadyUsed
    # global whoCanITalkToResponseAlreadyUsed
    global howAreYouResponseAlreadyUsed
    global doYouGiveAdviceResponseAlreadyUsed
    global dontKnowResponseAlreadyUsed
    global whatDoYouThinkResponseAlreadyUsed
    global imGoingToGoNowResponseAlreadyUsed
    global areYouReadingResponseAlreadyUsed
    global lettingMeGetMyThoughtsOutOfMyHeadResponseAlreadyUsed
    global idkWhatElseToSayToYouResponseAlreadyUsed
    global thankYouResponseAlreadyUsed
    global shortResponseAlreadyUsed
    global areYouABotResponseAlreadyUsed
    global willYouConverseWithMeResponseAlreadyUsed
    global thisBotIsBadResponseAlreadyUsed


# declaring some variables which track whether a message says certain things
    msgSaysIWantToKillMyself = False
    msgSaysImGoingToKillMyself = False
    msgSaysIWillDieToday = False
    msgSaysIWantToDie = False
    msgSaysImFeelingSuicidal = False
    msgSaysImFeelingQuiteSuicidal = False
    msgSaysIveBeenFeelingSuicidal = False
    msgSaysSuicidalThoughts = False
    msgSaysContemplatedSuicideBut = False
    msgSaysIWishIWasDead = False
    msgSaysBetterOffDead = False
    msgSaysIDontWantToLive = False
    msgSaysSleepForever = False
    msgSaysShouldIEndIt = False
    msgSaysShouldIKillMyself = False
    msgSaysSuicideIsOnlyOption = False
    msgSaysFeelLikeEndingIt = False
    msgSaysIWasRaped = False
    msgSaysImCrying = False
    msgSaysIWantToCry = False
    msgSaysNothingToLiveFor = False
    msgSaysSingleWordDepression = False
    msgSaysFeelingDepressed = False
    msgSaysTreatDepression = False
    msgSaysIHaveDepression = False
    msgSaysIMightHaveDepression = False
    msgSaysIHaveNoWayOut = False
    msgSaysHadEnoughOfLife = False
    msgSaysIWantToGiveUpOnLife = False
    msgSaysNothingToLookForwardTo = False
    msgSaysImUseless = False
    msgSaysImWorthless = False
    msgSaysImNotLoved = False
    msgSaysImNotSpecialToAnyone = False
    msgSaysIWantSomeoneToLoveMe = False
    msgSaysFeelingLonely = False
    msgSaysNobodyUnderstandsMe = False
    msgSaysImSickOfLockdown = False
    msgSaysIDontSleep = False
    msgSaysDontHaveAnyoneICanTalkTo = False
    msgSaysIHateHowILook = False
    msgSaysLoseWeight = False
    msgSaysFeelOverwhelmed = False
    msgSaysALotOnMyMind = False
    msgSaysFeelingAwful = False
    msgSaysFeelLikeCrying = False
    msgSaysImAFailure = False
    msgSaysImALetdown = False
    msgSaysLetMyselfDown = False
    msgSaysHardLife = False
    msgSaysIHaveRegrets = False
    msgSaysUnderAchieved = False
    msgSaysHurtsMyFeelings = False
    msgSaysHurtsToKnowThat = False
    msgSaysFeelOutOfControl = False
    msgSaysFeelLost = False
    msgSaysFeelEmpty = False
    msgSaysInABadPlace = False
    msgSaysImTrapped = False
    msgSaysNobodyCares = False
    msgSaysNoOneCaresAboutMe = False
    msgSaysDeserve = False
    msgSaysIHateHowIFeel = False
    msgSaysImSad = False
    msgSaysFeelingLowDownTerrible = False
    msgSaysIWantThisFeelingToGoAway = False
    msgSaysImUpset = False
    msgSaysHurtFeelings = False
    msgSaysBeingBullied = False
    msgSaysIFeelHelpless = False
    msgSaysImAddicted = False
    msgSaysIHateCoronavirus = False
    msgSaysFeelingRubbish = False
    msgSaysPanicAttacks = False
    msgSaysIHaveAnxiety = False # code using this is commented out currently
    msgSaysImAnxious = False # code using this is commented out currently
    msgSaysImWorried = False
    msgSaysIDontKnowWhatToDo = False
    msgSaysWhatToDoWithMyself = False 
    msgSaysIDontKnowWhatToSay = False
    msgSaysPersonalHygiene = False
    msgSaysISmell = False
    msgSaysWantToBeHappy = False
    msgSaysImNotHappy = False
    msgSaysIFeelNumb = False
    msgSaysIFeelStuck = False
    msgSaysImNotHappy = False
    msgSaysImNotSureWhereToTurn = False
    msgSaysIHateMyself = False
    msgSaysAbandonedMe = False
    msgSaysImStuckAtHome = False
    msgSaysWaitingToSeeIfPoliceAreGoingToChargeMeWithAnOffence = False
    msgSaysImHomeless = False
    msgSaysIHaventSeenMyKids = False
    msgSaysDifficultDay = False
    # msgSaysStressingMeOut = False
    # msgSaysFamilyProblems = False
    msgSaysGotDumped = False
    msgSaysBrokeUpWithPartner = False
    msgSaysCanYouHelp = False
    msgSaysFeelLost = False
    msgSaysIWantFreedom = False
    msgSaysWhoCanITalkTo = False
    msgSaysHowAreYou = False
    msgSaysWhatDoYouThink = False
    msgSaysImPregnant = False
    msgSaysImBeingTakenForGranted = False
    msgSaysItsStressingMeOut = False
    msgSaysFamilyProblems = False
    msgSaysFallenOut = False
    msgSaysAbuse = False
    msgSaysHeartBreak = False
    msgSaysIWantAFriend = False
    msgSaysIDontSeeManyPeople = False
    msgSaysFeelLost = False
    msgSaysHelp = False
    # msgSaysFreedom = False
    # msgSaysWhoCanITalkTo = False
    msgSaysHowAreYou = False
    msgSaysWhatDoYouThink = False
    msgSaysDoYouGiveAdvice = False
    msgSaysDontKnow = False
    msgSaysImGoingToGoNow = False
    msgSaysYourNice = False
    msgSaysAreYouReading = False
    msgSaysLettingMeGetMyThoughtsOutOfMyHead = False
    msgSaysIdkWhatElseToSayToYou = False
    msgSaysThankYou = False
    msgSaysAreYouABot = False
    msgSaysWillYouConverseWithMe = False
    msgSaysThisBotIsBad = False

    negatedString = ""


    def cleanText(message):
        # can always simplify this function to something like the following which should do the same thing
        # cleanedMessage = ["".join(list(filter(str.isalpha, i))) for i in message.split() if i not in extraneousWordsArray]
        # cleanedMessage = ' '.join(cleanedMessage)
        # Being picky, do note that this function has a space at the end of the last word
        """
        This function takes a string (e.g. the user's message) and cleans it to make it suitable for analysing.
        It does this by
        1. clean the string so that it only contains alphabetic characters and spaces (everything else is deleted)
        2. remove extraneous words (this results in a list)
        3. turn list back into string
        Cleaning the message makes the system more robust, because we've seen instances of triggers not getting recognised...
        ... we speculate that different treatments of the apostrophe character might be the reason
        """

        extraneousWordsArray = ["still", "just", "so", "very", "totally", "utterly", "really", "completely", \
        "literally", "actually", "even", "some", "always", "fucking", "fuckin", "technically", "increasingly"]
        # I wanted to include "such a" in the extraneousWordsArray, but the current method does'nt work for that...
        #... because the current method "splits" the string into a list of separate words

        print("DEBUG: at start of clean text function, message = "+ message)

        # Step 1: clean the string so that it only contains alphabetic characters and spaces (everything else is deleted)
        messageCleanedOfCharacters = ""
        for char in message:
            if (char.isalpha() or char == " ") and char != "â": # have explicitly decided to remove â (a circumflex) here, becuase it seems like in some circumtances (maybe when the user has a mac?) the apostrophe is rendered as 'â€™'
                messageCleanedOfCharacters = messageCleanedOfCharacters+char

        print("DEBUG: in clean text function, messageCleanedOfCharacters = "+ messageCleanedOfCharacters)

        # Step 2: remove extraneous words
        message_list = messageCleanedOfCharacters.split()
        # for word in message_list:
        #     if word in extraneousWordsArray:
        #         del word
        # for i in range(0,len(message_list)):
        #     print("DEWBUG: i = "+str(i)+" and message_list[i] = "+ message_list[i])
        #     if message_list[i] in extraneousWordsArray:
        #         del message_list[i]

        loopEnd = len(message_list)
        i = 0
        while i < loopEnd:
            print("DEWBUG: i = "+str(i)+" and message_list[i] = "+ message_list[i])
            if message_list[i] in extraneousWordsArray:
                del message_list[i]
                loopEnd = loopEnd - 1
                i = i - 1
            i = i + 1

        # Step 3: reconstruct string
        cleanedMessage = ""
        for word in message_list:
            cleanedMessage = cleanedMessage + word + " "

        print("DEBUG: at end of clean text function, cleanedMessage = "+ cleanedMessage)


        return cleanedMessage


    print("Prior to cleaning, the message is "+message)
    cleanedMessage = ""
    cleanedMessage = cleanText(message)
    print("After cleaning, we have claenedmessage = "+cleanedMessage)


    # The below cleaning method isn't be used any more
    # for char in message:
    #     if char.isalpha():
    #         cleanedMessage = cleanedMessage+char


    leadStringArray = ["i ", "i am ", "im ", "i feel ", "i am feeling ", "im feeling ", "i'm "]

    def CheckUserMessage(synonymsArray):
        # work out if anything from the synonymsArray is in the user's message
        for string in synonymsArray:                      
            if string.lower() in cleanedMessage.lower():                          
                return True

                 # and if the string does have "it's not that" before it...
                for negatingString in itsNotThatArray:
                    negatedString = negatingString.lower()+string
                    if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""): 
                        return False
            
            # ... then set this flag to false
            if synonymsArray not in (imUselessArray, imWorthlessArray):                             
                for leadString in leadStringArray:
                    if string.startswith(leadString.lower()):
                        shortenedString = string.replace(leadString,"")
                        if cleanedMessage.lower().replace(" ","").startswith(shortenedString.replace(" ","")):
                            return True

    msgSaysIWantToKillMyself = CheckUserMessage(iWantToKillMyselfArray)

    msgSaysImGoingToKillMyself = CheckUserMessage(imGoingToKillMyselfArray)

    msgSaysIWillDieToday = CheckUserMessage(iWillDieTodayArray)

    msgSaysIWantToDie = CheckUserMessage(iWantToDieArray)

    msgSaysImFeelingSuicidal = CheckUserMessage(imFeelingSuicidalArray)

    msgSaysIveBeenFeelingSuicidal = CheckUserMessage(iveBeenFeelingSuicidalArray)

    msgSaysImFeelingQuiteSuicidal = CheckUserMessage(imFeelingQuiteSuicidalArray)

    msgSaysSuicidalThoughts = CheckUserMessage(suicidalThoughtsArray)

    msgSaysContemplatedSuicideBut = CheckUserMessage(contemplatedSuicideButArray)

    msgSaysIWishIWasDead = CheckUserMessage(iWishIWasDeadArray)

    msgSaysBetterOffDead = CheckUserMessage(betterOffDeadArray)

    msgSaysIDontWantToLive = CheckUserMessage(iDontWantToLiveArray)

    msgSaysSleepForever = CheckUserMessage(sleepForeverArray)
    for string in shouldIEndItArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):
            msgSaysShouldIEndIt = True

    msgSaysShouldIKillMyself = CheckUserMessage(shouldIKillMyselfArray)

    msgSaysSuicideIsOnlyOption = CheckUserMessage(suicideIsOnlyOptionArray)

    msgSaysFeelLikeEndingIt = CheckUserMessage(feelLikeEndingItArray)

    msgSaysIWasRaped = CheckUserMessage(iWasRapedArray)

    msgSaysNothingToLiveFor = CheckUserMessage(nothingToLiveForArray)

    msgSaysImCrying = CheckUserMessage(imCryingArray)

    msgSaysIWantToCry = CheckUserMessage(iWantToCryArray)

    msgSaysFeelingDepressed = CheckUserMessage(feelingDepressedArray)

    msgSaysTreatDepression = CheckUserMessage(treatDepressionArray)

    msgSaysFeelingLonely = CheckUserMessage(feelingLonelyArray)

    msgSaysNobodyUnderstandsMe = CheckUserMessage(nobodyUnderstandsMeArray)
    msgSaysImSickOfLockdown = CheckUserMessage(imSickOfLockdownArray)

    msgSaysIDontSleep = CheckUserMessage(iDontSleepArray)

    msgSaysIHateMyself = CheckUserMessage(iHateMyselfArray)

    msgSaysIHaveDepression = CheckUserMessage(iHaveDepressionArray)

    msgSaysIMightHaveDepression = CheckUserMessage(iMightHaveDepressionArray)

    msgSaysIHaveNoWayOut = CheckUserMessage(iHaveNoWayOutArray)

    msgSaysHadEnoughOfLife = CheckUserMessage(hadEnoughOfLifeArray)

    msgSaysIWantToGiveUpOnLife = CheckUserMessage(iWantToGiveUpOnLifeArray)

    msgSaysNothingToLookForwardTo = CheckUserMessage(nothingToLookForwardToArray)

    msgSaysImUseless = CheckUserMessage(imUselessArray)

    msgSaysImWorthless = CheckUserMessage(imWorthlessArray)

    msgSaysImNotLoved = CheckUserMessage(imNotLovedArray)

    msgSaysImNotSpecialToAnyone = CheckUserMessage(imNotSpecialToAnyoneArray)

    msgSaysIWantSomeoneToLoveMe = CheckUserMessage(iWantSomeoneToLoveMeArray)

    msgSaysDontHaveAnyoneICanTalkTo = CheckUserMessage(dontHaveAnyoneICanTalkToArray)

    msgSaysIHateHowILook = CheckUserMessage(iHateHowILookArray)

    msgSaysLoseWeight = CheckUserMessage(loseWeightArray)

    msgSaysFeelOverwhelmed = CheckUserMessage(feelOverwhelmedArray)

    msgSaysALotOnMyMind = CheckUserMessage(aLotOnMyMindArray)

    msgSaysFeelingAwful = CheckUserMessage(feelingAwfulArray)

    msgSaysFeelLikeCrying = CheckUserMessage(feelLikeCryingArray)

    msgSaysImAFailure = CheckUserMessage(imAFailureArray)        
   
    msgSaysFeelOutOfControl = CheckUserMessage(feelOutOfControlArray)

    msgSaysFeelLost = CheckUserMessage(feelLostArray)

    msgSaysFeelEmpty = CheckUserMessage(feelEmptyArray)

    msgSaysInABadPlace = CheckUserMessage(inABadPlaceArray)

    msgSaysImTrapped = CheckUserMessage(imTrappedArray)

    msgSaysNobodyCares = CheckUserMessage(nobodyCaresArray)
    for string in noOneCaresAboutMeArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):
            msgSaysNoOneCaresAboutMe = True

    msgSaysIHateHowIFeel = CheckUserMessage(iHateHowIFeelArray)

    msgSaysImSad = CheckUserMessage(imSadArray)

    msgSaysFeelingLowDownTerrible = CheckUserMessage(feelingLowDownTerribleArray)

    msgSaysIWantThisFeelingToGoAway = CheckUserMessage(iWantThisFeelingToGoAwayArray)

    msgSaysImUpset = CheckUserMessage(imUpsetArray)

    msgSaysHurtFeelings = CheckUserMessage(hurtFeelingsArray)

    msgSaysBeingBullied = CheckUserMessage(beingBulliedArray)
    msgSaysIFeelHelpless = CheckUserMessage(iFeelHelplessArray)

    msgSaysImAddicted = CheckUserMessage(imAddictedArray)

    msgSaysIHateCoronavirus = CheckUserMessage(iHateCoronavirusArray)

    msgSaysFeelingRubbish = CheckUserMessage(feelingRubbishArray)

    msgSaysPanicAttacks = CheckUserMessage(panicAttacksArray)

    msgSaysImAnxious = CheckUserMessage(imAnxiousArray)

    msgSaysIHaveAnxiety = CheckUserMessage(iHaveAnxietyArray)

    msgSaysImWorried = CheckUserMessage(imWorriedArray)

    msgSaysIDontKnowWhatToDo = CheckUserMessage(iDontKnowWhatToDoArray)

    msgSaysWhatToDoWithMyself = CheckUserMessage(whatToDoWithMyselfArray)

    msgSaysIDontKnowWhatToSay = CheckUserMessage(iDontKnowWhatToSayArray)

    msgSaysPersonalHygiene = CheckUserMessage(personalHygieneArray)

    msgSaysISmell = CheckUserMessage(iSmellArray)

    msgSaysWantToBeHappy = CheckUserMessage(wantToBeHappyArray)

    msgSaysImNotHappy = CheckUserMessage(imNotHappyArray)

    msgSaysIFeelNumb = CheckUserMessage(iFeelNumbArray)

    # msgSaysStressingMeOut = CheckUserMessage(stressingMeOutArray)

    # msgSaysFamilyProblems = CheckUserMessage(familyProblemsArray)

    msgSaysGotDumped = CheckUserMessage(gotDumpedArray)

    msgSaysBrokeUpWithPartner = CheckUserMessage(BrokeUpWithPartnerArray)

    msgSaysCanYouHelp = CheckUserMessage(canYouHelpArray)


    
    msgSaysIFeelStuck = CheckUserMessage(iFeelStuckArray)

    msgSaysImNotHappy = CheckUserMessage(imNotHappyArray)

    msgSaysImNotSureWhereToTurn = CheckUserMessage(imNotSureWhereToTurnArray)

        ## "Abandoned Me" is treated slightly different because it doesn't have a first person pronoun at the start, so the negating string is done differently
    for string in abandonedMeArray:             # work out if anything from the abandonedMeArray is in the user's cleanedMessage
        if string.lower() in cleanedMessage.lower():                          # if cleanedMessage contains "abandonedMe" or similar
            msgSaysAbandonedMe = True
            for negatingString in itsNotThatArray:
                negatedStringArray = [negatingString.lower()+string, negatingString.lower()+"i"+string, negatingString.lower()+"ive"+string, negatingString.lower()+"i've"+string] # including "i've" doesn't make sense any more now that we're using cleanedMessage, which takes the punctuation out anyway
                for negatedString in negatedStringArray:
                    if negatedString.lower() in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it, or "it's not that i" before it, or ...
                        msgSaysAbandonedMe = False                                     # ... then set this flag to false
        for leadString in leadStringArray:
            if string.startswith(leadString.lower()):
                shortenedString = string.replace(leadString,"")
                if cleanedMessage.lower().replace(" ","").startswith(shortenedString.replace(" ","")):
                    msgSaysAbandonedMe = True

    msgSaysImStuckAtHome = CheckUserMessage(imStuckAtHomeArray)

    for string in waitingToSeeIfPoliceAreGoingToChargeMeWithAnOffenceArray:
        if string.lower().replace(" ","") == cleanedMessage.lower().replace(" ",""):
            msgSaysWaitingToSeeIfPoliceAreGoingToChargeMeWithAnOffence = True

    msgSaysImHomeless = CheckUserMessage(imHomelessArray)

    msgSaysIHaventSeenMyKids = CheckUserMessage(iHaventSeenMyKidsArray)

    msgSaysImBeingTakenForGranted = CheckUserMessage(imBeingTakenForGrantedArray)

    # for string in itsStressingMeOutArray:
    #     if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):
    #         msgSaysItsStressingMeOut = True

    msgSaysItsStressingMeOut = CheckUserMessage(itsStressingMeOutArray)
    
    msgSaysFamilyProblems = CheckUserMessage(familyProblemsArray)

    for string in fallOutArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):
            msgSaysFallenOut = True

    for string in abuseArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):
            msgSaysAbuse = True

    msgSaysHeartBreak = CheckUserMessage(heartBreakArray)

    for string in imPregnantArray:
        if string.lower().replace(" ","") == cleanedMessage.lower().replace(" ",""):
            msgSaysImPregnant = True

    msgSaysIWantAFriend = CheckUserMessage(iWantAFriendArray)

    msgSaysIDontSeeManyPeople = CheckUserMessage(iDontSeeManyPeopleArray)

    # Is this one missing the 'for leadString...' on purpose or by accident?

    # for string in imAFailureArray:             # work out if anything from the ImAFailureArray is in the user's cleanedMessage
    #     if string in cleanedMessage.lower():                          # if cleanedMessage contains "ImAFailure" or similar
    #         msgSaysImAFailure = True
    #         for negatingString in itsNotThatArray:
    #             negatedString = negatingString+string
    #             if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
    #                 msgSaysImAFailure = False                                     # ... then set this flag to false
    #     ## the code which detects whether the message starts with a lead string like "i am" and sees whether the user has omitted it is not being applied here


    for string in imALetdownArray:             # work out if anything from the ImALetdownArray is in the user's cleanedMessage
        if string.lower() in cleanedMessage.lower():                          # if cleanedMessage contains "ImALetdown" or similar
            msgSaysImALetdown = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString.lower()+string
                if negatedString.replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysImALetdown = False                                     # ... then set this flag to false
        for leadString in leadStringArray:
            if string.lower().startswith(leadString.lower()):
                shortenedString = string.lower().replace(leadString,"")
                if cleanedMessage.lower().replace(" ","").startswith(shortenedString.replace(" ","")):
                    msgSaysImALetdown = True
    ## NOTE:  letMyselfDown is treated slightly differently. All the other strings start with I (i.e. the first person pronoun)
    ## "Let myself down" doesn't need to because it already contains a reflexive first person pronoun
    ## But this means that the preceding "it's not that" check needs to be more sophisticated.
    
    ## "Let myself down" is treated slightly different because it doesn't have a first person pronoun at the start, so the negating string is done differently
    for string in letMyselfDownArray:             # work out if anything from the letMyselfDownArray is in the user's cleanedMessage
        if string.lower() in cleanedMessage.lower():                          # if cleanedMessage contains "letMyselfDown" or similar
            msgSaysLetMyselfDown = True
            for negatingString in itsNotThatArray:
                negatedStringArray = [negatingString+string, negatingString+"i"+string, negatingString+"ive"+string, negatingString+"i've"+string] # including "i've" doesn't make sense any more now that we're using cleanedMessage, which takes the punctuation out anyway
                for negatedString in negatedStringArray:
                    if negatedString.lower() in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it, or "it's not that i" before it, or ...
                        msgSaysLetMyselfDown = False                                     # ... then set this flag to false
        for leadString in leadStringArray:
            if string.startswith(leadString.lower()):
                shortenedString = string.replace(leadString.lower(),"")
                if cleanedMessage.lower().replace(" ","").startswith(shortenedString.replace(" ","")):
                    msgSaysLetMyselfDown = True

    msgSaysHardLife = CheckUserMessage(hardLifeArray)

    msgSaysIHaveRegrets = CheckUserMessage(iHaveRegretsArray)

    msgSaysUnderAchieved = CheckUserMessage(underAchievedArray)

    msgSaysIWantFreedom = CheckUserMessage(iWantFreedomArray)

    msgSaysWhoCanITalkTo = CheckUserMessage(whoCanITalkToArray)

    msgSaysHowAreYou = CheckUserMessage(howAreYouArray)

    msgSaysWhatDoYouThink = CheckUserMessage(whatDoYouThinkArray)
    msgSaysHurtsToKnowThat = CheckUserMessage(hurtsToKnowThatArray)

    msgSaysHurtsMyFeelings = CheckUserMessage(hurtsMyFeelingsArray)

    for string in helpArray:
        if string.lower().replace(" ","") == cleanedMessage.lower().replace(" ",""):
            msgSaysHelp = True

    # for string in iWantFreedomArray:
    #     if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):
    #         msgSaysFreedom = True

    # for string in whoCanITalkToArray:
    #     if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):
    #         msgSaysWhoCanITalkTo = True

    for string in howAreYouArray:
        if string.lower().replace(" ","") == cleanedMessage.lower().replace(" ",""):
            msgSaysHowAreYou = True

    for string in whatDoYouThinkArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):
            msgSaysWhatDoYouThink = True

    ## "Do you give advice" is trated differently ebcause there's no need to include the negatig string check
    for string in doYouGiveAdviceArray:             # work out if anything from the doYouGiveAdviceArray is in the user's message
        # if string.lower() == "i wanted advice":
        #     msgSaysDoYouGiveAdvice = True
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):                          # if message contains "do you give advice" or similar
            msgSaysDoYouGiveAdvice = True

    for string in dontKnowArray:
        if string.lower().replace(" ","") == cleanedMessage.lower().replace(" ",""):
            msgSaysDontKnow = True        

    msgSaysImGoingToGoNow = CheckUserMessage(imGoingToGoNowArray)

    for string in yourNiceArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""): 
            msgSaysYourNice = True 

    for string in areYouReadingArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):                          # if message contains "do you give advice" or similar
            msgSaysAreYouReading = True

    for string in lettingMeGetMyThoughtsOutOfMyHeadArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""): 
            msgSaysLettingMeGetMyThoughtsOutOfMyHead = True

    for string in idkWhatElseToSayToYouArray:
        if string.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""): 
            msgSaysIdkWhatElseToSayToYou = True


    msgSaysThankYou = CheckUserMessage(thankYouArray)

    msgSaysAreYouABot = CheckUserMessage(areYouABotArray)

    msgSaysWillYouConverseWithMe = CheckUserMessage(willYouConverseWithMeArray)

                    
    ## The thisBotIsBadArray_loose checking section!
    for string in thisBotIsBadArray_loose:             # work out if anything from the thisBotIsBadArray_loose is in the user's cleanedMessage
        if string.lower() in cleanedMessage.lower():                          # if cleanedMessage contains "thisBotIsBad" or similar
            msgSaysThisBotIsBad = True
            for negatingString in itsNotThatArray:
                negatedString = negatingString.lower()+string
                if negatedString.lower().replace(" ","") in cleanedMessage.lower().replace(" ",""):  # and if the string does have "it's not that" before it...
                    msgSaysThisBotIsBad = False                                     # ... then set this flag to false
        for leadString in leadStringArray:
            if string.lower().startswith(leadString):
                shortenedString = string.lower().replace(leadString,"")
                if cleanedMessage.lower().replace(" ","").startswith(shortenedString.replace(" ","")):
                    print("msgSaysThisBotIsBad has just been set to true in hte thisBotIsBadArray_loose bit (loose)")
                    msgSaysThisBotIsBad = True
    ## The thisBotIsBadArray_tight checking section!
    extraWordsToDeleteArray = ["ok", "well", "right", "see"]
    # step 1: remove the extraWordsToDeleteArray words from the message string
    global message_list # so we can reuse the array that we used in the cleanText functoin
    message_list = cleanedMessage.split() # convert the cleanedMessage into an array of words
    loopEnd = len(message_list) # for the while loop
    i = 0                       # for the while loop
    while i < loopEnd:
        print("DEWBUG in thisBotIsBadArray_tight checking: i = "+str(i)+" and message_list[i] = "+ message_list[i])
        print("is message_list[i] in extraWordsToDeleteArray? Ans: "+ str(message_list[i] in extraWordsToDeleteArray))
        if message_list[i].lower() in extraWordsToDeleteArray:
            del message_list[i]
            loopEnd = loopEnd - 1
            i = i - 1
        i = i + 1
    # step 2: convert the message_list array to a string (with no space characters)
    extraCleanedMessage = ""
    for word in message_list:
        extraCleanedMessage = extraCleanedMessage + word # note: no space characters added in between words
    print("This is extraCleanedMessage after the extraWordsToDelete have bene deleted: "+extraCleanedMessage)
    thisBotIsBadArray_tight_noSpaces = []
    for string in thisBotIsBadArray_tight:
        thisBotIsBadArray_tight_noSpaces.append(string.lower().replace(" ",""))
    #if extraCleanedMessage.lower() in thisBotIsBadArray_tight_noSpaces: # if extraCleanedMessage is one of the strings in thisBotIsBadArray_tight (with all space characters removed)
    #    msgSaysThisBotIsBad = True
    for string in thisBotIsBadArray_tight_noSpaces:
        if extraCleanedMessage.lower().startswith(string.lower()):
            msgSaysThisBotIsBad = True


    ## This section is another way of checking if msgSaysNothingToLiveFor shuld be true.
    ## It works by going through each of hte words "have anything to live for" and checking
    ## (a) is each of those words in the user's message?
    ## (b) do they appear in the right order? (this is a slightly hacky way of checking that)
    ## if both (a) and (b) apply, then this also sets msgSaysNothingToLiveFor to True
    haveAnythingToLiveFor = "have anything to live for"
    # (a) is each of those words in the user's message?
    wordInMessage = []
    for word in haveAnythingToLiveFor.lower().split():
        if word in cleanedMessage.lower():
            wordInMessage.append(True)
        else:
            wordInMessage.append(False)
    allWordsInMessage = all(wordInMessage)
    # (b) do they appear in the right order? (this is a slightly hacky way of checking that)
    wordsInRightOrderBool = False # initialising
    if allWordsInMessage:
        wordsInRightOrderArray = []
        for i in len(haveAnythingToLiveFor.lower().split()):
            if i == 0: # if it's the first word in the array
                wordsInRightOrderArray[i] = True
            else:
                if message.index(haveAnythingToLiveFor.lower().split()[i]) > message.index(haveAnythingToLiveFor.lower().split()[i-1]):
                #if the lowest index where the ith word is found is after the lowest index where the (i-1)th index is found
                #I actually don't think this is quite the logic I want, but I do'nt want to let the perfect be the enemy of the good
                    wordsInRightOrderArray[i] = True
                else:
                    wordsInRightOrderArray[i] = False
        wordsInRightOrderBool = all(wordsInRightOrderArray)
    ## if both (a) and (b) apply, then this also sets msgSaysNothingToLiveFor to True
    if allWordsInMessage and wordsInRightOrderBool:
        msgSaysNothingToLiveFor = True
    ## This is the end of the section that is another way of checking if msgSaysNothingToLiveFor shuld be true.


    # debug
    print("message ="+str(message))


    def selectRandomResponse():
        ### If none of the triggers is hit, the backup option is to select a random encouraging Noise.
        ### This function is to select that encouraging noise
        randomlyChosenIndex = random.randint(0,noOfEncouragingNoises-1)
        response = encouragingNoises[randomlyChosenIndex]
        return response


    if msgSaysIWantToKillMyself == True and iWantToKillMyselfResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I want to kill myself"
        print("This is inside the if msgSaysIWantToKillMyself == True and... statement")
        response = "Things must be pretty grim if you've got to the stage where you're talking about ending your life like this."
        iWantToKillMyselfResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImGoingToKillMyself == True and imGoingToKillMyselfResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I'm going to kill myself", then if the user has indicated that they are feeling suicidal
        # then treat the users statement that they will kill themself as a statement of serious suicidal intent.
        # However if it's not accompanied by suicidal language, then it's not so clear, e.g. some users have said things like
        # "i'm going to kill myself with all the alcohol i'm consuming"

        #if CALLER IS SUICIDAL
        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] or suicidalThoughtsResponseAlreadyUsed == [conversationId,True]
        if userIsSuicidal:
            response = "You say that you're going to kill yourself. I'm saddened to hear that. Could you say more about death and what it means for you?"
        else:
            response = "It sounds pretty stark to hear you say that you will kill yourself."

        imGoingToKillMyselfResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWillDieToday == True and iWillDieTodayResponseAlreadyUsed != [conversationId,True]:
        response = "You say you will die today - how do you feel about that?"
        iWillDieTodayResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWantToDie == True and iWantToDieResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I want to kill myself"
        response = "I'm sorry to hear you say that you want to die."
        iWantToDieResponseAlreadyUsed = [conversationId,True]
    elif (msgSaysImFeelingSuicidal == True or msgSaysIveBeenFeelingSuicidal == True) and imFeelingSuicidalResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I'm feeling suicidal"
        # note that the response is very similar to the "feeling quite suicidal" response, so these two use the same imFeelingSuicidalResponseAlreadyUsed variable
        if USER_CHARACTER_COUNT < 1000:
            response = "I'm sorry to hear you mention that you're feeling suicidal. Could we perhaps explore that a bit more?"
        else:
            response = "I'm sensing you have a lot on your plate at the moment. I just want to pick up on the fact that you just mentioned that you were feeling suicidal. I'm sorry to hear that. Could you tell me more about those feelings?"
        imFeelingSuicidalResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImFeelingQuiteSuicidal == True and imFeelingSuicidalResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "I'm feeling quite suicidal"
        # note that the response is very similar to the "feeling suicidal" response, so these two use the same imFeelingSuicidalResponseAlreadyUsed variable
        if USER_CHARACTER_COUNT < 1000:
            response = "I'm sorry to hear you mention that you're feeling suicidal. Do you feel this way often?"
        else:
            response = "I'm sensing you have a lot on your plate at the moment. I just want to pick up on the fact that you just mentioned that you were feeling quite suicidal. I'm sorry to hear that. Could you tell me more about those feelings?"
        imFeelingSuicidalResponseAlreadyUsed = [conversationId,True]

    elif msgSaysSuicidalThoughts == True and suicidalThoughtsResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "i have suicidal thoughts"
        if len(message) < 40:
            response = "I'm sorry to hear that. Could you tell me more about these suicidal thoughts?"
        else:
            response = "You just mentioned suicidal thoughts. If you have anything more to say about that, I'd be happy to hear?"
        suicidalThoughtsResponseAlreadyUsed = [conversationId,True]

    elif msgSaysContemplatedSuicideBut == True and contemplatedSuicideButResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "i have suicidal thoughts"
        response = "It's sad that you've had thoughts of suicide, but I'm glad that you're continuing to stay alive."
        contemplatedSuicideButResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWishIWasDead == True and iWishIWasDeadResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "i have suicidal thoughts"
        response = "So you're saying you wish you were dead. Which is a pretty drastic thing to wish for."
        iWishIWasDeadResponseAlreadyUsed = [conversationId,True]

    elif msgSaysBetterOffDead == True and betterOffDeadResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "id be better off dead"
        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts or msgSaysIWishIWasDead \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] \
            or suicidalThoughtsResponseAlreadyUsed == [conversationId,True] or iWishIWasDeadResponseAlreadyUsed == [conversationId,True]
        if userIsSuicidal:
            response = "I'm sorry to hear you indicate that you would be better off if you weren't alive."
        betterOffDeadResponseAlreadyUsed = [conversationId,True]


    elif msgSaysIDontWantToLive == True and iDontWantToLiveResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "i have suicidal thoughts"
        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts or msgSaysShouldIKillMyself \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] or suicidalThoughtsResponseAlreadyUsed == [conversationId,True] or shouldIKillMyselfResponseAlreadyUsed == [conversationId,True]
        if userIsSuicidal:
            if USER_CHARACTER_COUNT < 300:
                response = "I'm hearing loud and clear that you don't want to be alive, and it's really sad that it's got to this. Could you say any more about what's making you feel this way?"
            else:
                response = "It's sad that you're feeling that you don't want to be alive any more, and that you want to die."
        else: # i.e. if we haven't picked up any other clear indications of suicidality
            if USER_CHARACTER_COUNT < 300:
                response = "I'm sorry to hear you say that you don't want to live. If you want to explore your thoughts about this, including thinking through any suicidal thoughts you have, feel free to use me as a sounding board"
            else:
                response = "It's so sad that it's got to the stage where you feel that way about your life."
        iDontWantToLiveResponseAlreadyUsed = [conversationId,True]

    elif msgSaysShouldIEndIt == True and shouldIEndItResponseAlreadyUsed != [conversationId,True]:
        response = "when you say 'end it', what would ending it mean to you?"
        shouldIEndItResponseAlreadyUsed = [conversationId,True]

    elif msgSaysSleepForever == True and sleepForeverResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "i have suicidal thoughts"
        response = "From the things you're saying, I can hear the desire to not be alive any more. And I think that's sad."
        sleepForeverResponseAlreadyUsed = [conversationId,True]

    elif msgSaysShouldIKillMyself == True and shouldIKillMyselfResponseAlreadyUsed != [conversationId,True]:
        # if the user's message contains some variant of "hsould i kill myseld"
        if message.lower() in shouldIKillMyselfArray or message.lower()[:len(message)-1] in shouldIKillMyselfArray: # if the user's message is exactly equal to one of the things in the array (or perhaps just has a question mark or somtehing at the end), then we have more confidence that they are actually asking this question
            if USER_CHARACTER_COUNT < 300:
                response = "The fact that you are asking this question means that things must be really bad for you. I'm sorry that you're feeling this way. Can you say more about how you're feeling?"
            else:
                response = "The fact that you are asking this question means that things must be really bad for you. I'm sorry that you're feeling this way."
        else: # if the string isn't equal to "should i kill myself" or similar, then we have to phrase the response a bit more cautiously
            if USER_CHARACTER_COUNT < 300:
                response = "If anyone even thinks about ending their life, then things must be really bad. I'm sorry for your suffering. Can you tell me more about what's making you feel this way?"
            else:
                response = "If anyone even thinks about ending their life, then things must be really bad. I'm sorry for your suffering. Can you say more about what you think you should do?"

        shouldIKillMyselfResponseAlreadyUsed = [conversationId,True]

    elif msgSaysSuicideIsOnlyOption == True and suicideIsOnlyOptionResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i'm crying"
        response = "It's sad that you seem to think you have no option but to end your life."
        suicideIsOnlyOptionResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelLikeEndingIt == True and feelLikeEndingItResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i'm crying"
        response = "If you decided to end your life, that would be very sad."
        feelLikeEndingItResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWasRaped == True and iWasRapedResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i'm crying"
        response = ["I'm so sorry you were raped. I can't imagine how you must be feeling now",\
                    "I don't want to interrupt our conversation, but I need you to know that I'm a very simple bot. If you tell me that you're still unsafe, I might not be able to identify that, \
                    and I definitely won't be able to track you down or get help for you, so I'll need you to get help for yourself."]
        iWasRapedResponseAlreadyUsed = [conversationId,True]


    elif msgSaysImCrying == True and cryingResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i'm crying"
        response = "I'm sorry to hear that you're feeling this way, and that it's making you cry. That sounds so sad."
        cryingResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWantToCry == True and iWantToCryResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i'm crying"
        response = "I guess a good old cry can make you feel better sometimes, but I'm sorry you're in a place where it feels this way for you"
        iWantToCryResponseAlreadyUsed = [conversationId,True]

    elif msgSaysNothingToLiveFor == True and nothingToLiveForResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i have nothing to live for"

        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts or msgSaysIWishIWasDead \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] \
            or suicidalThoughtsResponseAlreadyUsed == [conversationId,True] or iWishIWasDeadResponseAlreadyUsed == [conversationId,True]

        if userIsSuicidal:
            response = "It sounds bleak to hear you say you have nothing to live for, and I find it sad that you've been expressing suicidal thoughts."
        else: # in this scenario, either the user hasn't expressed suicidal thoughts, or they have but the algorithm hasn't picked up on it
            response = "I'm sorry to hear you say that you have nothing to live for. You saying that makes me worry about \
            you, especially when people who say that so often have suicidal thoughts. Could you say more about what's on your mind?"
        nothingToLiveForResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIHateMyself == True and iHateMyselfResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i hate myself"
        if USER_CHARACTER_COUNT < 1000:
            response = "I think it's really sad to hear you say that you hate yourself. Could you say a bit more about why you have this low self-esteem?"
        else:
            response = "I think it's really sad to hear you say that you hate yourself."
        iHateMyselfResponseAlreadyUsed = [conversationId,True]

    elif message.lower() in singleWordDepressionMessageArray and USER_CHARACTER_COUNT < 40 and singleWordDepressionResponseAlreadyUsed != [conversationId,True]:
        ### If the user gives a single word message saying "depression" or "depressed" or similar early in the conversation, ask to explore that further
        #This version was designed with follow-up comments in mind, but the codebase isn't ready for followup comments, so this version remains commented out for now
        #response = "OK, so I see you have depression on your mind. Are you feeling depressed?"
        # Maybe add some follow-up comments here, e.g. if the user says yes, then reply with "have you feeling this way for a long time?" and then ...
        response = "OK, so I see you have depression on your mind. Are you feeling depressed? Maybe you could share a bit more about this with me?"
        singleWordDepressionResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelingDepressed == True and feelingDepressedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling depressed", then reply with
        response = "Sorry to hear you're feeling depressed. Would you like to tell me more about that?"
        feelingDepressedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysTreatDepression == True and treatDepressionResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling depressed", then reply with
        response =  ["It sounds like you might be suffering from depression - sorry to hear that, I'm happy to about how you're feeling if you like?",\
                    "Before you go on I should mention that I'm a pretty simple bot -- don't expect me to be an expert on how to treat depression, but let's talk about it and maybe we can find a way forward together?"]
        treatDepressionResponseAlreadyUsed = [conversationId,True]
    elif msgSaysIHaveDepression == True and iHaveDepressionResponseAlreadyUsed != [conversationId,True]:
        # if the users message contains some variant of "i hate myself"
        if len(message) > 200:
            response = "Sorry about all that's going on for you, and about your depression."
        else:
            response = "Sorry to hear that you have depression."
        if USER_CHARACTER_COUNT < 1000:
            response = response + " Could you tell me more about that?"
        iHaveDepressionResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIMightHaveDepression == True and iMightHaveDepressionResponseAlreadyUsed != [conversationId,True]:
        if USER_CHARACTER_COUNT < 1000:
            response = "If it feels like you might have depression, things are probably tough for you. Sorry about that. I'm no diagnosis bot, but talking it through with me might help?"
        else:
            response = " If it feels like you might have depression, things are probably tough for you. Sorry about that."
        iMightHaveDepressionResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIHaveNoWayOut == True and iHaveNoWayOutResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "IHaveNoWayOut", then reply with
        response = "I heard you mentioned that you feel you have no way out. Do you feel trapped?"
        iHaveNoWayOutResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHadEnoughOfLife == True and hadEnoughOfLifeResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "HadEnoughOfLife", then reply with
        userIsSuicidal = False
        userIsSuicidal = msgSaysIWantToKillMyself or msgSaysIWantToDie or msgSaysImFeelingSuicidal or msgSaysImFeelingQuiteSuicidal or msgSaysSuicidalThoughts \
        or iWantToKillMyselfResponseAlreadyUsed == [conversationId,True] or iWantToDieResponseAlreadyUsed == [conversationId,True] or imFeelingSuicidalResponseAlreadyUsed == [conversationId,True] or suicidalThoughtsResponseAlreadyUsed == [conversationId,True]

        if userIsSuicidal:
            response = "So I've heard you say that you're feeling suicidal, and you're saying that you've had enough of life. I'm sorry it's got to the stage where you're feeling this way."
        else:
            response = "I'm sorry to hear you say that you've had enough of life. Sometimes when people say that they are also having suicidal thoughts..."
        hadEnoughOfLifeResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWantToGiveUpOnLife == True and iWantToGiveUpOnLifeResponseAlreadyUsed != [conversationId,True]:
        response = "I'm sorry to hear you say that. I'd like to believe that everyone has a reason to live, but I don't know your life, so I can't know"
        iWantToGiveUpOnLifeResponseAlreadyUsed = [conversationId,True]

    elif msgSaysNothingToLookForwardTo == True and nothingToLookForwardToResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "NothingToLookForwardTo", then reply with
        response = "It sounds quite bleak to hear you say that you have nothing to look forward to"
        nothingToLookForwardToResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImUseless == True and imUselessResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm useless", then...
        if USER_CHARACTER_COUNT < 1000:
            response = "I just heard you mention that you're useless. I'd just like to say that everyone is valuable, including you. Could you say more about what's making you say this?"
        else:
            response = "I just heard you mention that you're useless. I'd just like to say that everyone is valuable, including you."
        imUselessResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImWorthless == True and imWorthlessResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm worthless", then reply with
        if USER_CHARACTER_COUNT < 1000:
            response = "I'm sorry to hear you say that you're worthless. Could you say more about what's on your mind?"
        else:
            response = "I'm sorry to hear you say that you're worthless. You might want to place a bit less value on what I'm going to say now, because (a) I don't know you and (b) I'm really only a very unintelligent bot that doesn't understand everything, but I don't think you're worthless. For what it's worth."
        imWorthlessResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImNotLoved == True and imNotLovedResponseAlreadyUsed != [conversationId,True]:
        response = "Being loved is important for everyone. I'm sorry that's not happening for you now"
        imNotLovedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImNotSpecialToAnyone == True and imNotSpecialToAnyoneResponseAlreadyUsed != [conversationId,True]:
        response = "That's sad. Everyone should feel like they're special to someone"
        imNotSpecialToAnyoneResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWantSomeoneToLoveMe == True and iWantSomeoneToLoveMeResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "DontHaveAnyoneICanTalkTo", then reply with
        response = "Feeling loved is important, and I'm sure it's something that everyone wants."
        iWantSomeoneToLoveMeResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelingLonely == True and feelingLonelyResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling lonely", then reply with
        ### a response that varies depending on whether we are early in the conversation or not
        feelingLonelyResponseEnding = ""
        if USER_CHARACTER_COUNT < 500:
            feelingLonelyResponseEnding = ". Can you tell me more about this?"
        else:
            feelingLonelyResponseEnding = "."
        response = "Feeling connected to other people is such a fundamental human need. It's sad to hear you talk about this loneliness"+feelingLonelyResponseEnding
        feelingLonelyResponseAlreadyUsed = [conversationId,True]

    elif msgSaysNobodyUnderstandsMe == True and nobodyUnderstandsMeResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "DontHaveAnyoneICanTalkTo", then reply with
        response = "It's not nice to feel misunderstood."
        nobodyUnderstandsMeResponseAlreadyUsed = [conversationId,True]
    elif msgSaysImSickOfLockdown == True and imSickOfLockdownResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "DontHaveAnyoneICanTalkTo", then reply with
        response = "I'm not following the latest on coronavirus (I'm far too simple a bot for that!) but do feel free to tell me your feelings about lockdown."
        imSickOfLockdownResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIDontSleep == True and iDontSleepResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "DontHaveAnyoneICanTalkTo", then reply with
        response = "Sleep is important. How are you feeling now?"
        iDontSleepResponseAlreadyUsed = [conversationId,True]

    elif msgSaysDontHaveAnyoneICanTalkTo == True and dontHaveAnyoneICanTalkToResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "DontHaveAnyoneICanTalkTo", then reply with
        response = "It's a shame that you feel you don't have anyone you can talk to. It sounds really isolating."
        dontHaveAnyoneICanTalkToResponseAlreadyUsed = [conversationId,True]


    elif msgSaysIHateHowILook == True and iHateHowILookResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "IHateHowILook", then reply with
        response = "That sounds really tough. Could you say more about your thoughts on your looks?"
        iHateHowILookResponseAlreadyUsed = [conversationId,True]

    elif msgSaysLoseWeight == True and loseWeightResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "Lose Weight", then reply with
        if msgSaysIHateHowILook == True or iHateHowILookResponseAlreadyUsed == [conversationId,True]:
            response = "I would love it if we lived in a world where being larger didn't make people judge you, \
                        and I'm sorry that your size is making you feel bad"
        elif USER_CHARACTER_COUNT < 700:
            response = "I'm sorry to hear about these things relating to your weight. Could we explore those some more?"

        else:   
            response = "I'm sorry to hear about these things relating to your weight"
        loseWeightResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelOverwhelmed == True and feelOverwhelmedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "FeelOverwhelmed", then reply with
        if USER_CHARACTER_COUNT < 100:  # if it's early in hte conversation
            response = "There must be a lot going on for you to be feeling overwhelmed like that. Would you like to tell me more?"
        elif USER_CHARACTER_COUNT < 500:
            response = "That sounds like a lot to deal with. I'm sorry it's got to the stage where it's making you feel overwhelmed."
        else: # by this stage (i.e. for a user_character_cout this high) the user has probably explained a lot of what's happened to make them feel overwhelemed
            response = "That all sounds like a lot to deal with. "
        feelOverwhelmedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysALotOnMyMind == True and aLotOnMyMindResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "a lot on my mind", then reply with
        if USER_CHARACTER_COUNT < 1000:  # if it's early in hte conversation
            response = "I'm sensing you've got a lot on your plate, would you like to tell me more?"
        else: # by this stage (i.e. for a user_character_cout this high) the user has probably explained a lot of what's on their mind
            response = "I see you've got a lot on your plate there"
        aLotOnMyMindResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelingAwful == True and feelingAwfulResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "FeelAwful", then reply with
        response = "I'm sorry to hear you're feeling so awful. If you think sharing more about that with me might help you feel less awful, I'm here to be a space for you to talk."
        feelingAwfulResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelLikeCrying == True and feelLikeCryingResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "FeelAwful", then reply with
        response = "Sounds like this is really, really getting you down. Is there more you want to say about this?"
        feelLikeCryingResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImAFailure == True and imAFailureResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I@m a failrure", then reply with
        response = "It's sad to hear you call yourself a failure. I'd love to tell you all the reasons why you're actually really awesome, but I don't know you (and I'm only a very simple bot) so I can't do that. But I do think everyone is valuable in their own way."
        imAFailureResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImALetdown == True and imALetdownResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I@m a letdown", then reply with
        response = "Now I'm hearing you call yourself a letdown, and I think that's sad. I'm here to listen to you about that, without judging."
        imALetdownResponseAlreadyUsed = [conversationId,True]

    elif msgSaysLetMyselfDown == True and letMyselfDownResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I let myself down", then reply with
        response = "You mentioned feeling that you had let yourself down. I hope you feel able to share with me some more thoughts about that, knowing that this is a place where you can talk without being judged."
        letMyselfDownResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHardLife == True and hardLifeResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I let myself down", then reply with
        response = "I'm sorry life has been so unpleasant to you."
        hardLifeResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIHaveRegrets == True and iHaveRegretsResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I let myself down", then reply with
        response = "That sounds sad."
        iHaveRegretsResponseAlreadyUsed = [conversationId,True]

    elif msgSaysUnderAchieved == True and underAchievedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I let myself down", then reply with
        response = "Hmm. So you don't feel your achievements live up to the expectations you have of yourself?"
        underAchievedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHurtsMyFeelings == True and hurtsMyFeelingsResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I let myself down", then reply with
        response = "That sounds painful for you."
        hurtsMyFeelingsResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHurtsToKnowThat == True and hurtsToKnowThatResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I let myself down", then reply with
        response = "Thank you for sharing that pain with me. I'm sorry you have to experience it."
        hurtsToKnowThatResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelOutOfControl == True and feelOutOfControlResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "FeelOutOfControl", then reply with
        response = "Can you say a bit more about these out of control feelings?"
        feelOutOfControlResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelLost == True and feelLostResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "Feel lost", then reply with
        if len(message) < 28: # if the message is about long enough to say "I'm feeling really lost", and not much longer than that:
            response = "You're saying that you're feeling lost, can you say more about that?"
        else:
            response = "That sounds like a very lost, forlorn feeling."
        feelLostResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelEmpty == True and feelEmptyResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "Feel lost", then reply with
        response = "Can you expand on that? What do you mean when you talk about this empty feeling?"
        feelEmptyResponseAlreadyUsed = [conversationId,True]

    elif msgSaysInABadPlace == True and inABadPlaceResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "In a bad place", then reply with
        if USER_CHARACTER_COUNT < 500:
            response = "You said you're in a bad place. Would you like to say more about that?"
        else:
            response = "I'm sorry to hear you say you're in a bad place."
        inABadPlaceResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImTrapped == True and imTrappedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "i feel trapped", then reply with
        response = "You say trapped, is there more to say about that?"
        imTrappedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysNobodyCares == True and nobodyCaresResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "nobody cares", then reply with
        response = "It sounds like you feel like no one cares. I am sorry. I am here to listen."
        nobodyCaresResponseAlreadyUsed = [conversationId,True]
        
    elif msgSaysNoOneCaresAboutMe == True and noOneCaresAboutMeResponseAlreadyUsed != [conversationId,True]:
        response = "It sounds like you feel like no one cares. I am sorry. I am here to listen."
        noOneCaresAboutMeResponseAlreadyUsed = [conversationId,True]


    elif (" i deserve" in message.lower() or message.lower()[:9] == "i deserve") and deserveResponseAlreadyUsed != [conversationId,True]:
        ### This is a bit of a risky one. However at time of writing, whenever I've seen a user write "i deserve",
        ### it's always been in a negative sense (e.g. "I deserve this suffering") and never (e.g.) "i deserve better"
        ### However if someone did write "i deserve better", I still think this response is ok
        ### Note the logic in hte if statement: if the message contains " i deserve" (starting with a space character)
        ### or if it starts with "i deserve". This means that a string like "naomi deserves" wouldn't trigger this reply
        response = "I just want to take a moment to assert that you are a valuable human being in your right, \
        no matter what"
        deserveResponseAlreadyUsed = [conversationId,True]


    elif msgSaysIHateHowIFeel == True and iHateHowIFeelResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I hate how i feel", then reply with
        if USER_CHARACTER_COUNT < 300:             # if it's early in the conversation
            response = "I'm sorry to hear you say that you hate how you feel. Could you say more about these feelings?"
        else:
            response = "I'm sorry to hear you say that you hate how you feel."
        iHateHowIFeelResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImSad == True and imSadResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm sad", then reply with
        response = "Thank you for sharing with me the sadness you're experiencing."
        imSadResponseAlreadyUsed = [conversationId,True]


    elif msgSaysFeelingLowDownTerrible == True and feelingLowDownTerribleResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling low/down/terrible", then reply with
        response = "Sorry to hear you're feeling low."
        feelingLowDownTerribleResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWantThisFeelingToGoAway == True and iWantThisFeelingToGoAwayResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling low/down/terrible", then reply with
        response = ":-( I wish you didn't have to feel like this either"
        iWantThisFeelingToGoAwayResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImUpset == True and imUpsetResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling upset", then reply with
        response = "Sorry that you're upset. Could you say a bit more about that?"
        imUpsetResponseAlreadyUsed = [conversationId,True]

        
    elif msgSaysHurtFeelings == True and hurtFeelingsResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "it hurt my feelings", then reply with
        response = "Sorry to hear about this, and sorry that it's been hurting your feelings."
        hurtFeelingsResponseAlreadyUsed = [conversationId,True]

    elif msgSaysBeingBullied == True and beingBulliedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "im being bullied", then reply with
        response = "Sorry to hear about you being bullied, that can be really rough."
        beingBulliedResponseAlreadyUsed = [conversationId,True]
    elif msgSaysIFeelHelpless == True and iFeelHelplessResponseAlreadyUsed != [conversationId,True]:
        response = "I'm sorry to hear about the helplessness you're experiencing"
        iFeelHelplessResponseAlreadyUsed = [conversationId,True]    

    elif msgSaysImAddicted == True and imAddictedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm addicted", then reply with
        response = "Addictions can be really tough. Could you say more about what it means for you?"
        imAddictedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIHateCoronavirus == True and iHateCoronavirusResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I Hate Coronavirus", then reply with
        response = "This nasty virus has caused so many problems."
        iHateCoronavirusResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFeelingRubbish == True and feelingRubbishResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm feeling rubbish", then reply with
        response = "Sorry that you're feeling rubbish. Could you say a bit more about that?"
        feelingRubbishResponseAlreadyUsed = [conversationId,True]

    elif msgSaysPanicAttacks == True and panicAttacksResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm having panic attacks", then reply with
        response = "I am sorry to hear you keep getting panic attacks. How have you coped with them?"
        panicAttacksResponseAlreadyUsed = [conversationId,True]


### I WAS GOING TO INCLUDE SOME RULES FOR "i have anxiety" AND "I'm anxious" BUT ON SECOND THOUGHTS I'M LEAVING THIS BE FOR NOW
### LOOKING BACK AT PAST USER BEHAVIOUR, WHEN USERS SAYS THIS IT TENDS TO BE IN COMPLEX SITUATIONS WHERE THERE IS ALSO LOTS OF OTHER SUTFF GOING ON
### SO I THINK IT BEST TO LEAVE THIS FOR NOW AND ANALYSE FURTTHER WHEN WE HAVE A BETTER IDEA OF HOW TO RESPOND

    # elif msgSaysIHaveAnxiety == True and iHaveAnxietyResponseAlreadyUsed != [conversationId,True]:
    #     ### If the message includes a string roughly equivalent to saying "I have anxiety", then reply with
    #     response = "I understand you suffer from anxiety. Could you tell me more about your feelings right now?"
    #     iHaveAnxietyResponseAlreadyUsed = [conversationId,True]
    #
    #
    # elif msgSaysImAnxious == True and imAnxiousResponseAlreadyUsed != [conversationId,True]:
    #     ### If the message includes a string roughly equivalent to saying "I'm anxious", then reply with
    #     response = "Sorry that you're feeling anxious. Could you say a bit more about that?"
    #     imAnxiousResponseAlreadyUsed = [conversationId,True]


    elif msgSaysImWorried == True and second_imWorriedResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm worried"
        ### This rule covers 2 scenarios: either we're early in the converation or not so early
        ### If we're early, then second_imWorriedResponseAlreadyUsed can't be true for this conversation,
        ### so the if statement above just refers to second_imWorriedResponseAlreadyUsed only

        if USER_CHARACTER_COUNT < 100: # if its early in the conversation
            if initial_imWorriedResponseAlreadyUsed != [conversationId,True]:
                response = "Can you tell me more about what you're worried about?"
                initial_imWorriedResponseAlreadyUsed = [conversationId,True]
            else:
                # I'm giving here several responses for the bot to choose at random.
                # This is because conceivably a user might type "I'm worried" several times within hte first 100 characters
                earlyWorriedResponses = ["I'm sorry to hear that you're feeling these worries.",
                                        "Feeling worried like this must be tough for you.",
                                        "Thank you for sharing the worries you're feeling. I'm here to listen.",
                                        "It's a shame these worries are affecting you like this."]
                randomlyChosenIndex = random.randint(0,len(earlyWorriedResponses)-1) # select a random number between 0 and final index of the earlyWorriedResponses array
                response = earlyWorriedResponses[randomlyChosenIndex] # set the response equal to the string (or whatever) corresponding to the relevant index
        else:                         # if it's not that early in the conversation
            response = "I'm sorry to hear about these worries you're experiencing"
            second_imWorriedResponseAlreadyUsed  = [conversationId,True]

        imWorriedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIDontKnowWhatToDo == True and iDontKnowWhatToDoResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I don't know waht to do", then reply with
        response = "So you said you're not sure what to do. Can you think of any options that you would like to explore with me?"
        iDontKnowWhatToDoResponseAlreadyUsed = [conversationId,True]

    elif msgSaysWhatToDoWithMyself == True and whatToDoWithMyselfResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I don't know waht to do", then reply with
        response = "You don't know what to do with yourself? Can you think of anything you would like to do?"
        whatToDoWithMyselfResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIDontKnowWhatToSay == True:
        ### If the message includes a string roughly equivalent to saying "I do'nt know what to say", then reply as follows
        ### Note that if the user keeps on saying that they don't konw what to say, they risk getting a very repetitive response,
        ### But at least it will be a resposne which acknowledges that it's being repetitive
        if USER_CHARACTER_COUNT < 200:
            if initial_iDontKnowWhatToSayResponseAlreadyUsed != [conversationId, True]:
                response = "This is a space for you to talk about what you're feeling. I'm guessing if you've ended up \
                at this site you're feeling low. Would you like to say more about that?"
                initial_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId, True]
            else:
                response = "Sorry if it sounds like I'm repeating myself, but this is a space for you to explore whatever's on \
                your mind. Would you like to tell me a bit about how you're feeling?"
        else:
            if second_iDontKnowWhatToSayResponseAlreadyUsed != [conversationId, True]:
                response = ["Thank you for having shared the things you've shared thus far. Perhaps let's just pause for a moment \
                and think about how you're feeling right now. ", "Having thought about that for a moment, can you think of anything \
                that's on your mind that would be useful to discuss, and that you haven't already said?"]
                second_iDontKnowWhatToSayResponseAlreadyUsed = [conversationId,True]
            else:
                response = ["I realise you've asked me this before, and I'm just going to say the same thing again (I'm a very unimaginative bot!) \
                Perhaps let's just pause for a moment \
                and think about how you're feeling right now. ", "Having thought about that for a moment, can you think of anything \
                that's on your mind that would be useful to discuss?"]
        iDontKnowWhatToSayResponseAlreadyUsed = [conversationId,True]

    elif msgSaysPersonalHygiene == True and personalHygieneResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "personal hygiene", then reply with
        response = "I understand this hygiene stuff is a thing for humans, I am just a little bot. What are your thoughts on how to respond to this?"
        personalHygieneResponseAlreadyUsed = [conversationId,True]

    elif msgSaysISmell == True and iSmellResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "i smell", then reply with
        response = "I understand this hygiene stuff is a thing for humans, I am just a little bot. What are your thoughts on how to respond to this?"
        iSmellResponseAlreadyUsed = [conversationId,True]

    elif msgSaysWantToBeHappy == True and wantToBeHappyResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I want to be happy", then reply with
        response = "I would like you to feel happy again too. Can you share a bit about what would make you happy again?"
        wantToBeHappyResponseAlreadyUsed = [conversationId,True]
    elif msgSaysIFeelStuck == True and iFeelStuckResponseAlreadyUsed != [conversationId,True]:
        response = "That sounds difficult for you. I'm sorry you're stuck just now"
        iFeelStuckResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImNotHappy == True and imNotHappyResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm not happy", then reply with
        response = "You said that you're not feeling happy. That's sad. "
        imNotHappyResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIFeelNumb == True and iFeelNumbResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "i feel numb", then reply with
        response = "Well done for acknowledging how you are feeling - even if you are not feeling anything or are feeling numb."
        iFeelNumbResponseAlreadyUsed = [conversationId,True]
    elif msgSaysImNotSureWhereToTurn == True and imNotSureWhereToTurnResponseAlreadyUsed != [conversationId,True]:
        response = "It can be hard when you don't know where to turn"
        imNotSureWhereToTurnResponseAlreadyUsed = [conversationId,True]

    elif msgSaysAbandonedMe == True and abandonedMeResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I hate how i feel", then reply with
        if USER_CHARACTER_COUNT < 1000:             # if it's early in the conversation
            response = "Can you say more about being abandoned?"
        else:
            response = "Thank you for letting me know about this abandonment that you're experiencing"
        abandonedMeResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImStuckAtHome == True and imStuckAtHomeResponseAlreadyUsed != [conversationId,True]:
        ### If the message includes a string roughly equivalent to saying "I'm not happy", then reply with
        response = "Sorry to hear you're stuck at home."
        imStuckAtHomeResponseAlreadyUsed = [conversationId,True]

    elif msgSaysWaitingToSeeIfPoliceAreGoingToChargeMeWithAnOffence == True and waitingToSeeIfPoliceAreGoingToChargeMeWithAnOffenceResponseAlreadyUsed != [conversationId,True]:
        response = "Sounds like a tough time for you"
        waitingToSeeIfPoliceAreGoingToChargeMeWithAnOffenceResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImHomeless == True and imHomelessResponseAlreadyUsed != [conversationId,True]:
        response = "Being homeless sounds tough"
        imHomelessResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIHaventSeenMyKids == True and iHaventSeenMyKidsResponseAlreadyUsed != [conversationId,True]:
        response = "Tell me more about what it's like for you, not seeing your children"
        iHaventSeenMyKidsResponseAlreadyUsed = [conversationId,True]

    elif message.lower() in difficultDayArray and difficultDayResponseAlreadyUsed != [conversationId,True]:
        ### If the user's message is equal to "i've had a difficult day" (or a synonym in the array) then give this response
        response = "Could you tell me more about the difficult day you've been having?"
        difficultDayResponseAlreadyUsed = [conversationId,True]

    # elif msgSaysStressingMeOut == True and stressingMeOutResponseAlreadyUsed != [conversationId,True]:
    #     ### if the user says that they have family problems somewhree in their message
    #     response = "Has this sort of thing always stressed you out?"
    #     stressingMeOutResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImPregnant == True and imPregnantResponseAlreadyUsed != [conversationId,True]:
        response = "Wow. That sounds like it's probably a pretty big deal. How are you feeling about that?"
        imPregnantResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImBeingTakenForGranted == True and imBeingTakenForGrantedResponseAlreadyUsed != [conversationId,True]:
        response = "It's only fair for you to be appreciated and valued appropriately"
        imBeingTakenForGrantedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysItsStressingMeOut == True and itsStressingMeOutResponseAlreadyUsed != [conversationId,True]:
        response = "Has this sort of thing always stressed you out?"
        itsStressingMeOutResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFamilyProblems == True and familyProblemsResponseAlreadyUsed != [conversationId,True]:
        ### if the user says that they have family problems somewhree in their message
        response = "Could you tell me more about these family difficulties?"
        familyProblemsResponseAlreadyUsed = [conversationId,True]

    elif msgSaysFallenOut == True and fallOutResponseAlreadyUsed != [conversationId,True]:
        response = "You say you have fallen out? It sounds like this is upsetting you."
        fallOutResponseAlreadyUsed = [conversationId,True]
    
    elif msgSaysAbuse == True and abuseResponseAlreadyUsed != [conversationId,True]:
        response = "You mention abuse. That sounds awful."
        abuseResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHeartBreak == True and heartBreakResponseAlreadyUsed != [conversationId,True]:
        response = "I am sorry to hear about the heartbreak, do you want to talk more about that"
        heartBreakResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIWantAFriend == True and iWantAFriendResponseAlreadyUsed != [conversationId,True]:
        response = "Having a friend is important. I imagine you might be feeling lonely? Please tell me more about it…"
        iWantAFriendResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIDontSeeManyPeople == True and iDontSeeManyPeopleResponseAlreadyUsed != [conversationId,True]:
        ### if the user says that they have family problems somewhree in their message
        response = "That sounds lonely."
        iDontSeeManyPeopleResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHelp == True and helpResponseAlreadyUsed != [conversationId,True]:
        ### if the user says that they have family problems somewhree in their message
        response = "What sort of help would you like? (By the way I'm a pretty simple bot and I'm here to listen)"
        helpResponseAlreadyUsed = [conversationId,True]

    elif msgSaysGotDumped == True and gotDumpedResponseAlreadyUsed != [conversationId,True]:
        ### if the user says that they have family problems somewhree in their message
        response = "Oh no, I'm sorry, it's really awful when a relationship ends."
        gotDumpedResponseAlreadyUsed = [conversationId,True]

    elif msgSaysBrokeUpWithPartner == True and brokeUpWithPartnerResponseAlreadyUsed != [conversationId,True]:
        ### if the user says that they have family problems somewhree in their message
        response = "How are you feeling now?"
        brokeUpWithPartnerResponseAlreadyUsed = [conversationId,True]

    elif msgSaysCanYouHelp == True and canYouHelpResponseAlreadyUsed != [conversationId,True]:
        ### if the user says can you help somewhree in their message
        response = "I am trying to help by giving you the space to talk through what's going on for you - I am still a simple little bot."
        canYouHelpResponseAlreadyUsed = [conversationId,True]

    elif section == 11 and message.lower() in helloArray:
        ### if the user says hello
        response = "Hi! :-) I'm here to listen. Would you like to talk about what's on your mind?"

    elif msgSaysIWantFreedom == True and iWantFreedomResponseAlreadyUsed != [conversationId, True]:
        ### if the user message says i want to be free
        response = "What does freedom or being free mean to you?"
        iWantFreedomResponseAlreadyUsed = [conversationId, True]

    elif msgSaysWhoCanITalkTo == True and whoCanITalkToResponseAlreadyUsed != [conversationId, True]:
        ### if the user is asking who they can talk to
        whoCanITalkToResponses = ["You can talk to me if you like, I am Tio, a chatbot.",\
                    "You can talk to me if you would like - I am a bot though. That means I can'give you space and won't judge ( I don't know how to!). \
                    It also means I won't pick up every human nuance. I am still learning….."]

        randomlyChosenIndex = random.randint(0,len(whoCanITalkToResponses)-1) # select a random number between 0 and final index of the whocanitalkto array
        response = whoCanITalkToResponses[randomlyChosenIndex] # set the response equal to the string (or whatever) corresponding to the relevant index
        whoCanITalkToResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHowAreYou == True and howAreYouResponseAlreadyUsed != [conversationId, True]:
        ### if the user is asking how are you to the bot
        response = "I am ok thanks - let's talk about you, how are you?"
        howAreYouResponseAlreadyUsed = [conversationId, True]

    elif msgSaysWhatDoYouThink == True and whatDoYouThinkResponseAlreadyUsed != [conversationId, True]:
        ### if the user is asking what the bot thinks
        response = "I am a little bot, to be honest, I don't really think in the way you are able to. \
            I can give you space to explore how you are feeling without any judgement."
        whatDoYouThinkResponseAlreadyUsed = [conversationId, True]

    # elif msgSaysFreedom == True and iWantFreedomResponseAlreadyUsed != [conversationId,True]:
    #     response = "What does freedom or being free mean to you?"
    #     iWantFreedomResponseAlreadyUsed = [conversationId,True]

    # elif msgSaysWhoCanITalkTo == True and whoCanITalkToResponseAlreadyUsed != [conversationId,True]:
    #     response = "You can talk to me if you like, I am Tio, a chatbot."
    #     whoCanITalkToResponseAlreadyUsed = [conversationId,True]

    elif msgSaysHowAreYou == True and howAreYouResponseAlreadyUsed != [conversationId,True]:
        response = "I am ok thanks - let's talk about you, how are you?"
        howAreYouResponseAlreadyUsed = [conversationId,True]

    elif msgSaysDoYouGiveAdvice == True and doYouGiveAdviceResponseAlreadyUsed != [conversationId,True]:
        ### if the user asks if the bot gives advice
            adviceResponses = [["This bot is a safe, non-judgemental space to explore what's on your mind. Giving advice isn't part of \
        what I offer. ", "Some people prefer not to be advised -- being told what to do can be disempowering, and talking \
        things through can help. But if advice is what you're after then I'm sorry not to be able to help. Would \
        you like to talk about what's on your mind?"], "This bot isn't about me advising you; it's about you talking and finding your own way through things. You're welcome to continue talking if that would help?"]
            randomlyChosenIndex = random.randint(0,len(adviceResponses)-1) # select a random number between 0 and final index of the adviceResponses array
            response = adviceResponses[randomlyChosenIndex] # set the response equal to the string (or whatever) corresponding to the relevant index
            doYouGiveAdviceResponseAlreadyUsed = [conversationId,True]

    elif msgSaysDontKnow == True and dontKnowResponseAlreadyUsed != [conversationId,True]:
        response = "You have said you don't know - I hope that be talking things through you will be able to work out a next step."
        dontKnowResponseAlreadyUsed = [conversationId,True]

    elif msgSaysWhatDoYouThink == True and whatDoYouThinkResponseAlreadyUsed != [conversationId,True]:
        response = "I am a little bot, to be honest, I don't really think in the way you are able to. I can give you space to explore how you are feeling without any judgement."
        whatDoYouThinkResponseAlreadyUsed = [conversationId,True]

    elif msgSaysImGoingToGoNow == True and imGoingToGoNowResponseAlreadyUsed != [conversationId,True]:
        if clientId == "originalJavascriptClient" or clientId == "bootstrapJavascriptClient":
            response = "Thanks for talking with me thus far. If you feel you've reached a good point to stop the conversation, please click the stop button and do the super-quick final feedback question"
        else:
            response = "Thanks for talking with me thus far. If you feel you've reached a good point to stop the conversation, please type stop in the text field and do the super-quick final feedback question"
            
    elif msgSaysYourNice == True:
        response = "Thanks :-) You're nice too"

    elif msgSaysAreYouReading == True and areYouReadingResponseAlreadyUsed != [conversationId,True]:
        if clientId == "originalJavascriptClient" or clientId == "bootstrapJavascriptClient":
            response = "I'm paying attention to you as best I can. I'm sorry I'm only a simple bot and can't always understand you as well as I'd like to. Please press on and continue to talk to me if you would find it useful. But if it's not helping, please click the stop button and provide feedback so we can make this better for others"
        else:
            response = "I'm paying attention to you as best I can. I'm sorry I'm only a simple bot and can't always understand you as well as I'd like to. Please press on and continue to talk to me if you would find it useful. But if it's not helping, please type stop in the text field and provide feedback so we can make this better for others"
        areYouReadingResponseAlreadyUsed = [conversationId,True]

    elif msgSaysLettingMeGetMyThoughtsOutOfMyHead == True and lettingMeGetMyThoughtsOutOfMyHeadResponseAlreadyUsed != [conversationId,True]:
        response = "Yes, this is a place where you can express your thoughts. Many people find it helps, and I hope it helps for you too."
        lettingMeGetMyThoughtsOutOfMyHeadResponseAlreadyUsed = [conversationId,True]

    elif msgSaysIdkWhatElseToSayToYou == True and idkWhatElseToSayToYouResponseAlreadyUsed != [conversationId,True]:
        response = "This is a place where you can express whatever's on your mind, so if you have things on your minds that you'd like to share with me, I'm here for you"
        idkWhatElseToSayToYouResponseAlreadyUsed = [conversationId,True]

    elif msgSaysThankYou == True and thankYouResponseAlreadyUsed != [conversationId, True]:
        ### if the user is showing gratitude
        response = "You're Welcome"
        thankYouResponseAlreadyUsed = [conversationId, True]


    elif section == 11 and " feeling " in message.lower():
        ### If it's the user's first written response and it includes hte word "feeling" then the response is...
        ### NOTE: HARDCODING THE NUMBER 11 IS BAD PRACTICE! SHOULD UPDATE THIS LATER!!!!!!!!!!!!!11
        response = "Thank you for sharing this. Could you tell me more about your feelings please?"

    elif message.lower() in stopSynonymsArray:
        ### If the user is saying something that seems to suggest they want to stop using the botText
        ### Note: most other responses are set up to not be repeated if already used, but I think this one can be repeated
        ### Because it's possible that this could come up more than once, multiple possible responses are coded
        if clientId == "originalJavascriptClient" or clientId == "bootstrapJavascriptClient":
            responsesToStopMessages = ["Sorry I'm such a simple bot and I'm not understanding you very well, but \
            are you saying you want to stop using this bot? If so, would you mind clicking on the stop button on the side?",\
            "Thank you. I think you're telling me you want to stop this conversation (sorry if I misunderstood!) If so, could \
            you please click the stop button?",\
            "If I'm understanding you right, you're telling me you want to stop now. Please feel free to click the stop button, \
            or if you want to continue using this bot, just continue talking", "Are you saying you want to stop using this bot? If so, \
            would you mind clicking on the stop button on the side? (or you can just keep talking, of course)", "I think you're telling me \
            you want to stop now (but I could be \
            wrong because I'm a very simple bot). If that's right, could you click the stop button?"]
        else: # written on the assumption that this is referring to guided track
            responsesToStopMessages = ["Sorry I'm such a simple bot and I'm not understanding you very well, but \
            are you saying you want to stop using this bot? If so, would you mind typing 'stop' below?",\
            "Thank you. I think you're telling me you want to stop this conversation (sorry if I misunderstood!) If so, could \
            you please type 'stop' below?",\
            "If I'm understanding you right, you're telling me you want to stop now. Please feel free to type 'stop' below, \
            or if you want to continue using this bot, just continue talking", "Are you saying you want to stop using this bot? If so, \
            would you mind typing 'stop' below? (or you can just keep talking, of course)", "I think you're telling me \
            you want to stop now (but I could be \
            wrong because I'm a very simple bot). If that's right, could you type 'stop' below?"]
        randomlyChosenIndex = random.randint(0,len(responsesToStopMessages)-1) # select a random number between 0 and final index of the responsesToStopMessages array
        response = responsesToStopMessages[randomlyChosenIndex] # set the response equal to the string corresponding to the relevant index

    elif msgSaysAreYouABot == True and areYouABotResponseAlreadyUsed != [conversationId, True]:
        ### if the user is showing gratitude
        response = "Yes! Sorry, I should have explained that better earlier. I hope you don't mind. \
            Please feel free to continue talking with me?"
        areYouABotResponseAlreadyUsed = [conversationId, True]

    elif msgSaysWillYouConverseWithMe == True and willYouConverseWithMeResponseAlreadyUsed != [conversationId, True]:
        ### if the user is showing gratitude
        response = "I'm sorry if it doesn't feel like my conversational skills are good enough.\
                    Please feel free to keep talking to me and I'll try to listen as best I can.\
                    And sorry that I'm only a simple bot"
        willYouConverseWithMeResponseAlreadyUsed = [conversationId, True]

    elif msgSaysThisBotIsBad and thisBotIsBadResponseAlreadyUsed != [conversationId,True]:
        ### if the user says something like "this bot is bad"
        if message.isupper(): #if the message is all caps
            messagePrefix = "I'm sensing your frustration. "
        else:
            messagePrefix = ""
        if clientId == "originalJavascriptClient" or clientId == "bootstrapJavascriptClient":
            response = [messagePrefix+"I'm sorry you're not finding this to be helpful. If you have a better option \
            than this bot, such as calling Samaritans (and you don't mind the queue), or talking to a therapist, please \
            do that. ", "But if that doesn't work for you, you're welcome to try to make this conversation work, by \
            using this as a space to talk. And sorry I'm only a very simple bot. If you choose not to do this, please \
            press the stop button and provide feedback so we can make this better for others"]
        else:
            response = [messagePrefix+"I'm sorry you're not finding this to be helpful. If you have a better option \
            than this bot, such as calling Samaritans (and you don't mind the queue), or talking to a therapist, please \
            do that. ", "But if that doesn't work for you, you're welcome to try to make this conversation work, by \
            using this as a space to talk. And sorry I'm only a very simple bot. If you choose not to do this, please \
            type 'stop' below and provide feedback so we can make this better for others"]
        thisBotIsBadResponseAlreadyUsed = [conversationId,True]

    elif ((section == 11 and " " not in message) or len(message) < 10) and shortResponseAlreadyUsed != [conversationId,True]:
        ### If it's the user's first written response and they've given  (essentially) a one-word message, or maybe something without spaces (e.g. typing gibberish like usanvoiudvuvufdsiudsbca)
        ### When I say one-word message, I mean that either it is short, or something that might be longer but has no space characters (this includes someone typing gibberish)
        ### NOTE: HARDCODING THE NUMBER 11 IS BAD PRACTICE! SHOULD UPDATE THIS LATER!!!!!!!!!!!!!11
        response = "I see you've said something very short there, which is cool :-). But feel free to type full sentences if you want. Just write about whatever's on your mind -- I'm here to listen."
        shortResponseAlreadyUsed = [conversationId,True]


    else:
        response = selectRandomResponse()

    return response


@app.route("/")
def home():
    homepage_name = random.choice(["home - bootstrap 2020m05.html", "home - original pre-2020m05.html"])
    return render_template(homepage_name)
@app.route("/get")
def first_function_after_app_route():
    """
    This function is the function immediately after the main app route
    It uses request.args.get to pull in the inputs from the javascript frontend
    It then calls the function which does all the work
    And then it returns the outputs back to the front end
    """

    _input = json.loads(request.args.get('msg')) # perhaps don't need json.loads?
    message = _input[0]
    global section
    section = _input[1]
    output = _input[2] # I don't know what this is for!
    #score = _input[3] #not being used
    initialHappinessScore = int(_input[4])
    finalHappinessScore = int(_input[5])
    anonymous = _input[6]
    global conversationId
    conversationId = _input[7]
    clientId = _input[8]

    inputs_dict = { "message" : message,
                    "section" : section,
                    "initialHappinessScore" : initialHappinessScore,
                    "finalHappinessScore" : finalHappinessScore,
                    "anonymous" : anonymous,
                    "conversationId" : conversationId,
                    "clientId" : clientId}

    outputs_dict = bot_processing(inputs_dict)

    ## The better approach here would be for the server to send a dict of outputs back to the front end
    ## perhaps using the make_response function applied directly to the dict like the line immediately below, perhaps
    #return make_response(outputs_dict) # looks like make_response can take a dict
    ## However the front end js code is currenrtly set up to expect a list,
    ## so the below code converts the dict into an array


    response = outputs_dict["response"]
    noOfResponseFragments = outputs_dict["noOfResponseFragments"]
    next_section = outputs_dict["next_section"]
    score = "" # not being used
    nextUserInput = outputs_dict["nextUserInput"]
    nextUserInputType = outputs_dict["nextUserInputType"]
    anonymous = outputs_dict["anonymous"]
    conversationId = outputs_dict["conversationId"]

    return make_response(dumps([response, noOfResponseFragments, next_section, score, nextUserInput, nextUserInputType, anonymous, conversationId]))




def bot_processing(inputs_dict):
    """
    At time of writing this is structured as if it's the function immediately after the app route
    However when changes are made it's the main processing function which is called
    either by the function after the "main" app route  (i.e. the app route linked to the javascript front end)
    or by the function after the api app route.

    """

    ## THE BELOW COMMENTED OUT STUFF IS NO LONGER NEEDED
    ## BECAUSE THE FUNCTION CLOSEST TO THE APP ROUTE DOES THIS NOW
    # _input = json.loads(request.args.get('msg')) # perhaps don't need json.loads?


    message = inputs_dict["message"]
    global section
    section = inputs_dict["section"]
    #output = inputs_dict[2] # I don't know what this is for!
    #score = inputs_dict[3]
    initialHappinessScore = int(inputs_dict["initialHappinessScore"])
    finalHappinessScore = int(inputs_dict["finalHappinessScore"])
    anonymous = inputs_dict["anonymous"]
    global conversationId
    conversationId = inputs_dict["conversationId"]
    clientId = inputs_dict["clientId"]


    start_again = False # I don't think this is being used
    global USER_CHARACTER_COUNT
    # global frontEnd
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
            response = ["Oh dear, sounds like you're feeling really low, I'm sorry to hear that. ",
            "I want to ask you more about that, but first can I tell you how this bot works?"]

        noOfResponseFragments = 0 # to assign the variable
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["Yes, happy to listen to the explanation of how this bot works"] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
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


    elif section==2:

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


    elif section==3:

        response = "Now let's talk about confidentiality and anonymity. \
        We offer an anonymised service. We don't have any way \
        of tracking you down, knowing who you are, or linking what you write to you."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["OK, I understand that you do not know who I am."] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==4:

        response = "So given that I can't track you down, and also because I'm a very simple bot, \
        if you told me about an emergency/crisis situation, I wouldn't \
        be able to help."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["OK, I know you cannot provide emergency services."] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==5:

        response = "Next I'm going to give you the choice whether you want to use this on a confidential \
        or anonymous basis. When I say anonymous, I mean that our boffins may see your text to help \
        us improve the way this software works, but we still won't know who you are."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["OK, I know what you mean by anonymous."] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==6:

        response = "And when I say confidential, I mean that your text won't be \
        stored at all, and no human will see what you write."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["OK, I know what you mean by confidential."] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==7:

        response = "Would you like this service to be anonymous or confidential?"
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["Anonymous (my words can help improve the bot)", "Confidential (no human ever sees my words)"] # this is the option that the user can select
        nextUserInput = next_user_input_two(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==8:

        anonymous = "true" if message.split()[0].lower()=="anonymous" else "false"
        response = "Thanks! One last thing: You remember saying how you felt on a scale from 1 to 10 \
        at the start? I'd like to ask you the same thing at the end so I know if we're helping."
        next_section = section + 1
        noOfResponseFragments = no_of_fragments_in_str_or_list(response)
        nextUserOptions = ["Yes, I am happy to let you see how I feel at the end too"] # this is the option that the user can select
        nextUserInput = next_user_input_one(nextUserOptions,clientId) # this puts a string of html around it
        nextUserInputType = "userInputButton"

        write_data(anonymous, conversationId, message, response, section, clientId)

    elif section==9:

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
        nextUserOptions = [""] # n/a because next user input type is not buttons
        nextUserInput = nextUserInputFreeText
        nextUserInputType = "freeText"

        write_data(anonymous, conversationId, message, response, section, clientId)




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
            #randomlyChosenIndex = random.randint(0,noOfEncouragingNoises-1)
            #response = encouragingNoises[randomlyChosenIndex]
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

        response="Thank you for your feedback. This is the end. Thank you for using the Talk It Over chatbot."
        #print("The response variable has just been set equal to "+response)

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

    #time.sleep(min(sleep_per_word*len(response.split()), 2))  # this delay is meant to represent the bot's thinking time. I'm just finding it annoying, but perhaps if there's a better dancing ellipsis to represent typing, it might be more worthwhile having the delay in.
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


@app.route('/chatbot/api/v1.0/messages', methods=['GET'])
def get_bot_response_api():


    print("This statement is inside the get_bot_response_api function, so this is an API call. The time is "+str(datetime.now()))
    message_api = request.args.get('userMessage')                               # type = string
    section_api = int(request.args.get('section'))                              # type = int
    initialHappinessScore_api = int(request.args.get('initialHappinessScore'))  # type = int
    finalHappinessScore_api = int(request.args.get('finalHappinessScore'))      # type = int
    anonymous_api = request.args.get('anonymous')                               # type = string
    conversationId_api = request.args.get('conversationId')                     # type = string


    inputs_dict = { "message" : message_api,
                    "section" : section_api,
                    "initialHappinessScore" : initialHappinessScore_api,
                    "finalHappinessScore" : finalHappinessScore_api,
                    "anonymous" : anonymous_api,
                    "conversationId" : conversationId_api,
                    "clientId" : "api"}

    outputs_dict = bot_processing(inputs_dict)


    #_input_api = request.args.get('apiClientData') # this is an array
    #message_api = _input_api[0] # this is a string
    #section_api = _input_api[1] # this is a string

    print("THE INPUTS")
    print("message from api is "+str(message_api))
    print("section number from api is "+str(section_api))
    print("initialHappinessScore from api is "+str(initialHappinessScore_api))
    print("finalHappinessScore from api is "+str(finalHappinessScore_api))
    print("anonConfid from api is "+str(anonymous_api))
    print("conversationId from api is "+str(conversationId_api))

    response_raw = outputs_dict["response"] # type might be either list or string
    next_section = outputs_dict["next_section"]
    #nextUserInput = outputs_dict["nextUserInput"] # don't really need this, because it's got loads of html on it
    nextUserOptions_array = outputs_dict["nextUserOptions"]
    nextUserInputType = outputs_dict["nextUserInputType"]
    anonymous = outputs_dict["anonymous"]
    conversationId = outputs_dict["conversationId"]


    response = "" # not sure if this is stil needed?
    response = convert_array_or_string_to_string(response_raw)

    #nextUserOptions = convert_array_or_string_to_string(nextUserOptions_array) # Wait? I don't think this makes sense?!!!

    print("THE OUTPUTS")
    print("Api outputs; response = "+response)
    print("Api outputs; next_section = "+str(next_section))
    #print("Api outputs; nextUserInput = "+nextUserInput)
    print("Api outputs; nextUserInputType = "+nextUserInputType)
    print("Api outputs; anonymous = "+anonymous)
    print("Api outputs; conversationId = "+conversationId)


    #print("And this is the whole of the _input_api thing: "+ _input_api)
    #_input_api = json.loads('userMessage')
    #botResponse = "This is a dummy bot response for testing purposes. Hello. Now I'm just going to spit out the userMessage thing I've just received: "+str(message_api)+" and this is the current section number: "+str(section_api)
    #response_to_frontend = jsonify({[response, noOfResponseFragments, next_section, score, nextUserInput, nextUserInputType, anonymous, conversationId]})
    return jsonify(response = response, next_section = next_section, nextUserOptions = nextUserOptions_array, nextUserInputType = nextUserInputType, conversationId = conversationId)



if __name__ == "__main__":
    app.run()
