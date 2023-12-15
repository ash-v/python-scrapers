import requests
import re
import json
from datetime import datetime

def eventbrite_scraper(place_id):
    events = []
    
    # Creating the new session
    session = requests.Session()
    session.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 OPR/89.0.4447.71",
                    "referrer-policy": "strict-origin-when-cross-origin",
                    "Referer": "https://www.eventbrite.com/d/ny--syracuse/all-events/?page=2"}

    # visit the first homepage and adding the cookie and X-CSRFToken to headers
    initial_req = session.get("https://www.eventbrite.com")
    crsf_token = re.findall(r'csrftoken=(.*?)\;', initial_req.headers["set-cookie"])[0]
    session.headers["cookie"] = "csrftoken={};".format(crsf_token)
    session.headers["X-CSRFToken"] = crsf_token
    
    current_page = 1
    while True:
        req = session.post("https://www.eventbrite.com/api/v3/destination/search/",
                            json={"event_search":{"dates":"this_week","dedup":True,"places":[str(place_id)],"page":current_page,"page_size":50,"online_events_only":False,"client_timezone":"America/New_York","include_promoted_events":True},"expand.destination_event":["primary_venue","image","ticket_availability","saves","event_sales_status","primary_organizer","public_collections"]})
        
        jsonData = json.loads(req.text)
        results = jsonData["events"]["results"]
                
        if len(results) >= 1:
            for result in results:  
                keywords_from_json = list(result.keys())
                
                # Preparing the required fields
                event_info = {
                            "event_url":result["url"],
                            "ea_name":result["name"],
                            "loc_name":result["primary_venue"]["name"],
                            "loc_address":result["primary_venue"]["address"]["localized_address_display"],
                            "img_url":result["image"]["url"] if "image" in keywords_from_json else None,
                            "img_key": None, # they create image dynamicly so no exist image name or image file type
                            "lat":result["primary_venue"]["address"]["latitude"],
                            "lng":result["primary_venue"]["address"]["longitude"],
                            "day_of_event":datetime.strptime(result["start_date"], '%Y-%m-%d').strftime("%A"),
                            "time_of_event":result["start_time"],
                            "frequency":None,
                            "start_date":result["start_date"],
                            "end_date":result["end_date"],
                            "event_info_source":result["url"],
                            "category":None,
                            "description":result["summary"],
                            "state":result["primary_venue"]["address"]["region"],
                            "email":None,
                            "contact_name":result["primary_organizer"]["name"],
                            "contact_phone":None,
                            "price":" - ".join([result["ticket_availability"]["minimum_ticket_price"]["display"] if result["ticket_availability"]["minimum_ticket_price"] else "Free", result["ticket_availability"]["maximum_ticket_price"]["display"] if result["ticket_availability"]["maximum_ticket_price"] else "Free"]),
                            "except_for":None,
                            "tags": ", ".join([tag["display_name"] for tag in result["tags"]])
                        }
                
                events.append(event_info)
                
                print(event_info)
            current_page+=1
        else:
            break
    
    return events


all_events = eventbrite_scraper(85941375)

"""
Sample Locations ids
BOSTON : 85950361
Syracuse : 85977785
"""