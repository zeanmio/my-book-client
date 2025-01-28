from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# URL of Service 1
BOOKS_API_URL = "http://127.0.0.1:5000/books"

@app.route("/books", methods=["GET"])
def search_books():
    genre_query = request.args.get('genre')
    author_query = request.args.get('author')
    title_query = request.args.get('title')
    
    params = {
        'genre': genre_query,
        'author': author_query,
        'title': title_query
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    try:
        response = requests.get(BOOKS_API_URL, params=params)
        if response.ok:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to fetch books from Service 1'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Connection error: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
