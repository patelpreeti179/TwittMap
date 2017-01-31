from elasticsearch import Elasticsearch
import sys
import logging
from flask import Flask, render_template, json, request

app= Flask(__name__)
application=app
@app.route('/')
def main():
   return render_template('tweetmap.html')
   

@app.route('/tmap',methods=['POST'])
def signUp():
    _name = request.form['inputName']
    logging.basicConfig()
    es = Elasticsearch('YOUR ELASTICSEARCH INSTANCE ADDRESS')
    rs = es.search(index="YOUR INDEX", 
               scroll='100s', 
               search_type='scan', 
               size=1000,
              
               body={
                 "fields" : [ "geo.coordinates"],
                  "query" : {
                    
                     "bool": {
                        "must": [
                           { "match": { "geo.type":  "Point" }},
                           { "match": { "text": _name }}
                           ]
                         }
                   }
               }
   )
    print("%d documents found" % rs['hits']['total'])
    tweets = []
    scroll_size = rs['hits']['total']
    while (scroll_size > 0):
     try:
            scroll_id=rs['_scroll_id']
            rs=es.scroll(scroll_id=scroll_id,scroll='100s')
            tweets+=rs['hits']['hits']
            scroll_size=len(rs['hits']['hits'])
     except:
            break

    geo=[]
    for tweet in tweets:
    	geo += tweet['fields']['geo.coordinates']

    return json.dumps(tweets)
    
    

if __name__ == '__main__':
   app.run(port=5002)
