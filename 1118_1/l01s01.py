import sys
import json
import gzip
import unicodedata
import numpy 

fp=gzip.open("../reviews_Beauty_5.json.gz")
all_data=[]
reviews_text=[]
products_count={}
only_scores=[]



for line in fp:
    review_data=json.loads(line)
    review_n=unicodedata.normalize('NFKD',review_data['reviewText']).encode('ascii','ignore')
    asin=review_data['asin']
    if not asin in products_count:
        products_count[asin]=0
    products_count[asin]+=1
    only_scores.append(review_data['overall'])


for asin in products_count:
    print asin, products_count[asin]


print "Average score", numpy.mean(only_scores)




