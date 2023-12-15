from bs4 import BeautifulSoup
import requests
import datetime
import json

def Albany():  
    today = datetime.datetime.today()
    today_str = today.strftime('%Y-%m-%d')
    
    week_ahead = today + datetime.timedelta(days=7)
    week_ahead_str = week_ahead.strftime('%Y-%m-%d')
    
    # We add the event informations in the dictionary structure to this list.
    EVENTS = []
    
    session = requests.session()
    session.headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84"
    }
    
    token = session.get("https://www.albany.org/plugins/core/get_simple_token/").text.strip()
    
   
    api_url = "https://www.albany.org/includes/rest_v2/plugins_events_events_by_date/find/?json=%7B%22filter%22%3A%7B%22categories.catId%22%3A%7B%22%24in%22%3A%5B%2244%22%2C%2211%22%2C%2248%22%2C%2249%22%2C%2214%22%2C%2213%22%2C%225%22%2C%2238%22%2C%224%22%2C%2247%22%2C%2228%22%2C%2216%22%2C%2215%22%2C%2250%22%2C%229%22%2C%226%22%2C%2212%22%2C%2251%22%2C%2246%22%2C%227%22%2C%228%22%2C%2210%22%2C%2245%22%2C%223%22%2C%2240%22%2C%2234%22%5D%7D%2C%22dates.eventDate%22%3A%7B%22%24gte%22%3A%7B%22%24date%22%3A%22{start_date}T00%3A00%3A00-04%3A00%22%7D%2C%22%24lte%22%3A%7B%22%24date%22%3A%22{end_date}T23%3A59%3A59-04%3A00%22%7D%7D%7D%2C%22options%22%3A%7B%22skip%22%3A{skip}%2C%22limit%22%3A50%2C%22hooks%22%3A%5B%22afterFind_listing%22%2C%22afterFind_host%22%5D%2C%22sort%22%3A%7B%22date%22%3A1%2C%22rank%22%3A1%2C%22title%22%3A1%7D%2C%22fields%22%3A%7B%22categories%22%3A1%2C%22endDate%22%3A1%2C%22featured%22%3A1%2C%22host_id%22%3A1%2C%22host.recid%22%3A1%2C%22host.title%22%3A1%2C%22host.detailURL%22%3A1%2C%22latitude%22%3A1%2C%22listing_id%22%3A1%2C%22listing.recid%22%3A1%2C%22listing.title%22%3A1%2C%22listing.detailURL%22%3A1%2C%22listing.address1%22%3A1%2C%22address1%22%3A1%2C%22city%22%3A1%2C%22state%22%3A1%2C%22zip%22%3A1%2C%22location%22%3A1%2C%22longitude%22%3A1%2C%22media_raw%22%3A1%2C%22nextDate%22%3A1%2C%22rank%22%3A1%2C%22recId%22%3A1%2C%22recid%22%3A1%2C%22recurType%22%3A1%2C%22recurrence%22%3A1%2C%22startDate%22%3A1%2C%22title%22%3A1%2C%22typeName%22%3A1%2C%22loc%22%3A1%2C%22url%22%3A1%2C%22date%22%3A1%2C%22email%22%3A1%2C%22linkUrl%22%3A1%2C%22phone%22%3A1%2C%22times%22%3A1%2C%22startTime%22%3A1%2C%22endTime%22%3A1%2C%22admission%22%3A1%7D%2C%22count%22%3Atrue%7D%7D&token={token}"
    
    page = 1
    while True:
        page_offset = (page-1)*50
        
        req = session.get(api_url.format(
                                        start_date=today_str,
                                        end_date=week_ahead_str,
                                        token=token,
                                        skip=page_offset)
                          )
        jsonData = json.loads(req.text) 
               
        if len(jsonData["docs"]["docs"]) >= 1:
            for event_document in jsonData["docs"]["docs"]:
                
                start_date_obj = datetime.datetime.strptime(event_document["startDate"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                if "endDate" in list(event_document.keys()):
                    end_date_obj = datetime.datetime.strptime(event_document["endDate"].split(".")[0],  "%Y-%m-%dT%H:%M:%S")
                else:
                    end_date_obj = None
                
                address = " - ".join([event_document["address1"] if "address1" in list(event_document.keys()) else "",
                                      event_document["city"]if "city" in list(event_document.keys()) else "",
                                      event_document["state"]if "state" in list(event_document.keys()) else "",
                                      event_document["recId"] if "recId" in list(event_document.keys()) else ""])
                
                pageReq =session.get(event_document["absoluteUrl"])
                soup = BeautifulSoup(pageReq.text, "lxml")
                
                event_info = {
                            "event_url":event_document["absoluteUrl"],
                            "ea_name":event_document["title"],
                            "loc_name":event_document["location"] if "location" in list(event_document.keys()) else None,
                            "loc_address":address,
                            "img_url":event_document["media_raw"][0]["mediaurl"] if "media_raw" in list(event_document.keys()) else None,
                            "img_key":event_document["media_raw"][0]["mediaurl"].split("/")[-1] if "media_raw" in list(event_document.keys()) else None,
                            "lat":event_document["loc"]["coordinates"][1] if "loc" in list(event_document.keys()) else None,
                            "lng":event_document["loc"]["coordinates"][0] if "loc" in list(event_document.keys()) else None,
                            "day_of_event":start_date_obj.strftime('%A'),
                            "time_of_event":event_document["startTime"] if "startTime" in list(event_document.keys()) else None,
                            "frequency":"{} - {}".format(event_document["recurrence"], event_document["times"]) if "recurrence" in list(event_document.keys()) and "times" in list(event_document.keys()) else None,
                            "start_date":start_date_obj.strftime("%Y-%m-%d"),
                            "end_date":end_date_obj.strftime("%Y-%m-%d") if end_date_obj else None,
                            "event_info_source":event_document["linkUrl"] if "linkUrl" in list(event_document.keys()) else None,
                            "category":", ".join([category["catName"] for category in event_document["categories"]]),
                            "description": soup.find("div", "content-text").text.strip(),
                            "state":event_document["state"] if "state" in list(event_document.keys()) else None,
                            "email":event_document["email"] if "email" in list(event_document.keys()) else None,
                            "contact_name":None,
                            "contact_phone":event_document["phone"] if "phone" in list(event_document.keys()) else None,
                            "price":event_document["admission"] if "admission" in list(event_document.keys()) else None, 
                            "except_for":None,
                            "tags":None
                        }
                
                print(event_info)
                
                
                EVENTS.append(event_info)
        else:
            break
             
        page+=1
       
    return EVENTS


print("start scrapping...")
events = Albany()
print("Done scrapping.")