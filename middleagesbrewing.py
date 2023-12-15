import requests
from bs4 import BeautifulSoup
from datetime import date
from dateutil.parser import parse



def middleagesbrewing():
    # Request to events calendar page
    req_listing = requests.get("https://www.middleagesbrewing.com/events-calendar")
    soup_listing = BeautifulSoup(req_listing.text, "lxml")
    
    frame = soup_listing.find("div", attrs={"id":"wix-events-widget"})
    event_boxs = frame.findAll("li", attrs={"data-hook":"events-card"})
    
    for event_box in event_boxs:
        event_url = event_box.find("a").get("href")
        
        print(event_url)
        
        req = requests.get(event_url)
        soup = BeautifulSoup(req.text, "lxml")
        
        try:
            event_name = soup.find("h1", attrs={"data-hook":"event-title"}).text.strip()
        except AttributeError:
            continue
        
        description = soup.find("p", attrs={"data-hook":"event-description"}).text.strip()
        
        
        # Date Process
        current_year = str(date.today().year)
        full_date = soup.find("p", attrs={"data-hook":"event-full-date"}).text.strip()
        print(full_date)
        
        try:
            event_date, full_time = tuple(full_date.split(", "))
        except:
            event_date, other_event_date, full_time = tuple(full_date.split(", "))
            event_date += other_event_date
            
        start_time, end_time = tuple(full_time.split("–"))
        
        start_date = event_date+", " +current_year
        
        eventDateObj = parse(start_date, fuzzy=True)
        eventDayName = eventDateObj.strftime("%A")
        
        
        # Image extraction
        image_element = soup.find("div", attrs={"data-hook":"event-image"}).find("img")
        event_image = image_element.get("src")
        img_key = event_image.split('/')[-1].split('?')[0] 

        # Main Event Informations
        event_info = {
            "event_url":event_url,
            "ea_name":event_name,
            "loc_name":"MIDDLE AGES BREWING CO",
            "loc_address":"120 Wilkinson St, Syracuse, NY 13204, USA",
            "img_url":event_image,
            "img_key":img_key,
            "lat":"43.0510216981813",
            "lng":"-76.1615369848104",
            "day_of_event":eventDayName,
            "time_of_event":start_time,
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
            "price":None,
            "except_for":None,
            "tags": None
            
        }
        
        print(event_info)
        
        #------- You can write code here ---------#  
        
middleagesbrewing()