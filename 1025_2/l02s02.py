import sys
import json
import gzip
import unicodedata
import numpy 
import re
import operator
import nltk


def custom_word_tokenizer(my_string):
    s0= my_string
    s1= re.sub(r'([a-z])\.([A-Z])',r'\1 \2',s0)
    s2= re.sub(r'[;:,!\? \-\$\*\%]+',r' ',s1.lower())
    s3= re.sub(r'\.$',r'',s2)
    s4 = re.sub(r'[\.]+ ',r' ',s3)
    words = s3.split(' ')
    return words



fp1=open('stop_words.txt','rt')
stop_words=set()
for line in fp1:
    word=line.rstrip()
    stop_words.add(word)


max_reviews=10000

fp=gzip.open("../reviews_Beauty_5.json.gz")
all_data=[]
reviews_text=[]
products_count={}
only_scores=[]

all_counts={}
words_per_category={}


for line in fp:

    if max_reviews==0:
        break
    max_reviews-=1

    review_data=json.loads(line)
    review_n=unicodedata.normalize('NFKD',review_data['reviewText']).encode('ascii','ignore')

    #words= custom_word_tokenizer(review_n)
    words= nltk.word_tokenize(review_n)
    words_pos = nltk.pos_tag(words)
    #print words
    #print words_pos
    rating=review_data['overall']
    if not rating in all_counts:
        all_counts[rating]={}
    if not rating in words_per_category:
        words_per_category[rating]=0
    words_per_category[rating]+=1

    for duplet in words_pos:
        word=duplet[0]
        pos=duplet[1]
        if word in stop_words:
            continue

        # At home, please find out what was wrong with my boolean syntax
        # WHYY??? if pos!='NN'  or  pos!='NNS':
        #if pos !='NN':


        # At home focus on JJ_NN

        if pos !='JJ':
            continue
        if not word in all_counts[rating]:
            all_counts[rating][word]=0
        all_counts[rating][word]+=1




for score in all_counts:
    print "SCORE", score
    sortedx=sorted(all_counts[score].items(), key=operator.itemgetter(1),reverse=True)
    probabilities=[(x[0],float(x[1])/words_per_category[score]) for x in sortedx]
    print probabilities[:20]


