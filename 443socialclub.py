import requests
from bs4 import BeautifulSoup
from datetime import date
from dateutil.parser import parse

def scrape_443SocailClub():
    page = 1
    while True:
        # Request to events page
        req_listing = requests.get("https://443socialclub.com/events/photo/page/{}/".format(page), headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.60"
        })
        soup_listing = BeautifulSoup(req_listing.text, "lxml")
        
        frame = soup_listing.find("div", "tribe-events-pro-photo")
        
        # if frame is None/Empty break the loop. This means all pages are scraped
        if frame == None:
            break
        
        event_boxs = frame.findAll("article")
        
        for event_box in event_boxs:
            event_url = event_box.find("a").get("href")
        
            print(event_url)
            
            req = requests.get(event_url, headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.60"
            })
            soup = BeautifulSoup(req.text, "lxml")   

            event_name = soup.find("h1", "tribe-events-single-event-title").text.strip()
            description = soup.find("div", "tribe-events-single-event-description tribe-events-content").text.strip()

            
            # Image extraction
            image_element = soup.find("div", "tribe-events-event-image").find("img")
            event_image = image_element.get("src")
            img_key = event_image.split('/')[-1].split('?')[0] 
            
            
            # Date Process
            current_year = str(date.today().year)
            
            event_full_date = soup.find("span", "tribe-event-date-start").text.strip()
            end_time = soup.find("span", "tribe-event-time").text.strip()
            event_date, start_time = tuple(event_full_date.split(" @ "))
            
            start_date = event_date+", " +current_year
            eventDateObj = parse(start_date, fuzzy=True)
            eventDayName = eventDateObj.strftime("%A")

            
            # Main Event Informations
            event_info = {
                "event_url":event_url,
                "ea_name":event_name,
                "loc_name":"443 Social Club & Lounge",
                "loc_address":"443 Burnet Ave, Syracuse, NY 13203",
                "img_url":event_image,
                "img_key":img_key,
                "lat":"43.05246069876397",  
                "lng":"-76.14030750200487",
                "day_of_event":eventDayName,
                "time_of_event":"{} - {}".format(start_time, end_time),
                "frequency":None,
                "start_date":start_date,
                "end_date":event_date,
                "event_info_source":None,
                "category":None,
                "description":description,
                "state":None,
                "email":None,
                "contact_name":None,
                "contact_phone":None,
                "price":"$15 per person/seat min. purchase required",
                "except_for":None,
                "tags": None
                
            }
            
            #------- You can write code here ---------#  

        page+=1
        
scrape_443SocailClub()