import requests, re
from bs4 import BeautifulSoup


def Everson():
    self.savedEventUrls = []

    # Start from page 0 (first page)
    page = 1
    while True:
        # We will request to get event list page. It return json data. Headers is must
        req = requests.get("https://everson.org/events-list/events-category-events/page/{}/".format(page), headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43"
        })

        soup = BeautifulSoup(req.text, "lxml")

        # We extract events url to list
        event_urls = [event_box.find("a", attrs={"itemprop":"url"}).get("href") for event_box in soup.findAll("div", "list-blog post_content_holder")]
        if event_urls:
            for event_url in event_urls:
                # If we haven't scraped the event previously, we'll scrape.
                if event_url not in self.savedEventUrls:
                    req = requests.get(event_url, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43"
                    })

                    soup = BeautifulSoup(req.text, "lxml")

                    wpb_wrapper = soup.find("div", "wpb_wrapper")
                    full_desc = wpb_wrapper.text.strip()
                    print(full_desc)
                

                    full_start_date = None
                    event_time = None
                    location_name = None
                    ticket_price = None
                    day_of_event = None
                    description = None#wpb_wrapper.findAll("p")[1].text.strip()

            

                    event_name = soup.find("h1", attrs={"itemprop":"name"}).text.strip()
                    event_image_element = soup.find("div", "expo_feat_img").get("style")
                    event_image = re.findall(r'url\((https:.*)\)', event_image_element)[0]
                    
                    categories = [i.get("class")[1] for i in soup.find("div", "iconsbox").findAll("a", attrs={"rel":"tag"})]

                    # Main Event Informations
                    event_info = {
                        
                        "event_url":event_url,
                        "ea_name":event_name,
                        "loc_name":location_name,
                        "loc_address":None,
                        "img_key":event_image,
                        "lat":None,
                        "lng":None,
                        "day_of_event":day_of_event,
                        "time_of_event":event_time,
                        "frequency":None,
                        "start_date":full_start_date,
                        "end_date":None,
                        "event_info_source":None,
                        "category":categories,
                        "description":description,
                        "state":None,
                        "email":None,
                        "contact_name":None,
                        "contact_phone":None,
                        "price":ticket_price,
                        "except_for":None,
                        "tags":None,
                        "full_desc":full_desc
                    }

                    #------- You can write code here ---------#

                    self.savedEventUrls.append(event_url)
                else:
                    # If we have scraped the event previously, we'll pass.
                    continue
        else:
            # If event_urls is empty so that means we scraped all the events
            # We will break loop
            break

        page+=1

Everson()