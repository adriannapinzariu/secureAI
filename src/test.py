import requests
from bs4 import BeautifulSoup
import urllib

# URL to scrape
url = 'https://www.hotels.com'

print(f"Starting to scrape {url}")

# Send a GET request
response = requests.get(url)


if response.status_code == 200:
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    img_tags = soup.find_all('img')
    img_urls = [img['src'] for img in img_tags if 'src' in img.attrs]

    print(f"Found {len(img_urls)} image URLs")