import requests
from bs4 import BeautifulSoup

def scrape_images(query):
    url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        image_urls = []

        for img in soup.find_all('img'):
            image_url = img.get('src')
            if image_url:
                # Replace 'https:' with 'https:' to ensure full-quality image
                image_urls.append(image_url.replace('https:', 'https:'))

        return image_urls
    else:
        print("Error:", response.status_code)
        return []
