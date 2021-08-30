import flask
import tensorflow as tf
import tensorflow_hub as hub
import seaborn as sns
import pandas as pd
import numpy as np
import csv
import operator
import os
import sentencepiece as spm

class SentenceEncoder:
    def __init__(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, 'data.csv')

        with tf.Session() as sess:
            module = hub.Module("https://tfhub.dev/google/universal-sentence-encoder-lite/2")
            spm_path = sess.run(module(signature="spm_path"))
        sp = spm.SentencePieceProcessor()
        sp.Load(spm_path)

        self.model = hub.load(module_url)
        self.dataset = pd.read_csv(my_file)

        


sp = spm.SentencePieceProcessor()
sp.Load(spm_path)
    def embed(self,sentences):
        return self.model(sentences)

    def cut_up_msg3(self,msg,cut_string):
        msg = msg.split()
        cut_string = cut_string.split()
        if len(msg)>=len(cut_string)+3:
            msg_size = len(cut_string)+3
        else:
            msg_size = len(cut_string)+(len(msg)-len(cut_string))
        if len(cut_string) < len(msg):
            return [" ".join(msg[i: j]) for i in range(len(msg)) for j in range(i + 1, len(msg) + 1) if len(msg[i:j]) == msg_size]
        else:
            return [" ".join(msg)]

    def get_cat(self,message):
        threshold = {'Abuse':0.6,'Addiction':0.8,'Anxiety':0.7,'Bullied':0.68,'Complaining about using the bot':0.57,
                'Coronavirus/Lockdown': 0.8,'Depression':0.82,'Empty':0.55,'Family & Relationships':0.58,
                'Hate myself':0.78,'Help':0.72,"I don't know what to do":0.8,'I feel ugly':0.5,'Lonely':0.69,
                'Lost':0.53,'Overwhelmed':0.6,'Self-harm':0.65,'Suicidal':0.8,'Upset':0.7,"Useless/Worthless/Failure":0.65}
    
        all_info = {}
        average_dot_products_per_category = {}
        max_dot_per_cat = {}

        for category in self.dataset.columns[1:]:
            dot_products = []
            dfWithoutNaNs = self.dataset.dropna(subset=[str(category)], inplace=False)
            category_message_embeddings = self.embed(dfWithoutNaNs[str(category)].tolist())

            for x,toy in enumerate(dfWithoutNaNs[str(category)].tolist()):
                embeded_msgs = self.embed(self.cut_up_msg3(message,toy))
                dot_products.append(np.max(np.inner(embeded_msgs,category_message_embeddings[x])))
        
            average_dot_products_per_category[str(category)] = np.average(dot_products)
            max_dot_per_cat[str(category)] = max(dot_products)

        max_compare_thresh = {x:max_dot_per_cat[x] for x in max_dot_per_cat.keys() & threshold.keys() if max_dot_per_cat[x] > threshold[x]}
        avg_compare_thresh = {x:average_dot_products_per_category[x] for x in average_dot_products_per_category.keys() & threshold.keys() if average_dot_products_per_category[x] > threshold[x]}    
        
        highest_average_score_category = max(average_dot_products_per_category, key=average_dot_products_per_category.get)
        highest_max_score_category = max(max_dot_per_cat,key=max_dot_per_cat.get)

        all_info ={"user_msg":message,"max_over_thresh":max_compare_thresh,'avg_over_thresh':avg_compare_thresh,
                    "max_dot_per_cat":max_dot_per_cat,
                    "average_dot_products_per_category":average_dot_products_per_category,
                    'highest_average_score_category':highest_average_score_category,
                    'highest_avg_cat_dot': average_dot_products_per_category[highest_average_score_category],
                    'highest_max_score_category':highest_max_score_category,
                    'highest_max_cat_dot':max_dot_per_cat[highest_max_score_category]}

        return all_info

    def guse_response(self,cat):
        return cat



if __name__ == '__main__':
    se = SentenceEncoder()
    print(se.get_cat('im so mad')['highest_max_score_category'])