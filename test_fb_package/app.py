from facebook_scraper import get_posts
from urllib.parse import urlencode

url = 'https://www.facebook.com/events/search?'
params = {'q': 'Syracuse'}
qstr = urlencode(params)

final_url = url + qstr

for post in get_posts(post_urls=["https://www.facebook.com/events/search/?q=syracuse%20Ny"]):
    print(post['text'][:50])