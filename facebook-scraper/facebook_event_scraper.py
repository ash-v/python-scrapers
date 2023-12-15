from selenium import webdriver
import time
from pathlib import Path
from bs4 import BeautifulSoup
import re, json, os
from dateutil.parser import parse

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class FacebookEvent:
    def __init__(self):
        # url is listing page url / Please set filters (time range and location)
        #url = "https://www.facebook.com/events/search?q=rochester&filters=eyJycF9ldmVudHNfbG9jYXRpb246MCI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfbG9jYXRpb25cIixcImFyZ3NcIjpcIjEwNzYxMTI3OTI2MTc1NFwifSIsImZpbHRlcl9ldmVudHNfZGF0ZV9yYW5nZTowIjoie1wibmFtZVwiOlwiZmlsdGVyX2V2ZW50c19kYXRlXCIsXCJhcmdzXCI6XCIyMDIyLTA2LTAzXCJ9IiwiZmlsdGVyX2V2ZW50c19kYXRlX3JhbmdlOjEiOiJ7XCJuYW1lXCI6XCJmaWx0ZXJfZXZlbnRzX2RhdGVcIixcImFyZ3NcIjpcIjIwMjItMDYtMDRcIn0iLCJmaWx0ZXJfZXZlbnRzX2RhdGVfcmFuZ2U6MiI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfZGF0ZVwiLFwiYXJnc1wiOlwiMjAyMi0wNS0zMH4yMDIyLTA2LTA1XCJ9IiwiZmlsdGVyX2V2ZW50c19kYXRlX3JhbmdlOjMiOiJ7XCJuYW1lXCI6XCJmaWx0ZXJfZXZlbnRzX2RhdGVcIixcImFyZ3NcIjpcIjIwMjItMDYtMDR%2BMjAyMi0wNi0wNVwifSIsImZpbHRlcl9ldmVudHNfY2F0ZWdvcnk6MCI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfY2F0ZWdvcnlcIixcImFyZ3NcIjpcIjY2MDAzMjYxNzUzNjM3M1wifSIsImZpbHRlcl9ldmVudHNfY2F0ZWdvcnk6MSI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfY2F0ZWdvcnlcIixcImFyZ3NcIjpcIjExMTYxMTE2NDg1MTU3MjFcIn0ifQ%3D%3D"
        url = "https://www.facebook.com/events/search?q=Syracuse%20NY&filters=eyJmaWx0ZXJfZXZlbnRzX2RhdGVfcmFuZ2U6MCI6IntcIm5hbWVcIjpcImZpbHRlcl9ldmVudHNfZGF0ZVwiLFwiYXJnc1wiOlwiMjAyMi0wNi0yMH4yMDIyLTA2LTI2XCJ9IiwicnBfZXZlbnRzX2xvY2F0aW9uOjAiOiJ7XCJuYW1lXCI6XCJmaWx0ZXJfZXZlbnRzX2xvY2F0aW9uXCIsXCJhcmdzXCI6XCIxMDk3NDg5NzIzNzc4NzBcIn0ifQ%3D%3D"
        self.driverOpts = webdriver.ChromeOptions()
        self.driverOpts.add_argument("--lang=en-GB")
        
        if os.name == 'posix':
            self.driverOpts.add_argument('--ignore-certificate-errors-spki-list')
            self.driverOpts.add_argument('--ignore-ssl-errors')
            self.driverOpts.add_argument('--ignore-certificate-errors')
            self.driverOpts.add_argument("--no-sandbox")
            self.driverOpts.add_argument("--disable-dev-shm-usage")
            self.driverOpts.add_argument("--disable-gpu")
            self.driverOpts.add_argument("--headless")
            self.driverOpts.add_argument("--window-size=1920,1080")
            self.driver_path = "./chromedriver"
            
        elif os.name == 'nt':
            self.driverOpts.add_argument("--no-sandbox")
            self.driverOpts.add_argument("--disable-dev-shm-usage")
            self.driverOpts.add_argument("--disable-gpu")
            #self.driverOpts.add_argument("--headless")
            self.driver_path = Path("chromedriver.exe")
            
        self.driverOpts.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            
        print("Starting webdriver")
        self.driver = webdriver.Chrome(executable_path=self.driver_path, 
                                       chrome_options=self.driverOpts)
        
        
        self.driver.get(url)
        time.sleep(2)
        
        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
                            
        # All events data
        EVENT_DATAS = []

        event_urls = self.getEventUrls()
        print("event_urls size : ", len(event_urls))
        for event_url in event_urls:
            print(event_url)
            
            # We enter the event's page
            self.driver.get(event_url)
            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, "lxml")
            scripts = soup.findAll("script")
            
            # Getting scripts from html page source code
            for script in scripts:
                if "event_privacy_info" in str(script):
                    data = re.findall(r'adp_PublicEventCometAboutRootQueryRelayPreloader_.*?",(.*\})]\]', str(script),)[0]
                    jsonData = json.loads(data)
                                        
                    date = self.driver.find_element("xpath", "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div[1]/span").text
                    eventDateObj = parse(date.split(" – ")[0], fuzzy=True)
                    eventDayName = eventDateObj.strftime("%A")
                    
                    try:
                        event_image = self.driver.find_element("xpath","//img[@data-imgperflogname='profileCoverPhoto']").get_attribute("src")
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

                    EVENT_DATAS.append(event_info)

        print(EVENT_DATAS)
        
        # with open('data.json', 'w', encoding='utf-8') as f:
        #     json.dump(EVENT_DATAS, f, ensure_ascii=False, indent=4)

    def getEventUrls(self):
        # Getting event's url from listing page
        with open("currentPage.html", "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)
        urls = []
        item_index = 1
        while True:
            #try:
            url = WebDriverWait(self.driver, 50).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[{}]/a/div[1]/div/div/div/div/div[2]/div[1]/div/div/div/div[2]/span/span/object/a".format(item_index)))).get_attribute("href")
            urls.append(url)
            item_index+=1
            # except:
            #     break
                        
                   
        return urls


if __name__ == "__main__":
    FacebookEvent()
