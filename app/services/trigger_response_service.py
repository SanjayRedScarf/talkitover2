import random
from repositories import triggers_repository

class TriggerResponseService:

    def get_response_for_trigger(self, user_message, trigger, user_character_count):
        """
        Gets the response for a given trigger.
        """
        response = self.__find_response(user_message, trigger, user_character_count)

        if not response:
            _triggers_repository = triggers_repository.TriggersRepository()

            response = _triggers_repository.get_encouraging_noises_random_response()

        return response


    def __find_response(self, user_message, trigger, user_character_count):
        """
        Finds the response for a given trigger.
        """
        user_is_suicidal = self.__is_user_suicidal(trigger)

        response = ""

        if trigger == "iWantToKillMyself":
            # if the user's message contains some variant of "I want to kill myself"
            response = "Things must be pretty grim if you've got to the stage where you're talking about ending your life like this."

        elif trigger == "imGoingToKillMyself":
            # if the user's message contains some variant of "I'm going to kill myself", then if the user has indicated that they are feeling suicidal
            # then treat the users statement that they will kill themself as a statement of serious suicidal intent.
            # However if it's not accompanied by suicidal language, then it's not so clear, e.g. some users have said things like
            # "i'm going to kill myself with all the alcohol i'm consuming"

            if user_is_suicidal:
                response = "You say that you're going to kill yourself. I'm saddened to hear that. Could you say more about death and what it means for you?"
            else:
                response = "It sounds pretty stark to hear you say that you will kill yourself."

        elif trigger == "iWillDieToday":
            response = "You say you will die today - how do you feel about that?"

        elif trigger == "iWantToDie":
            response = "I'm sorry to hear you say that you want to die."

        elif trigger == "iWantToDieBut":
            response = "It's sad that you want to die, but I'm glad you're still staying alive"

        elif trigger == "imFeelingSuicidal" or trigger == "iveBeenFeelingSuicidal":
            if user_character_count < 1000:
                response = "I'm sorry to hear you mention that you're feeling suicidal. Could we perhaps explore that a bit more?"
            else:
                response = ["I'm sensing you have a lot on your plate at the moment. I just want to pick up on the fact that you just mentioned that you were feeling suicidal. I'm sorry to hear that.",\
                "I can’t stop you from ending your life -- I don’t know where you are and I can’t get help for you. But I can be here to listen to what’s on your mind. Could you tell me more about your feelings?"]

        elif trigger == "iveBecomeSuicidal":
            if user_character_count < 1000:
                response = "I'm sorry to hear you mention these suicidal thoughts. Could you say more about this?"
            elif user_is_suicidal == False:
                response = "I'm sensing there's a lot going on for you, and I'm sorry that it's got to the stage where you've started to feel suicidal."
            else:
                response = "I'm sensing there's a lot going on for you, and I'm sorry to hear about these suicidal feelings you've been mentioning."

        elif trigger == "imFeelingQuiteSuicidal":
            if user_character_count < 1000:
                response = "I'm sorry to hear you mention that you're feeling suicidal. Do you feel this way often?"
            else:
                response = "I'm sensing you have a lot on your plate at the moment. I just want to pick up on the fact that you just mentioned that you were feeling quite suicidal. I'm sorry to hear that. Could you tell me more about those feelings?"

        elif trigger == "suicidalThoughts":
            if len(user_message) < 40:
                response = "I'm sorry to hear that. Could you tell me more about these suicidal thoughts?"
            else:
                response = "You just mentioned suicidal thoughts. If you have anything more to say about that, I'd be happy to hear?"

        elif trigger == "contemplatedSuicideBut":
            response = "It's sad that you've had thoughts of suicide, but I'm glad that you're continuing to stay alive."

        elif trigger == "iWishIWasDead":
            response = "So you're saying you wish you were dead. Which is a pretty drastic thing to wish for."

        elif trigger == "betterOffDead":
            if user_is_suicidal:
                response = "I'm sorry to hear you indicate that you would be better off if you weren't alive."
            else:
                response = ["I'm sorry to hear you indicate that you would be better off if you weren't alive. Could you say more about that?", \
                "And also, if you're feeling suicidal, this is a safe space to share your thoughts about this. And remember that I'm only a simple bot, so I wouldn't be able to get help for you."]

        elif trigger == "iDontWantToLive":
            if user_is_suicidal:
                if user_character_count < 300:
                    response = "I'm hearing loud and clear that you don't want to be alive, and it's really sad that it's got to this. Could you say any more about what's making you feel this way?"
                else:
                    response = "It's sad that you're feeling that you don't want to be alive any more, and that you want to die."
            else: # i.e. if we haven't picked up any other clear indications of suicidality
                if user_character_count < 300:
                    response = "I'm sorry to hear you say that you don't want to live. If you want to explore your thoughts about this, including thinking through any suicidal thoughts you have, feel free to use me as a sounding board"
                else:
                    response = "It's so sad that it's got to the stage where you feel that way about your life."

        elif trigger == "iHateBeingAlive":
            if user_is_suicidal:
                if user_character_count < 300:
                    response = "That's so sad. I'm sorry that you hate being alive and you want your life to end. Could you say any more about what's making you feel this way?"
                else:
                    response = ["I like it when I hear about people loving their lives, and when someone says that they don't like being alive, that's always sad.",\
                    "I'm not in a position to stop you from ending your life -- I don't know where you are and can't get help for you -- but I'm happy to be a space for you to talk about whatever's on your mind."]
            else: # i.e. if we haven't picked up any other clear indications of suicidality
                if user_character_count < 300:
                    response = "I'm sorry to hear you say that you aren't liking being alive. If you want to explore your thoughts about this, including thinking through any suicidal thoughts you have, feel free to use me as a sounding board"
                else:
                    response = "I like it when I hear about people loving their lives, and when someone says that they don't like being alive, that's always sad. All the more so since people who say that can often be suicidal..."

        elif trigger == "shouldIEndIt":
            if user_is_suicidal:
                response = "when you say 'end it', I guess you mean ending your life? In which case, I very much hope you stay alive."
            else:
                response = "when you say 'end it', what would ending it mean to you?"

        elif trigger == "sleepForever":
            response = "From the things you're saying, I can hear the desire to not be alive any more. And I think that's sad."

        elif trigger == "shouldIKillMyself":
            if user_character_count < 300:
                response = "The fact that you are asking this question means that things must be really bad for you. I'm sorry that you're feeling this way. Can you say more about how you're feeling?"
            else: 
                response = "If anyone even thinks about ending their life, then things must be really bad. I'm sorry for your suffering. Can you say more about what you think you should do?"

        elif trigger == "suicideIsOnlyOption":
            response = "It's sad that you seem to think you have no option but to end your life."

        elif trigger == "feelLikeEndingIt":
            response = "If you decided to end your life, that would be very sad."

        elif trigger == "iWasRaped":
            response = ["I'm so sorry you were raped. I can't imagine how you must be feeling now",\
                        "I don't want to interrupt our conversation, but I need you to know that I'm a very simple bot. If you tell me that you're still unsafe, I might not be able to identify that, \
                        and I definitely won't be able to track you down or get help for you, so I'll need you to get help for yourself. But I'm still here to listen..."]

        elif trigger == "physicallyHurtMyself":
            response = "Do you know why you do that"

        elif trigger == "makesMeWantToSelfHarm":
            response = "I'm sorry to hear about these urges to self-harm. What you're going through sounds tough."

        elif trigger == "iHaventSelfHarmed":
            response = "I'm glad you've managed to not self-harm"

        elif trigger == "imCrying":
            response = "I'm sorry to hear that you're feeling this way, and that it's making you cry. That sounds so sad."

        elif trigger == "iWantToCry":
            response = "I guess a good old cry can make you feel better sometimes, but I'm sorry you're in a place where it feels this way for you"

        elif trigger == "nothingToLiveFor":
            if user_is_suicidal:
                response = "It sounds bleak to hear you say you have nothing to live for, and I find it sad that you've been expressing suicidal thoughts."
            else:
                response = "I'm sorry to hear you say that you have nothing to live for. You saying that makes me worry about \
                you, especially when people who say that so often have suicidal thoughts. Could you say more about what's on your mind?"

        elif trigger == "iHateMyself":
            if user_character_count < 1000:
                response = "I think it's really sad to hear you say that you hate yourself. Could you say a bit more about why you have this low self-esteem?"
            else:
                response = "I think it's really sad to hear you say that you hate yourself."

        elif trigger == "singleWordDepressionMessage" and user_character_count < 40:
            response = "OK, so I see you have depression on your mind. Are you feeling depressed? Maybe you could share a bit more about this with me?"

        elif trigger == "feelingDepressed":
            response = "Sorry to hear you're feeling depressed. Would you like to tell me more about that?"

        elif trigger == "treatDepression":
            response =  ["It sounds like you might be suffering from depression - sorry to hear that, I'm happy to hear about how you're feeling if you like?",\
                        "Before you go on I should mention that I'm a pretty simple bot -- don't expect me to be an expert on how to treat depression, but let's talk about it and maybe we can find a way forward together?"]

        elif trigger == "iHaveDepression":
            if len(user_message) > 200:
                response = "Sorry about all that's going on for you, and about your depression."
            else:
                response = "Sorry to hear that you have depression."
            if user_character_count < 1000:
                response = response + " Could you tell me more about that?"

        elif trigger == "iMightHaveDepression":
            if user_character_count < 1000:
                response = "If it feels like you might have depression, things are probably tough for you. Sorry about that. I'm no diagnosis bot, but talking it through with me might help?"
            else:
                response = " If it feels like you might have depression, things are probably tough for you. Sorry about that."

        elif trigger == "iHaveBeenDepressed":
            if user_character_count < 300:
                response = "I'm sorry to hear about the depressed feelings you've been having. Would you like to say more about those?"
            else:
                response = "So I'm hearing you have been depressed and I'm guessing you still are depressed now. I'm sorry to hear that."

        elif trigger == "iHaveNoWayOut":
            response = "I heard you mentioned that you feel you have no way out. Do you feel trapped?"

        elif trigger == "hadEnoughOfLife":
            if user_is_suicidal:
                response = "So I've heard you say that you're feeling suicidal, and you're saying that you've had enough of life. I'm sorry it's got to the stage where you're feeling this way."
            else:
                response = "I'm sorry to hear you say that you've had enough of life. Sometimes when people say that they are also having suicidal thoughts..."

        elif trigger == "iWantToGiveUpOnLife":
            response = "I'm sorry to hear you say that. I'd like to believe that everyone has a reason to live, but I don't know your life, so I can't know what it's like for you"

        elif trigger == "nothingToLookForwardTo":
            response = "It sounds quite bleak to hear you say that you have nothing to look forward to"

        elif trigger == "theOnlyReasonIHaventKilledMyself":
            response = "I'm sensing how close you are to being suicidal"

        elif trigger == "iKeepGettingHorribleThoughts":
            if user_character_count < 300:
                response = "Those thoughts sound unpleasant. Would you like to say more about those?"
            else:
                response = "I'm sorry to hear about the horrible thoughts"

        elif trigger == "iDontTrustAnyone":
            response = "Not being able to trust anyone sounds tough. And lonely..."

        elif trigger == "imUseless":
            if user_character_count < 1000:
                response = "I just heard you mention that you're useless. I'd just like to say that everyone is valuable, including you. Could you say more about what's making you say this?"
            else:
                response = "I just heard you mention that you're useless. I'd just like to say that everyone is valuable, including you."

        elif trigger == "imWorthless":
            if user_character_count < 1000:
                response = "I'm sorry to hear you say that you're worthless. Could you say more about what's on your mind?"
            else:
                response = "I'm sorry to hear you say that you're worthless. You might want to place a bit less value on what I'm going to say now, because (a) I don't know you and (b) I'm really only a very unintelligent bot that doesn't understand everything, but I don't think you're worthless. For what it's worth."

        elif trigger == "imNotLoved":
            response = "Being loved is important for everyone. I'm sorry that's not happening for you now"

        elif trigger == "imNotSpecialToAnyone":
            response = "That's sad. Everyone should feel like they're special to someone"

        elif trigger == "imMakingPeopleUpset":
            response = "It sounds difficult and maybe also lonely, knowing that you've caused hurt to others"

        elif trigger == "iWantSomeoneToLoveMe":
            response = "Feeling loved is important, and I'm sure it's something that everyone wants."

        elif trigger == "iFeelStupidForHavingTheseFeelings":
            response = "It's a shame you feel that way about your feelings -- I think you're entitled to feel whatever you're feeling"

        elif trigger == "feelingLonely":
            feeling_lonely_response_ending = ""

            if user_character_count < 500:
                feeling_lonely_response_ending = ". Can you tell me more about this?"
            else:
                feeling_lonely_response_ending = "."
            response = "Feeling connected to other people is such a fundamental human need. It's sad to hear you talk about this loneliness" + feeling_lonely_response_ending

        elif trigger == "nobodyUnderstandsMe":
            response = "It's not nice to feel misunderstood."

        elif trigger == "imSickOfLockdown":
            response = "I'm not following the latest on coronavirus (I'm far too simple a bot for that!) but do feel free to tell me your feelings about lockdown."

        elif trigger == "iDontSleep":
            response = "Sleep is important. How are you feeling now?"

        elif trigger == "dontHaveAnyoneICanTalkTo":
            response = "It's a shame that you feel you don't have anyone you can talk to. It sounds really isolating."

        elif trigger == "iDontHaveGoodRelationshipsWithAnybody":
            response = "Not having good relationships with anyone sounds hard. And lonely."

        elif trigger == "iStruggleToMakeConversation":
            response = "Is there anything more you'd like to tell me about conversations?"

        elif trigger == "iHateHowILook":
            response = "That sounds really tough. Could you say more about your thoughts on your looks?"

        elif trigger == "imFeelingFat":
            response = "Would you like to tell me more about feeling fat?"

        elif trigger == "loseWeight":
            if trigger == "iHateHowILook":
                response = "I would love it if we lived in a world where being larger didn't make people judge you, \
                            and I'm sorry that your size is making you feel bad"
            elif user_character_count < 700:
                response = "I'm sorry to hear about these things relating to your weight. Could we explore those some more?"

            else:
                response = "I'm sorry to hear about these things relating to your weight"

        elif trigger == "feelOverwhelmed":
            if user_character_count < 100:  # if it's early in hte conversation
                response = "There must be a lot going on for you to be feeling overwhelmed like that. Would you like to tell me more?"
            elif user_character_count < 500:
                response = "That sounds like a lot to deal with. I'm sorry it's got to the stage where it's making you feel overwhelmed."
            else: # by this stage (i.e. for a user_character_cout this high) the user has probably explained a lot of what's happened to make them feel overwhelemed
                response = "That all sounds like a lot to deal with. "

        elif trigger == "imTired":
            if user_character_count < 300:
                response = "Sorry to hear you're feeling tired. Would you like to tell me more about what's making you feel this way?"
            else:
                response = "Sorry to hear you're feeling tired."

        elif trigger == "aLotOnMyMind":
            if user_character_count < 1000:  # if it's early in hte conversation
                response = "I'm sensing you've got a lot on your plate, would you like to tell me more?"
            else: # by this stage (i.e. for a user_character_cout this high) the user has probably explained a lot of what's on their mind
                response = "I see you've got a lot on your plate there"

        elif trigger == "feelingAwful":
            response = "I'm sorry to hear you're feeling so awful. If you think sharing more about that with me might help you feel less awful, I'm here to be a space for you to talk."

        elif trigger == "feelLikeCrying":
            response = "Sounds like this is really, really getting you down. Is there more you want to say about this?"

        elif trigger == "imAFailure":
            response = "It's sad to hear you say that about yourself. I'd love to tell you all the reasons why you're actually really awesome, but I don't know you (and I'm only a very simple bot) so I can't do that. But I do think everyone is valuable in their own way."

        elif trigger == "imALetdown":
            response = "Now I'm hearing you call yourself a letdown, and I think that's sad. I'm here to listen to you about that, without judging."

        elif trigger == "letMyselfDown":
            response = "You mentioned feeling that you had let yourself down. I hope you feel able to share with me some more thoughts about that, knowing that this is a place where you can talk without being judged."

        elif trigger == "hardLife":
            response = "I'm sorry life has been so unpleasant to you."

        elif trigger == "iHaveRegrets":
            response = "That sounds sad."

        elif trigger == "underAchieved":
            response = "Hmm. So you don't feel your achievements live up to the expectations you have of yourself?"

        elif trigger == "iDontHaveMotivation":
            response = "Sounds tough, feeling like you don't have enough motivation or drive"

        elif trigger == "hurtsMyFeelings":
            response = "That sounds painful for you."

        elif trigger == "hurtsToKnowThat":
            response = "Thank you for sharing that pain with me. I'm sorry you have to experience it."

        elif trigger == "feelOutOfControl":
            response = "Can you say a bit more about these out of control feelings?"

        elif trigger == "feelLost":
            if len(user_message) < 28: # if the message is about long enough to say "I'm feeling really lost", and not much longer than that:
                response = "You're saying that you're feeling lost, can you say more about that?"
            else:
                response = "That sounds like a very lost, forlorn feeling."

        elif trigger == "feelEmpty":
            response = "Can you expand on that? What do you mean when you talk about this empty feeling?"

        elif trigger == "inABadPlace":
            if user_character_count < 500:
                response = "You said you're in a bad place. Would you like to say more about that?"
            else:
                response = "I'm sorry to hear you say you're in a bad place."

        elif trigger == "imTrapped":
            response = "You say trapped, is there more to say about that?"

        elif trigger == "nobodyCares":
            response = "It sounds like you feel like no one cares. I am sorry. I am here to listen."

        elif trigger == "noOneCaresAboutMe":
            response = "It sounds like you feel like no one cares. I am sorry. I am here to listen."

        elif trigger == "nooneHelpsMeFeelBetter":
            response = "If there were someone who could help you feel better, what would they do?"

        elif (" i deserve" in user_message.lower() or user_message.lower()[:9] == "i deserve"):
            ### This is a bit of a risky one. However at time of writing, whenever I've seen a user write "i deserve",
            ### it's always been in a negative sense (e.g. "I deserve this suffering") and never (e.g.) "i deserve better"
            ### However if someone did write "i deserve better", I still think this response is ok
            ### Note the logic in hte if statement: if the message contains " i deserve" (starting with a space character)
            ### or if it starts with "i deserve". This means that a string like "naomi deserves" wouldn't trigger this reply
            response = "I just want to take a moment to assert that you are a valuable human being in your right, \
            no matter what"

        elif trigger == "iHateHowIFeel":
            if user_character_count < 300: # if it's early in the conversation
                response = "I'm sorry to hear you say that you hate how you feel. Could you say more about these feelings?"
            else:
                response = "I'm sorry to hear you say that you hate how you feel."

        elif trigger == "imSad":
            response = "Thank you for sharing with me the sadness you're experiencing."

        elif trigger == "feelingLowDownTerrible":
            response = "Sorry to hear you're feeling low."

        elif trigger == "iWantThisFeelingToGoAway":
            response = ":-( I wish you didn't have to feel like this either"

        elif trigger == "imUpset":
            response = "Sorry that you're upset. Could you say a bit more about that?"

        elif trigger == "hurtFeelings":
            response = "Sorry to hear about this, and sorry that it's been hurting your feelings."

        elif trigger == "beingBullied":
            response = "Sorry to hear about you being bullied, that can be really rough."

        elif trigger == "iFeelHelpless":
            response = "I'm sorry to hear about the helplessness you're experiencing"

        elif trigger == "imAddicted":
            response = "Addictions can be really tough. Could you say more about what it means for you?"

        elif trigger == "iHateCoronavirus":
            response = "This nasty virus has caused so many problems."

        elif trigger == "feelingRubbish":
            response = "Sorry that you're feeling rubbish. Could you say a bit more about that?"

        elif trigger == "panicAttacks":
            response = "I am sorry to hear you keep getting panic attacks. How have you coped with them?"

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


        elif trigger == "imWorried":
            ### If the message includes a string roughly equivalent to saying "I'm worried"
            ### This rule covers 2 scenarios: either we're early in the converation or not so early
            ### If we're early, then second_imWorriedResponseAlreadyUsed can't be true for this conversation,
            ### so the if statement above just refers to second_imWorriedResponseAlreadyUsed only

            if user_character_count < 100: # if its early in the conversation
                response = "Can you tell me more about what you're worried about?"
            else:   # if it's not that early in the conversation
                response = "I'm sorry to hear about these worries you're experiencing"

        elif trigger == "iDontKnowWhatToDo":
            response = "So you said you're not sure what to do. Can you think of any options that you would like to explore with me?"

        elif trigger == "whatToDoWithMyself":
            response = "You don't know what to do with yourself? Can you think of anything you would like to do?"

        elif trigger == "iDontKnowWhatToSay":
            ### Note that if the user keeps on saying that they don't konw what to say, they risk getting a very repetitive response,
            ### But at least it will be a resposne which acknowledges that it's being repetitive
            if user_character_count < 200:
                possible_responses = ["This is a space for you to talk about what you're feeling. I'm guessing if you've ended up \
                    at this site you're feeling low. Would you like to say more about that?", "Sorry if it sounds like I'm repeating myself, but this is a space for you to explore whatever's on \
                    your mind. Would you like to tell me a bit about how you're feeling?"]

                response = random.choice(possible_responses)
            else:
                response = ["Thank you for having shared the things you've shared thus far. Perhaps let's just pause for a moment \
                    and think about how you're feeling right now. ", "Having thought about that for a moment, can you think of anything \
                    that's on your mind that would be useful to discuss, and that you haven't already said? If not, perhaps just say 'stop' and provide your feedback?"]

        elif trigger == "personalHygiene" or trigger == "iSmell":
            response = "I understand this hygiene stuff is a thing for humans, I am just a little bot. What are your thoughts on how to respond to this?"

        elif trigger == "wantToBeHappy":
            response = "I would like you to feel happy again too. Can you share a bit about what would make you happy again?"

        elif trigger == "iFeelStuck":
            response = "That sounds difficult for you. I'm sorry you're stuck just now"

        elif trigger == "imNotHappy":
            response = "You said that you're not feeling happy. That's sad. "

        elif trigger == "iStruggleToBeHappy":
            response = "Happiness is so important. I'm sorry to hear happiness seems elusive for you."

        elif trigger == "iFeelNumb":
            response = "Well done for acknowledging how you are feeling - even if you are not feeling anything or are feeling numb."

        elif trigger == "imNotSureWhereToTurn":
            response = "It can be hard when you don't know where to turn"

        elif trigger == "abandonedMe":
            if user_character_count < 1000: # if it's early in the conversation
                response = "Can you say more about being abandoned?"
            else:
                response = "Thank you for letting me know about this abandonment that you're experiencing"

        elif trigger == "imStuckAtHome":
            response = "Sorry to hear you're stuck at home."

        elif trigger == "waitingToSeeIfPoliceAreGoingToChargeMeWithAnOffence":
            response = "Sounds like a tough time for you"

        elif trigger == "imHomeless":
            response = "Being homeless sounds tough"

        elif trigger == "iHaventSeenMyKids":
            response = "Tell me more about what it's like for you, not seeing your children"

        elif trigger == "difficultDay":
            response = "Could you tell me more about the difficult day you've been having?"

        elif trigger == "imPregnant":
            response = "Wow. That sounds like it's probably a pretty big deal. How are you feeling about that?"

        elif trigger == "imBeingTakenForGranted":
            response = "It's only fair for you to be appreciated and valued appropriately"

        elif trigger == "itsStressingMeOut":
            response = "Has this sort of thing always stressed you out?"

        elif trigger == "familyProblems":
            response = "Could you tell me more about these family difficulties?"

        elif trigger == "fallOut":
            response = "You say you have fallen out? It sounds like this is upsetting you?"

        elif trigger == "iHaveLostMyFriends":
            response = "Losing your friends sounds tough"

        elif trigger == "abuse":
            response = ["You mention abuse. That sounds awful.", "Just so you know, I’m a very simple bot, and if you’re being harmed or abused, \
            I wouldn’t be able to get help for you, you would have to get help for yourself. But I can continue to be here for you and listen to you \
            if you would like to keep talking?"]

        elif trigger == "heartBreak":
            response = "I am sorry to hear about the heartbreak, do you want to talk more about that"

        elif trigger == "iWantAFriend":
            response = "Having a friend is important. I imagine you might be feeling lonely? Please tell me more about it…"

        elif trigger == "iDontSeeManyPeople":
            response = "That sounds lonely."

        elif trigger == "myLifeIsBoring":
            response = "Sorry to hear you're not sounding excited about your life. I'd be happy to hear you say more about your feelings about your life?"

        elif trigger == "help":
            response = "What sort of help would you like? (By the way I'm a pretty simple bot and I'm here to listen)"

        elif trigger == "gotDumped":
            response = "Oh no, I'm sorry, it's really awful when a relationship ends."

        elif trigger == "brokeUpWithPartner":
            response = "How are you feeling now?"

        elif trigger == "boyfriendsLeftMe":
            if user_character_count < 300:
                response = "Relationships are complex. I'm a pretty simple bot, but if you want to tell me more about it, I'm here to be a space for you to discuss this further."
            else:
                response = "I'm sorry to hear about the end of your relationship."

        elif trigger == "canYouHelp":
            response = "I am trying to help by giving you the space to talk through what's going on for you - I am still a simple little bot."

        elif trigger == "hello":
            response = "Hi! :-) I'm here to listen. Would you like to talk about what's on your mind?"

        elif trigger == "iWantFreedom":
            response = "What does freedom or being free mean to you?"

        elif trigger == "whoCanITalkTo":
            possible_responses = ["You can talk to me if you like, I am Tio, a chatbot.",\
                        "You can talk to me if you would like - I am a bot though. That means I can'give you space and won't judge ( I don't know how to!). \
                        It also means I won't pick up every human nuance. I am still learning….."]

            response = random.choice(possible_responses)

        elif trigger == "howAreYou":
            response = "I am ok thanks - let's talk about you, how are you?"

        elif trigger == "whatDoYouThink":
            response = "I am a little bot, to be honest, I don't really think in the way you are able to. \
                I can give you space to explore how you are feeling without any judgement."

        elif trigger == "freedom":
            response = "What does freedom or being free mean to you?"

        elif trigger == "doYouGiveAdvice":
            possible_responses = [["This bot is a safe, non-judgemental space to explore what's on your mind. Giving advice isn't part of \
            what I offer. ", "Some people prefer not to be advised -- being told what to do can be disempowering, and talking \
            things through can help. But if advice is what you're after then I'm sorry not to be able to help. Would \
            you like to talk about what's on your mind?"], "This bot isn't about me advising you; it's about you talking and finding your own way through things. You're welcome to continue talking if that would help?"]
            
            response = random.choice(possible_responses)

        elif trigger == "speakToAProfessional":
            response = "What sort of help do you need"

        elif trigger == "dontKnow":
            response = "You have said you don't know - I hope that by talking things through you will be able to work out a next step."

        elif trigger == "whatDoYouThink":
            response = "I am a little bot, to be honest, I don't really think in the way you are able to. I can give you space to explore how you are feeling without any judgement."

        elif trigger == "imGoingToGoNow":
            response = "Thanks for talking with me thus far. If you feel you've reached a good point to stop the conversation, please click the stop button or type 'stop' and do the super-quick final feedback question"

        elif trigger == "yourNice":
            response = "Thanks :-) You're nice too"

        elif trigger == "areYouReading":
            response = "I'm paying attention to you as best I can. I'm sorry I'm only a simple bot and can't always understand you as well as I'd like to. Please press on and continue to talk to me if you would find it useful. But if it's not helping, please click the stop button or type 'stop' into the text field and provide feedback so we can make this better for others"

        elif trigger == "lettingMeGetMyThoughtsOutOfMyHead":
            response = "Yes, this is a place where you can express your thoughts. Many people find it helps, and I hope it helps for you too."

        elif trigger == "idkWhatElseToSayToYou":
            response = "This is a place where you can express whatever's on your mind, so if you have things on your minds that you'd like to share with me, I'm here for you"

        elif trigger == "thankYou":
            response = "You're welcome"

        elif " feeling " in user_message.lower():
            response = "Thank you for sharing this. Could you tell me more about your feelings please?"

        elif trigger == "stopSynonyms":
            possible_responses = ["Sorry I'm such a simple bot and I'm not understanding you very well, but \
                are you saying you want to stop using this bot? If so, would you mind clicking on the stop button on the side or typing 'stop' into the text field?",\
                "Thank you. I think you're telling me you want to stop this conversation (sorry if I misunderstood!) If so, could \
                you please click the stop button or type 'stop' into the text field?",\
                "If I'm understanding you right, you're telling me you want to stop now. Please feel free to click the stop button or type 'stop' into the text field, \
                or if you want to continue using this bot, just continue talking", "Are you saying you want to stop using this bot? If so, \
                would you mind clicking on the stop button on the side or type 'stop' into the text field? (or you can just keep talking, of course)", "I think you're telling me \
                you want to stop now (but I could be \
                wrong because I'm a very simple bot). If that's right, could you click the stop button or type 'stop' into the text field?"]
            
            response = random.choice(possible_responses)

        elif trigger == "areYouABot":
            response = "Yes, I'm a bot! Sorry, I should have explained that better earlier. I hope you don't mind. \
                Please feel free to continue talking with me?"

        elif trigger == "willYouConverseWithMe":
            response = "I'm sorry if it doesn't feel like my conversational skills are good enough.\
                        Please feel free to keep talking to me and I'll try to listen as best I can.\
                        And sorry that I'm only a simple bot"

        elif trigger == "thisBotIsBadloose":
            if user_message.isupper(): #if the message is all caps
                messagePrefix = "I'm sensing your frustration. "
            else:
                messagePrefix = ""

                response = [messagePrefix+"I'm sorry you're not finding this to be helpful. If you have a better option \
                than this bot, such as calling Samaritans (and you don't mind the queue), or talking to a therapist, please \
                do that. ", "But if that doesn't work for you, you're welcome to try to make this conversation work, by \
                using this as a space to talk. And sorry I'm only a very simple bot. If you choose not to do this, please \
                press the stop button or type 'stop' into the text field and provide feedback so we can make this better for others"]

        elif (" " not in user_message or len(user_message) < 10):
            ### If it's the user's first written response and they've given  (essentially) a one-word message, or maybe something without spaces (e.g. typing gibberish like usanvoiudvuvufdsiudsbca)
            ### When I say one-word message, I mean that either it is short, or something that might be longer but has no space characters (this includes someone typing gibberish)
            response = "I see you've said something very short there, which is cool :-). But feel free to type full sentences if you want. Just write about whatever's on your mind -- I'm here to listen."

        return response

    def __is_user_suicidal(self, trigger):
        """
        Checks if the user is suicidal.
        """

        is_suicidal_triggers_list = ["iWantToKillMyself", "iWantToDie", "imFeelingSuicidal", "imFeelingQuiteSuicidal", "suicidalThoughts", "iveBecomeSuicidal"]

        if trigger in is_suicidal_triggers_list:
            return True
        
        return False