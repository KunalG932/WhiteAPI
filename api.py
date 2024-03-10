from flask import Flask, jsonify, request
import pandas as pd
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

app = Flask(__name__)

# CSS styles
styles = """
<style>
body {
    font-family: Arial, sans-serif;
    margin: 40px;
    background-color: #f9f9f9;
}

.container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

h1 {
    color: #333;
}

p {
    color: #666;
    line-height: 1.5;
}

pre {
    background-color: #f4f4f4;
    padding: 10px;
}
</style>
"""

# Default landing page
@app.route('/')
def landing_page():
    return """
    <html>
    <head>
    <title>White API</title>
    """ + styles + """
    </head>
    <body>
    <div class="container">
        <h1>Welcome to White API</h1>
        <p>This API allows you to fetch news articles from various news sites.</p>
        <p>Usage:</p>
        <ul>
        <li>GET /news?q=search_term&filter=data_filter</li>
        </ul>
        <p>Parameters:</p>
        <ul>
        <li>q (required): Search term</li>
        <li>filter (optional): Data filter (e.g., today, this_week, this_year, or a specific number of days)</li>
        </ul>
        <p>Example:</p>
        <pre>GET /news?q=technology&filter=this_week</pre>
    </div>
    </body>
    </html>
    """

# Function to generate the URL based on search term and data filter
def clean_url(searched_item, data_filter):
    x = pd.Timestamp.today()
    today = str(x)[:10]
    yesterday = str(x + pd.Timedelta(days=-1))[:10]
    this_week = str(x + pd.Timedelta(days=-7))[:10]
    if data_filter == 'today':
        time_period = 'after%3A' + yesterday
    elif data_filter == 'this_week':
        time_period = 'after%3A'+ this_week + '+before%3A' + today
    elif data_filter == 'this_year':
        time_period = 'after%3A'+str(x.year - 1)
    elif str(data_filter).isdigit():
        temp_time = str(x + pd.Timedelta(days=-int(data_filter)))[:10]
        time_period = 'after%3A'+ temp_time + '+before%3A' + today
    else:
        time_period = ''
    url = f'https://news.google.com/rss/search?q={searched_item}+'+time_period+'&hl=en-US&gl=US&ceid=US%3Aen'
    return url

# Function to fetch news based on search term and data filter
def get_news(search_term, data_filter=None):
    url = clean_url(search_term, data_filter)
    response = requests.get(url)
    root = ET.fromstring(response.text)
    title = [i.text for i in root.findall('.//channel/item/title')]
    link = [i.text for i in root.findall('.//channel/item/link')]
    description = [i.text for i in root.findall('.//channel/item/description')]
    pubDate = [i.text for i in root.findall('.//channel/item/pubDate')]
    source = [i.text for i in root.findall('.//channel/item/source')]
    df = pd.DataFrame({'title': title, 'link': link, 'description': description, 'date': pubDate, 'source': source})
    df.date = pd.to_datetime(df.date, unit='ns')
    
    # Extract image URL from description
    image_urls = []
    for desc in description:
        soup = BeautifulSoup(desc, 'html.parser')
        img_tag = soup.find('img')
        if img_tag:
            image_urls.append(img_tag['src'])
        else:
            image_urls.append(None)
    
    df['image_url'] = image_urls
    return df.to_dict(orient='records')

# Route to fetch all types of news
@app.route('/news', methods=['GET'])
def get_all_news():
    # Get search term and data filter from query parameters
    search_term = request.args.get('q', default='', type=str)
    data_filter = request.args.get('filter', default='', type=str)
    
    # Call get_news function to fetch news
    news = get_news(search_term, data_filter)
    
    # Return the news in JSON format
    return jsonify(news)

if __name__ == '__main__':
    # Run the Flask app in debug mode
    app.run(host='159.223.40.117', port=4040)
