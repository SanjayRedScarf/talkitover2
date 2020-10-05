from models import next_user_option_types

class HtmlHelper:
    def get_next_user_input_options_html(self, client_id, next_user_input_options):
        if client_id == "originalJavascriptClient":
            html = self.__get_original_javascript_client_html(next_user_input_options)
        elif client_id == "bootstrapJavascriptClient":
            html = self.__get_bootstrap_clint_html(next_user_input_options)
        else:
            html = next_user_input_options[0] # in this scenario we're expecting that the client is the API, and therefore won't need any html text
        return html
            

    def __get_original_javascript_client_html(self, next_user_input_options):
        html = ''

        for option in next_user_input_options:
            html += '<button type="button" class = "userButton" id = "userInputButton" value = "'+str(option)+'" onclick="getBotResponse()">'+str(option)+'</button> \n'

        return html

    def __get_bootstrap_clint_html(self, next_user_input_options):
        html = "<select class='message_input' type='text' id='userInputButton'> <option selected disabled>Select</option>"

        for option in next_user_input_options:
            if option != next_user_input_options[-1]:
                html += "<option value='"+str(option)+"'>"+str(option)+"</option> \n"
            else:
                html += "<option value='"+str(option)+"'>"+str(option)+"</option> \n  </select>"

        return html

    def get_next_user_input_option_types_html(self, client_id):
        if client_id == "originalJavascriptClient":
            next_user_input_free_text = "<input id='textInput' type='text' name='msg' placeholder='Type your message here' />" # this is a standard choice of thing to have at the bottom of the chatbox which will allow the user to enter free text
            next_user_input_yes_no = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
            <option>Select</option>  \
            <option value='yes'>Yes</option> \
            <option value='no'>No</option> \
            </select>"
            next_user_input_one_option = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
            <option>Select</option>  \
            <option value='yes'>Yes</option> \
            </select>"
            next_user_input_two_options = "<select type='text' id='userInputButton' onchange='getBotResponse()'> \
            <option>Select</option>  \
            <option value='yes'>Yes</option> \
            <option value='no'>No</option> \
            </select>"
            next_user_input_final_happiness_survey = "<select type='number' id='finalHappinessSurvey' onchange='getBotResponse()' style = 'width:500px;'>\
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
        elif client_id == "bootstrapJavascriptClient":
            next_user_input_free_text = "<input class='message_input' placeholder='Type your message here...'>" # this is a standard choice of thing to have at the bottom of the chatbox which will allow the user to enter free text
            #nextUserInputYesNo = "<select class='message_input' type='text' id='userInputButton' onchange='sendMessage()> \
            next_user_input_yes_no = "<select class='message_input' type='text' id='userInputButton' > \
            <option selected disabled>Select</option>  \
            <option value='yes'>Yes</option> \
            <option value='no'>No</option> \
            </select>"
            #nextUserInputOneOption = "<select class='message_input' type='text' id='userInputButton' onchange='sendMessage()> \
            next_user_input_one_option = "<select class='message_input' type='text' id='userInputButton' > \
            <option selected disabled>Select</option>  \
            <option value='yes'>Yes</option> \
            </select>"
            #nextUserInputTwoOptions = "<select class='message_input' type='text' id='userInputButton' onchange='sendMessage()> \
            next_user_input_two_options = "<select class='message_input' type='text' id='userInputButton' > \
            <option selected disabled>Select</option>  \
            <option value='yes'>Yes</option> \
            <option value='no'>No</option> \
            </select>"
            #nextUserInputFinalHappinessSurvey = "<select class='message_input' type='number' id='finalHappinessSurvey' onchange='sendMessage()'>\
            next_user_input_final_happiness_survey = "<select class='message_input' type='number' id='finalHappinessSurvey' >\
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
            next_user_input_free_text = ""
            next_user_input_yes_no = ""
            next_user_input_one_option = ""
            next_user_input_two_options = ""
            next_user_input_final_happiness_survey = ""

        return next_user_option_types.NextUserOptionTypes(next_user_input_free_text, next_user_input_yes_no, next_user_input_one_option, next_user_input_two_options, next_user_input_final_happiness_survey)
