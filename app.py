from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

# API URL for fetching books
BOOKS_API_URL = os.getenv("BOOKS_API_URL", "http://default-url.com:5000/books")

@app.route("/", methods=["GET", "POST"])
def search_books():
    books = []  # Store search results
    error_message = None

    if request.method == "POST":
        # Get search input from the form
        genre_query = request.form.get('genre')
        author_query = request.form.get('author')
        title_query = request.form.get('title')

        # Filter out empty fields
        params = {k: v for k, v in {'genre': genre_query, 'author': author_query, 'title': title_query}.items() if v}

        try:
            response = requests.get(BOOKS_API_URL, params=params)
            if response.ok:
                books = response.json() # Get filtered books from API
            else:
                error_message = "Failed to fetch books from the server."
        except requests.exceptions.RequestException as e:
            error_message = f"Connection error: {str(e)}"

    return render_template("index.html", books=books, error_message=error_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
