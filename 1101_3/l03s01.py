import sys
import json
import unicodedata
import operator
import math
import gzip
import nltk


fp=open("stop_words.txt","rt")
stop_words=set()
for line in fp:
    stop_words.add(line.rstrip())
print "Loaded stop words"

product_count={}
fp=gzip.open("../reviews_Beauty_5.json.gz")
for line in fp:
    review_data=json.loads(line)
    asin=review_data['asin']
    if not asin in product_count:
        product_count[asin]=0.0
    product_count[asin]+=1.0
print "Number of products", len(product_count)

fp=gzip.open("../reviews_Beauty_5.json.gz")
dictionary_per_product={}
words_per_product={}
master_dictionary={}
for line in fp:
    review_data=json.loads(line)
    asin=review_data['asin']
    if product_count[asin]<40.0:
        continue
    review=unicodedata.normalize('NFKD',review_data['reviewText']).encode('ascii','ignore')
    if not asin in dictionary_per_product:
        dictionary_per_product[asin]={}
        words_per_product[asin]=0.0
    words=nltk.word_tokenize(review)
    for word_r in words:
        word=word_r.lower()
        if not word in stop_words:
            if not word in master_dictionary:
                master_dictionary[word]=0.0
            if not word in dictionary_per_product[asin]:
                dictionary_per_product[asin][word]=0.0
            master_dictionary[word]+=1.0
            dictionary_per_product[asin][word]+=1.0
            words_per_product[asin]+=1.0

top_words={}
InverseDocumentFrequency={}
for asin in dictionary_per_product:
    for word in dictionary_per_product[asin]:
        if not word in InverseDocumentFrequency:
            InverseDocumentFrequency[word]=0.0
        InverseDocumentFrequency[word]+=1.0
for asin in dictionary_per_product:
    top_words[asin]=set()
    for word in dictionary_per_product[asin]:
        if dictionary_per_product[asin][word]>=10.0:
            tf_idf=(float(dictionary_per_product[asin][word])/words_per_product[asin])*math.log(len(dictionary_per_product)/InverseDocumentFrequency[word])
            if tf_idf>=0.0001:
                top_words[asin].add((word,tf_idf))
    print asin, top_words[asin]



