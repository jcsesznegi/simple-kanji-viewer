from elasticsearch import Elasticsearch, exceptions
import time
from flask import Flask, jsonify, request, render_template
import sys
import requests
#import xml.etree.ElementTree as ET
import io, json

es = Elasticsearch(host='es')

app = Flask(__name__)

def load_data_in_es():
    """
        tree = ET.parse('./data/test.xml')
        root = tree.getroot()
    """
    with io.open('./data/test2.json','r',encoding='utf8') as f:
        text = f.read()
        data = json.loads(text)
        print "Loading data in elasticsearch ..."
        for id, character in enumerate(data['kanjidic2']['character']):
            res = es.index(index="kanjidata", doc_type="kanji", id=id, body=character)
        print "Total kanji loaded: ", len(data['kanjidic2']['character'])

def safe_check_index(index, retry=3):
    if not retry:
        print "Out of retries. Bailing out..."
        sys.exit(1)
    try:
        status = es.indices.exists(index)
        return status
    except exceptions.ConnectionError as e:
        print "Unable to connect to ES. Retrying in 5 secs..."
        time.sleep(5)
        safe_check_index(index, retry-1)

def check_and_load_index():
    if not safe_check_index('kanjidata'):
        print "Index not found..."
        load_data_in_es()

###########
### APP ###
###########
@app.route('/')
def index():
    """
    tree = ET.parse('./data/test.xml')
    root = tree.getroot()
    for child in root:
        tag = child.tag
    """
    return render_template('index.html' )

@app.route('/debug')
def test_es():
    resp = {}
    try:
        msg = es.cat.indices()
        resp["msg"] = msg
        resp["status"] = "success"
    except:
        resp["status"] = "failure"
        resp["msg"] = "Unable to reach ES"
    return jsonify(resp)

if __name__ == "__main__":
    check_and_load_index()
    #app.run(debug=True) # for dev
    app.run(host='0.0.0.0') # for prod
