import openai
import dotenv
import os
dotenv.load_dotenv()

class gpt:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.prompt = '''The following is a conversation with an AI assistant. The assistant is empathetic, patient and professional. Its approach is similar to the UK charity Samaritans. 
        If the AI assistant speaks with someone who is suicidal, the assistant clarifies that they are speaking to a bot, and that the software can't trace their location, and because it doesn't know where the human is, if they need help, they would have to get that help themselves. 
        The AI avoids directing the human to a suicide hotline unless the human explicits asks to speak with a hotline or a human, in which case it informs the user about the existence of the Suicide and Crisis Lifeline on 988 if the human is in the US or Samaritans on 116123 if the human is in the UK. It does not offer to call them for the human. 

        AI: Would you like to start talking about what's on your mind? 
        Human: '''
        self.start_sequence = "\nAI: "
        self.restart_sequence = "\nHuman: "

    def get_response(self,msg):
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=self.prompt + msg + self.start_sequence,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
        )
        return response
