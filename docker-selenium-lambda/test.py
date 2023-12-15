from selenium import webdriver
from tempfile import mkdtemp
import json
import time
import re, os
from bs4 import BeautifulSoup
from dateutil.parser import parse
from pathlib import Path
#import boto3
import csv
#import pandas as pd
from io import StringIO 
from datetime import date


def scrape_facebook():
    # driverOpts = webdriver.ChromeOptions()
    # driverOpts.add_argument("--lang=en-GB")

    # if os.name == 'posix':
    #         driverOpts.add_argument('--ignore-certificate-errors-spki-list')
    #         driverOpts.add_argument('--ignore-ssl-errors')
    #         driverOpts.add_argument('--ignore-certificate-errors')
    #         driverOpts.add_argument("--no-sandbox")
    #         driverOpts.add_argument("--disable-dev-shm-usage")
    #         driverOpts.add_argument("--disable-gpu")
    #         driverOpts.add_argument("--headless")
    #         driverOpts.add_argument("--window-size=1920,1080")
    #         driver_path = "/usr/local/bin/chromedriver"
            
    #     elif os.name == 'nt':
    #         driverOpts.add_argument("--no-sandbox")
    #         driverOpts.add_argument("--disable-dev-shm-usage")
    #         driverOpts.add_argument("--disable-gpu")
    #         #self.driverOpts.add_argument("--headless")
    #         driver_path = Path("chromedriver.exe")




    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
    chrome = webdriver.Chrome("/opt/chromedriver",  options=options)

    # url = "https://www.facebook.com/events/search?q=rochester&filters=eyJycF9ldmVudHNfbG9jYXRpb246MCI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfbG9jYXRpb25cIixcImFyZ3NcIjpcIjEwNzYxMTI3OTI2MTc1NFwifSIsImZpbHRlcl9ldmVudHNfZGF0ZV9yYW5nZTowIjoie1wibmFtZVwiOlwiZmlsdGVyX2V2ZW50c19kYXRlXCIsXCJhcmdzXCI6XCIyMDIyLTA2LTAzXCJ9IiwiZmlsdGVyX2V2ZW50c19kYXRlX3JhbmdlOjEiOiJ7XCJuYW1lXCI6XCJmaWx0ZXJfZXZlbnRzX2RhdGVcIixcImFyZ3NcIjpcIjIwMjItMDYtMDRcIn0iLCJmaWx0ZXJfZXZlbnRzX2RhdGVfcmFuZ2U6MiI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfZGF0ZVwiLFwiYXJnc1wiOlwiMjAyMi0wNS0zMH4yMDIyLTA2LTA1XCJ9IiwiZmlsdGVyX2V2ZW50c19kYXRlX3JhbmdlOjMiOiJ7XCJuYW1lXCI6XCJmaWx0ZXJfZXZlbnRzX2RhdGVcIixcImFyZ3NcIjpcIjIwMjItMDYtMDR%2BMjAyMi0wNi0wNVwifSIsImZpbHRlcl9ldmVudHNfY2F0ZWdvcnk6MCI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfY2F0ZWdvcnlcIixcImFyZ3NcIjpcIjY2MDAzMjYxNzUzNjM3M1wifSIsImZpbHRlcl9ldmVudHNfY2F0ZWdvcnk6MSI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfY2F0ZWdvcnlcIixcImFyZ3NcIjpcIjExMTYxMTE2NDg1MTU3MjFcIn0ifQ%3D%3D"
    url = "https://www.facebook.com/events/search?q=Syracuse%20NY&filters=eyJmaWx0ZXJfZXZlbnRzX2RhdGVfcmFuZ2U6MCI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfZGF0ZVwiLFwiYXJnc1wiOlwiMjAyMi0wNi0yMH4yMDIyLTA2LTI2XCJ9IiwicnBfZXZlbnRzX2xvY2F0aW9uOjAiOiJ7XCJuYW1lXCI6XCJmaWx0ZXJfZXZlbnRzX2xvY2F0aW9uXCIsXCJhcmdzXCI6XCIxMDk3NDg5NzIzNzc4NzBcIn0ifQ%3D%3D"
    chrome.get(url)

   

    time.sleep(2)
    SCROLL_PAUSE_TIME = 3

    # Get scroll height
    last_height = chrome.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = chrome.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # All events data
    EVENT_DATAS = []
    event_urls = getEventUrls(chrome)

    print(len(event_urls), event_urls)
    for event_url in event_urls:
        print(event_url)
        
        # We enter the event's page
        chrome.get(event_url)
        time.sleep(2)

        soup = BeautifulSoup(chrome.page_source, "lxml")
        scripts = soup.findAll("script")
        
        # Getting scripts from html page source code
        for script in scripts:
            if "event_privacy_info" in str(script):
                data = re.findall(r'adp_PublicEventCometAboutRootQueryRelayPreloader_.*?",(.*\})]\]', str(script),)[0]
                jsonData = json.loads(data)
                                    
                date = soup.find("h2").text.strip()
                eventDateObj = parse(date.split(" – ")[0], fuzzy=True)
                eventDayName = eventDateObj.strftime("%A")
                
                try:
                    event_image = chrome.find_element_by_xpath("//img[@data-imgperflogname='profileCoverPhoto']").get_attribute("src")
                except:
                    event_image = None
                
                try:
                    location_name = jsonData["__bbox"]["result"]["data"]["event"]["event_place"]["name"]
                except:
                    location_name = None 
                    
                try:
                    location_address = jsonData["__bbox"]["result"]["data"]["event"]["event_place"]["contextual_name"]
                except:
                    location_address = None 
                    
                try:
                    lat = jsonData["__bbox"]["result"]["data"]["event"]["event_place"]["location"]["longitude"]
                except:
                    lat = None    
                    
                try:
                    lng = jsonData["__bbox"]["result"]["data"]["event"]["event_place"]["location"]["latitude"]
                except:
                    lng = None  
                    
                try:
                    description = jsonData["__bbox"]["result"]["data"]["event"]["event_description"]["text"]
                except:
                    description = None   
                    
                try:
                    price = re.findall(r'\$(.*?) ',str(description))[0]
                except:
                    price = None   
                    
                try:
                    categories = [category["label"] for category in jsonData["__bbox"]["result"]["data"]["event"]["discovery_categories"]]
                except:
                    categories = None          
                
                event_info = {
                    "event_url":event_url,
                    "ea_name":soup.findAll("h2")[1].text.strip(),
                    "loc_name":location_name,
                    "loc_address":location_address,
                    "img_url":event_image,
                    "img_key":event_image.split('/')[-1] if event_image else None,
                    "lat":lat,  
                    "lng":lng,
                    "day_of_event":eventDayName,
                    "time_of_event":eventDateObj.strftime("%H:%M:%S"),
                    "frequency":None,
                    "start_date":eventDateObj.strftime("%Y-%m-%d %H:%M:%S"),
                    "end_date":None,
                    "event_info_source":None,
                    "category":categories,
                    "description":description,
                    "state":None,
                    "email":None,
                    "contact_name":None,
                    "contact_phone":None,
                    "price":price,
                    "except_for":None,
                    "tags": re.findall(r'#([^ #]+)(?=[ #]|$)', description) # getting hastags from description
                }
                
                print(event_info)
                
    print(len(EVENT_DATAS))
    # bucket = 'peeeq-datalake-raw-zone' 
    # df = pd.DataFrame(EVENT_DATAS)
    
    # df.end_date.fillna(df.start_date, inplace=True)
    # # df['start_date'] = df['start_date'].apply(lambda x: datetime.strptime(str(x + ' 2022'), "%b %d %Y").date())
    # # df['end_date'] = df['end_date'].apply(lambda x: datetime.strptime(str(x + ' 2022'), "%b %d %Y").date())
    # csv_buffer = StringIO() 
    # df.to_csv(csv_buffer)
    # s3_resource = boto3.resource('s3')
    # #today = date.today()
    # object_key = 'syracuse/facebook_syr/2022-06-19/df.csv'  # + str(today) + 
    # s3_resource.Object(bucket, object_key).put(Body=csv_buffer.getvalue())
            

    #return chrome.find_element_by_xpath("//html").text


# def getEventUrls(chrome):
#     # Getting event's url from listing page
#     urls = []
#     item_index = 1
#     while True:
#         try:
#             urls.append(
#                 chrome.find_element_by_xpath(
#                     "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[{}]/a/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/span/span/object/a".format(item_index)
#                 ).get_attribute("href")
#             )
#             item_index+=1
#         except:
#             break
#     return urls

def getEventUrls(chrome):
        # Getting event's url from listing page
        urls = []
        item_index = 1
        while True:
            try:
                url = WebDriverWait(chrome, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[{}]/a/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/span/span/object/a".format(item_index)))).get_attribute("href")

                urls.append(url)
                item_index+=1
            except:
                break
                        
                   
        return urls


# if __name__ == "__main__":
#     scrape_facebook()

def handler(event=None, context=None):
    scrape_facebook()

    body = {
        "message": "Hello, world! Your function executed successfully!",
    }
    return {
        "statusCode": 200,
        "body": json.dumps(body)
    }
