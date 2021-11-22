import flask
import pandas as pd
import numpy as np
import os
import json
from sentence_transformers import SentenceTransformer
import torch

class SentenceEncoder:
    def __init__(self):
        torch.set_num_threads(1)
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        my_file = os.path.join(THIS_FOLDER,'..', 'aidata.json')
        with open(my_file) as f:
            self.dataset = json.load(f)
        model_path = os.path.join(THIS_FOLDER,'../../..','model/all-MiniLM-L6-v2/')
        self.model = SentenceTransformer(model_path)
        self.response = []
        self.repeat = [] # not used anymore, replaced with session['ai_repeat']. Kept for testing reasons
        self.threshold = dict(zip(self.dataset.keys(),[self.dataset[x]['threshold'] for x in self.dataset.keys()]))
        #self.priority = dict(zip(self.dataset.keys(),[self.dataset[x]['priority'] for x in self.dataset.keys()]))
        self.cat_embed ={}

    def embed(self,sentences):
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

    def guse_response(self,cat,repeat):
        print('repeat_early:',repeat)
        compare = [item for item in cat.keys() if item not in repeat]
        priority = dict(zip(compare,[self.dataset[x]['priority'] for x in compare]))
        if len(priority) != 0:
            out_cat = min(priority,key=priority.get)
            print('out_cat:',out_cat)
            repeat.append(out_cat)
            print('repeat:',repeat)
            return out_cat, self.dataset[str(out_cat)]['response']
        else:
            return None, None



if __name__ == '__main__':
    se = SentenceEncoder()
    se.make_cat_embed()
    test = 'my girlfriend hit me and im being abused and im depressed and also Upset. You fucking suck'
    # test = '''A wonderful serenity has taken possession of my entire soul, like these sweet mornings of spring which I enjoy with my whole heart. I am alone, and feel the charm of existence in this spot, which was created for the bliss of souls like mine. I am so happy, my dear friend, so absorbed in the exquisite sense of mere tranquil 
    # existence, that I neglect my talents. I should be incapable of drawing a single stroke at the present moment; and yet I feel that I never was a greater artist than now. When, while the lovely valley teems with vapour around me, and the meridian sun strikes the upper surface of the impenetrable foliage of my trees, and but a few stray 
    # gleams steal into the inner sanctuary, I throw myself down among the tall grass by the trickling stream; and, as I lie close to the earth, a thousand unknown plants are noticed by me: when I hear the buzz of the little world among the stalks, and grow familiar with the countless indescribable forms of the insects and flies, 
    # then I feel the presence of the Almighty, who formed us in his own image, and the breath of that universal love which bears and sustains us, as it floats around us in an eternity of bliss; and then, my friend, when darkness overspreads my eyes, and heaven and earth seem to dwell in my soul and absorb its power, 
    # like the form of a beloved mistress, then I often think with longing, Oh, would I could describe these conceptions, could impress upon paper all that is living so full and warm within me, that it might be the mirror of my soul, as my soul is the mirror of the infinite God! O my friend'''
    out = se.get_cat_no_cut(test)
    cat = out['max_over_thresh']
    print(cat)
    print(se.guse_response(cat,se.repeat))
    #print(len(se.cut_250_word(test.split())))
    #print(se.cut_up_msg3(test,'yo yo yo yo'))

