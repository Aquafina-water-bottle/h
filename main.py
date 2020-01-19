import json
import requests

import pymongo
import heapq
from flask import Flask, render_template, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

with open("password.txt") as file:
    _client_password = file.read().strip()
    client = pymongo.MongoClient(_client_password)
    db = client.h
    collection = db.raw


def construct_graph(identifier):
    books = dict()
    movies = dict()
    games = dict()

    for doc in collection.find({'key': identifier}).limit(10): #, "like": 1}):
        user = doc['user']
        for docc in collection.find({'user': user, 'key': {'$ne': identifier}}).limit(100):
            sid = docc['key']
            typ = docc['type']
            if typ == 'Book':
                if sid not in books:
                    books[sid] = -1
                else:
                    books[sid] -= 1
            elif typ == 'Movie':
                if sid not in movies:
                    movies[sid] = -1
                else:
                    movies[sid] -= 1
            elif typ == 'Game':
                if sid not in games:
                    games[sid] = -1
                else:
                    games[sid] -= 1
        
    heap_books = [(str(score), str(ide)) for ide,score in books.items()]
    heap_movies = [(str(score), str(ide)) for ide,score in movies.items()]
    heap_games = [(str(score), str(ide)) for ide,score in games.items()]

    print(heap_movies)
    heapq.heapify(heap_books)
    heapq.heapify(heap_games)
    heapq.heapify(heap_movies)

    recommended_books = heapq.nsmallest(3, heap_books)
    recommended_movies = heapq.nsmallest(3, heap_movies)
    recommended_games = heapq.nsmallest(3, heap_games)

    result_books = []
    result_movies = []
    result_games = []

    for _,ide in recommended_books:
        doc = collection.find_one({'key': ide})
        title = doc['title']
        image = doc['image']
        result_books.append((title, image, ide))

    for _,ide in recommended_movies:
        doc = collection.find_one({'key': ide})
        title = doc['title']
        image = doc['image']
        result_movies.append((title, image, ide))

    for _,ide in recommended_games:
        doc = collection.find_one({'key': ide})
        title = doc['title']
        image = doc['image']
        result_games.append((title, image, ide))

    doc = collection.find_one({'key': identifier})

    if doc is None:
        print("Did not find medium")
        return dict()

    title = doc['title']
    image = doc['image']
    selected = (title, image, ide)

    graph = {
        'name': selected[0],
        'image': selected[1],
        'children': [
            {
                'name': 'Books',
                'children': [
                    {
                        'name': result_books[0][0] if len(result_books) else "",
                        'image': result_books[0][1] if len(result_books) else "",
                        'id': 100
                    },
                    {
                        'name': result_books[1][0] if len(result_books) else "",
                        'image': result_books[1][1] if len(result_books) else "",
                        'id': 100
                    },
                    {
                        'name': result_books[2][0] if len(result_books) else "",
                        'image': result_books[2][1] if len(result_books) else "",
                        'id': 100
                    }
                ]
            },
            {
                'name': 'Movies',
                'children': [
                    {
                        'name': result_movies[0][0] if len(result_movies) else "",
                        'image': result_movies[0][1] if len(result_movies) else "",
                        'id': 100
                    },
                    {
                        'name': result_movies[1][0] if len(result_movies) else "",
                        'image': result_movies[1][1] if len(result_movies) else "",
                        'id': 100
                    },
                    {
                        'name': result_movies[2][0] if len(result_movies) else "",
                        'image': result_movies[2][1] if len(result_movies) else "",
                        'id': 100
                    }
                ]
            },
            {
                'name': 'Games',
                'children': [
                    {
                        'name': result_games[0][0] if len(result_games) else "",
                        'image': result_games[0][1] if len(result_games) else "",
                        'id': 100
                    },
                    {
                        'name': result_games[1][0] if len(result_games) else "",
                        'image': result_games[1][1] if len(result_games) else "",
                        'id': 100
                    },
                    {
                        'name': result_games[2][0] if len(result_games) else "",
                        'image': result_games[2][1] if len(result_games) else "",
                        'id': 100
                    }
                ]
            }
        ]
    }
    return graph


@app.route('/')
def main():
    key = request.args.get('key', None)
    if key is not None:
        print("Fetching suggestions for", key)
        return construct_graph(key)
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

