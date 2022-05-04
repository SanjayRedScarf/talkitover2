import flask
#import tensorflow as tf
#import tensorflow_hub as hub
import seaborn as sns
import pandas as pd
import numpy as np
import csv
import operator
import os
import json
from keras import backend as K
from sentence_transformers import SentenceTransformer
import torch

class SentenceEncoder:
    def __init__(self):
        #tf.config.threading.set_intra_op_parallelism_threads(1)
        #os.environ['KERAS_BACKEND'] = 'theano'
        torch.set_num_threads(1)
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER, 'aidata.json')
        with open(my_file) as f:
            self.dataset = json.load(f)
        #module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
        model_path = os.path.join(THIS_FOLDER,'../model/all-MiniLM-L6-v2/')
        #self.model = hub.KerasLayer(module_path,trainable=False)
        self.model = SentenceTransformer(model_path)
        #self.dataset = pd.read_csv(my_file)
        self.response = []
        self.repeat = []
        self.threshold = dict(zip(self.dataset.keys(),[self.dataset[x]['threshold'] for x in self.dataset.keys()]))
        #self.priority = dict(zip(self.dataset.keys(),[self.dataset[x]['priority'] for x in self.dataset.keys()]))
        self.cat_embed ={}
        print('Hi Im new')
        print(self.repeat)

    def embed(self,sentences):
        #return self.model(sentences) # for the tf model
        return self.model.encode(sentences, convert_to_tensor = True) # used for the pytorch version

    def make_cat_embed(self):
            for category in self.dataset.keys():
                self.cat_embed[category]=self.embed(self.dataset[category]['exemplars'])

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

    def cut_250_word(self,msg):
        size = 250
        return [" ".join(msg[pos:pos+size]) for pos in range(0,len(msg),size)]

    def get_cat(self,message):
        all_info = {}
        max_dot_per_cat = {}

        max_dot_substring_dot =0
        max_dot_substring = ''
        max_dot_exemplar = ''
        for category in self.dataset.keys(): # for every category, taken from aidata json
            dot_products = []
            for x,toy in enumerate(self.dataset[category]['exemplars']): # for every exemplar sentence in each category
                cut_up_msg = self.cut_up_msg3(message,toy)
                embeded_msgs = self.embed(cut_up_msg)
                dots = np.inner(embeded_msgs,self.cat_embed[category][x])
                max_loc = np.argmax(dots)
                dot_products.append(dots[max_loc]) # append max for one exemplar out of all the cut ups of user msgs
                if dot_products[-1] > max_dot_substring_dot:
                    max_dot_substring_dot = dot_products[-1]
                    max_dot_substring = cut_up_msg[max_loc]
                    max_dot_exemplar = toy
            max_dot_per_cat[str(category)] = max(dot_products)

        max_compare_thresh = {x:max_dot_per_cat[x] for x in max_dot_per_cat.keys() & self.threshold.keys() if max_dot_per_cat[x] > self.threshold[x]}

        highest_max_score_category = max(max_dot_per_cat,key=max_dot_per_cat.get)

        all_info={"user_msg":message,"max_over_thresh":max_compare_thresh,
                    "max_dot_per_cat":max_dot_per_cat,
                    'highest_max_score_category':highest_max_score_category,
                    'highest_max_cat_dot':max_dot_per_cat[highest_max_score_category],
                    'exemplar_for_max_cat': max_dot_exemplar,
                    'substring_for_max_cat': max_dot_substring}
        print(all_info)
        return all_info

    def get_cat_no_cut(self,message):
        all_info = {}
        max_dot_per_cat = {}

        max_dot_substring_dot =0
        max_dot_substring = ''
        max_dot_exemplar = {}
        if len(message.split())>250:
            embeded_msg = self.embed(self.cut_250_word(message.split()))
        else:
            embeded_msg = self.embed(message)
        for category in self.dataset.keys(): # for every category, taken from aidata json
            dot_products = [] #probably not needed, though maybe for the sentence encoder 250 word limit
            dots = np.inner(embeded_msg,self.cat_embed[category])
            dots = dots.flatten()
            max_loc = np.argmax(dots)
            dot_products.append(dots[max_loc]) # append max for one exemplar out of all the cut ups of user msgs
            max_dot_per_cat[str(category)] = max(dot_products) # I think there is only one max in here 
            max_dot_exemplar[str(category)] = self.dataset[category]['exemplars'][max_loc]
        max_compare_thresh = {x:max_dot_per_cat[x] for x in max_dot_per_cat.keys() & self.threshold.keys() if max_dot_per_cat[x] > self.threshold[x]}

        highest_max_score_category = max(max_dot_per_cat,key=max_dot_per_cat.get)

        all_info={"user_msg":message,"max_over_thresh":max_compare_thresh,
                    "max_dot_per_cat":max_dot_per_cat,
                    'highest_max_score_category':highest_max_score_category,
                    'highest_max_cat_dot':max_dot_per_cat[highest_max_score_category],
                    'exemplar_for_max_cat': max_dot_exemplar[highest_max_score_category],
                    'substring_for_max_cat': max_dot_substring}
        print(all_info)
        return all_info

    def guse_response(self,cat):
        print('repeat_early:',self.repeat)
        compare = [item for item in cat.keys() if item not in self.repeat]
        priority = dict(zip(compare,[self.dataset[x]['priority'] for x in compare]))
        if len(priority) != 0:
            out_cat = min(priority,key=priority.get)
            print('out_cat:',out_cat)
            self.repeat.append(out_cat)
            print('repeat:',self.repeat)
            return out_cat, self.dataset[str(out_cat)]['response']
        else:
            return None, None



if __name__ == '__main__':
    se = SentenceEncoder()
    se.make_cat_embed()
    cat = se.get_cat('my girlfriend hit me and im being abused and im depressed and also Upset. You fucking suck')['max_over_thresh']
    print(cat)
    print(se.guse_response(cat))