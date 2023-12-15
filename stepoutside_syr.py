import requests
from bs4 import BeautifulSoup

url = 'https://stepoutside.org/syracuse-ny/events/'

# Send a GET request to the URL and store the response
response = requests.get(url)

# Parse the HTML content of the page with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the div with class 'events-container'
events_container_div = soup.find('div', {'class': 'events-container'})

if events_container_div is not None:
    # Find all the divs with class 'event-list-item'
    event_list_items = events_container_div.find_all('div', {'class': 'event'})

    # Loop through each event item and print the event title and date
    for event in event_list_items:
        event_title = event.find('a', {'class': 'event__title'}).text.strip()
        event_date = event.find('div', {'class': 'event__date'}).text.strip()
        print(f'{event_title} - {event_date}')
else:
    print('Could not find event list on the page.')
