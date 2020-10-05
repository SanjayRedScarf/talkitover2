class StringCleansingService:
    def clean_string(self, message):
        """
        Cleans the user's message to make it suitable for analysing.
        It does this by:
            1. cleans the string so that it only contains alphabetic characters and spaces (everything else is deleted)
            2. removes extraneous words (this results in a list)
            3. turns list back into string
        Cleaning the message makes the system more robust, because we've seen instances of triggers not getting recognised...
        ...we speculate that different treatments of the apostrophe character might be the reason
        """

        extraneous_words_array = ["still", "just", "so", "very", "totally", "utterly", "really", "completely", \
        "literally", "actually", "even", "some", "always", "fucking", "fuckin", "technically", "increasingly", "seriously", "extremely"]
       
        cleaned_message = ["".join(list(filter(str.isalpha, i))) for i in message.split() if i not in extraneous_words_array]

        cleaned_message = ' '.join(cleaned_message)

        return cleaned_message