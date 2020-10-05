class ResponseFragmentsHelper:
    def get_response_fragments_count(self, response):
        """
        Counts the number of fragments in the response.
        Sometimes the bot response is just one fragment; at other times one fragment will appear and then a typing ellipsis will appear for a moment, and then another fragment.
        """
        noOfResponseFragments = 0
        if isinstance(response,list):
            noOfResponseFragments = len(response)
        elif isinstance(response,str):
            noOfResponseFragments = 1
        else:
            print("Error: expecting the response variable to be either a string or a list, otherwise don't know how to set the noOfResponseFragments variable")
        return noOfResponseFragments