from flask import Flask, jsonify, request, render_template
import pandas as pd
import xml.etree.ElementTree as ET
import requests
from app.news import get_news, clean_url
from app.images import scrape_images

app = Flask(__name__)

# CSS styles
styles = """
<style>
body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #3498db;
    color: #ecf0f1;
}

.container {
    max-width: 800px;
    margin: 5% auto;
    padding: 20px;
    background-color: #2c3e50;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    animation: fadeIn 1s ease-in-out;
}

h1 {
    color: #3498db;
}

p {
    line-height: 1.6;
}

pre {
    background-color: #34495e;
    padding: 10px;
    color: #ecf0f1;
}

/* Animation keyframes */
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
"""

@app.route('/')
def landing_page():
    return render_template('landing_page.html', styles=styles)

@app.route('/images/<query>', methods=['GET'])
def get_images(query):
    image_urls = scrape_images(query)
    return jsonify({'images': image_urls})

@app.route('/news', methods=['GET'])
def get_all_news():
    search_term = request.args.get('q', default='', type=str)
    data_filter = request.args.get('filter', default='', type=str)

    news = get_news(search_term, data_filter)

    return jsonify(news.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(host='128.199.249.208',port='5000')
