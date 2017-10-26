import sys
import json
import gzip
import unicodedata
import numpy 
import re
import operator
import math

def custom_word_tokenizer(my_string):
    s0= my_string
    s1= re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
    s2= re.sub(r'[;:,!\? \-\$\*\%]+',r' ',s1.lower())
    s3= re.sub(r'\.$',r'',s2)
    s4 = re.sub(r'[\.]+ ',r' ',s3)
    words = s3.split(' ')
    return words

def entropy(distribution):
    e=0.0
    for p in distribution:
        e+=(-1.0)*p*math.log(p)
    return e

fp1=open('stop_words.txt','rt')
stop_words=set()
for line in fp1:
    word=line.rstrip()
    stop_words.add(word)



fp=gzip.open("../reviews_Beauty_5.json.gz")
all_data=[]
reviews_text=[]
products_count={}
only_scores=[]

all_counts={}
words_per_category={}
word_counts={}

for line in fp:


    review_data=json.loads(line)
    review_n=unicodedata.normalize('NFKD',review_data['reviewText']).encode('ascii','ignore')

    words= custom_word_tokenizer(review_n)

    #print words
    #print words_pos
    rating=review_data['overall']
    if not rating in all_counts:
        all_counts[rating]={}
    if not rating in words_per_category:
        words_per_category[rating]=0
    words_per_category[rating]+=1

    for word in words:
        if word in stop_words:
            continue

        if not word in word_counts:
            word_counts[word]=0
        word_counts[word]+=1



        if not word in all_counts[rating]:
            all_counts[rating][word]=0
        all_counts[rating][word]+=1


entropy_dict={}
for word in word_counts:
    if word_counts[word]>200:
        p=[]
        for r in all_counts:
            if word in all_counts[r]:
                p.append(float(all_counts[r][word])/words_per_category[r])
        entropy_dict[word]=entropy(p)

sorted_entropy=sorted(entropy_dict.items(), key=operator.itemgetter(1),reverse=False)
for i in range(30):
    print sorted_entropy[i]

