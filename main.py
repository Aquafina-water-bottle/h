from flask import Flask, render_template, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
def main():
    
    content_id = request.args.get('id', None)
    if content_id is not None:
        # TODO: Fetch real data from database
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

if __name__ == '__main__':
    app.run('127.0.0.1', port=8080, debug=True)

