import openai
import dotenv
import os
dotenv.load_dotenv()

class gpt:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.prompt = "This bot is kind and understanding. It answers cautiously in reference to suicide."

    def get_response(self,msg):
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=self.prompt + msg,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\nHuman: ", "\nAI: "]
        )
        return response
