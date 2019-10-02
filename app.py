#import files
from flask import Flask, render_template, request
from chatterbot import ChatBot
#from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer


conversation = ["aaaah ok", "and what does that mean?"]
app = Flask(__name__)
bot = ChatBot("Daniel")
#trainer = ChatterBotCorpusTrainer(bot)
trainer = ListTrainer(bot)
trainer.train(conversation)
#trainer.train('chatterbot.corpus.english')
#bot.train("chatterbot.corpus.english")
my_dict = {}

@app.route("/")
def home():    
    return render_template("home.html") 
@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg')
    response = str(bot.get_response(userText))
    my_dict[userText] = response
    f = open("dict.csv","w")
    f.write( str(my_dict) )
    f.close()
    return response
if __name__ == "__main__":    
    app.run()