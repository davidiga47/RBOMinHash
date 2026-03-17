
from __future__ import annotations
import string
import random
import json

#Given a dictionary d, returns the keys of the top n values
def top_keys(d, n):
    return [k for k, v in sorted(d.items(),
                                 key=lambda x: x[1], reverse=True)[:n]]

#Encodes a list of non-integer values to a list of integer values
def encode_ranking(r, translator, case_sensitive=False):
    res=[]
    for word in r:
        try:
            myint = int(word)
        except ValueError:
            if case_sensitive==False:
                word=word.lower()
            if word not in translator.keys():
                translator[word]=len(translator)+1
            myint=translator[word]
        res.append(myint)
    return res

#Loads all files of a directory into the variable 'rankings', then it encodes them
def load_rankings(directory):
    rankings=dict()
    for file in directory.iterdir():
        if file.is_file():
            file_name=file._str.split("\\")[-1]
            text = file.read_text(encoding="utf-8")
            for sign in string.punctuation:
                text = text.replace(sign, "")
            words=text.split()
            rankings[file_name]=words
    return rankings

#Generates two lists of integers with the desired cardinality of intersection (useful for experiments)
def generate_lists(lists_length, lists_intersection, max_value):
    common = random.sample(range(1, max_value+1), lists_intersection)
    rem1 = random.sample(
        [x for x in range(1, max_value+1) if x not in common], 
        lists_length-lists_intersection
        )
    rem2 = random.sample(
        [x for x in range(1, max_value+1) if x not in common and x not in rem1], 
        lists_length-lists_intersection
        )
    l1 = common + rem1
    l2 = common + rem2
    random.shuffle(l1)
    random.shuffle(l2)
    print(l1)
    print("\n")
    print(l2)
    #print(len(set(l1)&set(l2)))
    
def update_json(file, key, value):
    with open(file) as f:
        data = json.load(f)
    data[key] = value
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

    
