from selenium import webdriver
from bs4 import BeautifulSoup
import time, json
from dateutil.parser import parse


def FunknWafflesV2():
    # Create real-time browser
    driverOpts = webdriver.ChromeOptions()
    driverOpts.add_argument("--lang=en-GB")
    driverOpts.add_argument('--ignore-certificate-errors-spki-list')
    driverOpts.add_argument('--ignore-ssl-errors')
    driverOpts.add_argument('--ignore-certificate-errors')
    driverOpts.add_argument("--no-sandbox")
    driverOpts.add_argument("--disable-dev-shm-usage")
    driverOpts.add_argument("--disable-gpu")
    driverOpts.add_argument("--headless")
    driverOpts.add_argument("--window-size=1920,1080")
    driverOpts.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
    driver_path = ".\chromedriver.exe"
    
    browser = webdriver.Chrome(
                               executable_path=driver_path, 
                                       options=driverOpts,)
    
    # Define a list to store all events
    RESULT = []
    
    # Define page number
    pageNumber = 1
    while True:
        
        # Go to the listing url and parse html with BeautifulSoup
        url = "https://www.ticketweb.com/venue/funk-n-waffles-syracuse-ny/437585?page={}".format(pageNumber)
        browser.get(url)
        time.sleep(2)
        soup = BeautifulSoup(browser.page_source, "lxml")
        
        # Extract list container
        listFrame = soup.find("ul", class_="media-list")
        if listFrame:
            
            # Scrape items
            items = listFrame.findAll("li")
            for item in items:
                
                # Scrape event url from item row
                event_url = item.find("a").get("href")
                
                # Go to the event page and parse html with BeautifulSoup 
                browser.get(event_url)
                time.sleep(2)
                pageSoup = BeautifulSoup(browser.page_source, "lxml")
                
                # Scrape description of event
                try:
                    desc  = pageSoup.find("div", class_="editable-content").text.strip()
                except:
                    desc = None
                    
                # Extract page json from html
                jsonData = json.loads(pageSoup.find("script", attrs={"type":"application/ld+json"}).text.strip())
                
                # Extract and normalize start date
                try:
                    start_date = parse(jsonData["startDate"], fuzzy=True)
                    start_day = start_date.strftime("%A")
                    full_start_date = start_date.strftime('%Y-%m-%d %H:%M %p')
                    event_time = start_date.strftime('%H:%M %p')
                except:
                    start_day = full_start_date = event_time = None
                    
                 # Extract and normalize end date
                try:
                    end_date = parse(jsonData["endDate"], fuzzy=True)
                    full_end_date = end_date.strftime('%Y-%m-%d %H:%M %p')
                except:
                    full_end_date = None
                                
                # Main Event Informations
                event_info = {
                    "event_url":event_url,
                    "ea_name":jsonData["name"],
                    "loc_name":"Funk 'n Waffles",
                    "loc_address":"307-13 S Clinton St, Syracuse, NY 13202",
                    "img_key":jsonData["image"].split('/')[-1].split('?')[0] ,
                    "img_url":jsonData["image"],
                    "lat":43.050545,     ## "Funk 'n Waffles" coordinates hard coded
                    "lng":-76.153641,
                    "day_of_event":start_day,
                    "time_of_event":event_time,
                    "frequency":"Adhoc",
                    "start_date":full_start_date,
                    "end_date":full_end_date,
                    "event_info_source":event_url,
                    "category":"Live Music",
                    "description": desc ,
                    "state":"Active",
                    "email":None,
                    "contact_name":None,
                    "contact_phone":None,
                    "price":jsonData["offers"][0]["price"],
                    "except_for":None,
                    "tags":None
                }
                
                # Append event informations
                print(event_info)                        
                RESULT.append(event_info)

        else:
            break
        
        pageNumber+=1
        
    # return list of events
    return RESULT
     

FunknWafflesV2()