import flask
import tensorflow as tf
import tensorflow_hub as hub
import seaborn as sns
import pandas as pd
import numpy as np
import csv
import operator
import os
import json 

class SentenceEncoder:
    def __init__(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, 'aidata.json')
        with open(my_file) as f:
            self.dataset = json.load(f)
        #module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        module_path = os.path.join(THIS_FOLDER,'universal-sentence-encoder_4')
        self.model = hub.load(module_path)
        #self.dataset = pd.read_csv(my_file)
        self.response = []
        self.repeat = []
        self.threshold = dict(zip(self.dataset.keys(),[self.dataset[x]['threshold'] for x in self.dataset.keys()]))
        #self.priority = dict(zip(self.dataset.keys(),[self.dataset[x]['priority'] for x in self.dataset.keys()]))

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
        #threshold = dict(zip(self.dataset.keys(),[self.dataset[x]['threshold'] for x in self.dataset.keys()]))
    
        all_info = {}
        average_dot_products_per_category = {}
        max_dot_per_cat = {}

        for category in self.dataset.keys():
            dot_products = []
            #dfWithoutNaNs = self.dataset.dropna(subset=[str(category)], inplace=False)
            #category_message_embeddings = self.embed(dfWithoutNaNs[str(category)].tolist())
            category_message_embeddings = self.embed(self.dataset[category]['exemplars'])
            for x,toy in enumerate(self.dataset[category]['exemplars']):
                embeded_msgs = self.embed(self.cut_up_msg3(message,toy))
                dot_products.append(np.max(np.inner(embeded_msgs,category_message_embeddings[x])))
        
            average_dot_products_per_category[str(category)] = np.average(dot_products)
            max_dot_per_cat[str(category)] = max(dot_products)

        max_compare_thresh = {x:max_dot_per_cat[x] for x in max_dot_per_cat.keys() & self.threshold.keys() if max_dot_per_cat[x] > self.threshold[x]}
        avg_compare_thresh = {x:average_dot_products_per_category[x] for x in average_dot_products_per_category.keys() & self.threshold.keys() if average_dot_products_per_category[x] > self.threshold[x]}    
        
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
        
        compare = [item for item in cat.keys() if item not in self.repeat]
        priority = dict(zip(compare,[self.dataset[x]['priority'] for x in compare]))
        out_cat = min(priority,key=priority.get)
        
        self.repeat.append(out_cat)
        return self.dataset[str(out_cat)]['response']



if __name__ == '__main__':
    se = SentenceEncoder()
    cat = se.get_cat('my girlfriend hit me and im being abused and im depressed and also Upset. You fucking suck')['max_over_thresh']
    print(cat)
    print(se.guse_response(cat))