class ConversationSectionOneService:
    def get_initial_happiness_score(self, conversation_input_data):
        """
        This method gets the user to input an initial happiness score and returns a response based on the user's input.
        """
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


