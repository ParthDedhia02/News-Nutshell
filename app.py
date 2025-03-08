from flask import Flask, request, jsonify, render_template
from newspaper import Article
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Retrieve API key from .env
API_KEY = os.getenv("NEWSDATA_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    url = request.form.get('url')
    language = request.form.get('language', 'en')

    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()  # Extract summary

        return jsonify({
            'title': article.title,
            'summary': article.summary,
            'publish_date': article.publish_date if article.publish_date else "Unknown",
            'top_image': article.top_image if article.top_image else ""
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/news')
def get_news():
    if not API_KEY:
        return jsonify({'error': 'API key is missing'}), 500

    try:
        url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&country=in&language=en&category=business"
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'Failed to fetch news'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
