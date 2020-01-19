import json
import requests

from flask import Flask, render_template, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

import time

@app.route('/')
def main():
    
    content_id = request.args.get('key', None)
    
    if content_id is not None:
        # TODO: Fetch real data from database
        time.sleep(5)
        with open("static/graph.json") as file: # Use file to refer to the file object
            data = file.read()
        return data
        # return {
        #     'Selected': {'id': 10101, 'title': 'Selected Item\'s Title', 'type': 'Movie'},
        #     'Movies': [{'id': 12345, 'title': 'A Movie Title', 'score': 5}],
        #     'Games': [{'id': 67890, 'title': 'A Game Title', 'score': 3}],
        #     'Books': [{'id': 101112, 'title': 'A Book Title', 'score': 1}],
        # }
    return render_template('index.html')

@app.route('/api/search')
def search():
    query = request.args.get('query')

    url = "https://tastedive.com/api/autocomplete"

    querystring = {"v":"3","target":"search","q":query}

    response = requests.get(url, params=querystring)

    return json.dumps(response.json()["suggestions"])

@app.route('/api/get_key')
def get_key():
    query = request.args.get('query')

    url = "https://tastedive.com/"

    querystring = {"v":query,"t":"","q":"A"}

    response = requests.get(url,params=querystring)

    return response.url.split("/")[-1]

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)

