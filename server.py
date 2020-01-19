from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def main():
    content_id = request.args.get('id', None)
    if content_id is not None:
        # TODO: Fetch real data from database
        return {
            'Selected': {'id': 10101, 'title': 'Selected Item\'s Title', 'type': 'Movie'},
            'Movies': [{'id': 12345, 'title': 'A Movie Title', 'score': 5}],
            'Games': [{'id': 67890, 'title': 'A Game Title', 'score': 3}],
            'Books': [{'id': 101112, 'title': 'A Book Title', 'score': 1}],
        }
    return render_template('index.html')
