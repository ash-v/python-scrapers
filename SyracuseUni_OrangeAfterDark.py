import requests
from bs4 import BeautifulSoup
from slugify import slugify
import pandas as pd

def SyracuseUni_OrangeAfterDark():
    RESULT = []
    base_url = "https://experience.syracuse.edu/student-activities/orange-after-dark/"

    # We will request to get event list page. It return html page source.
    req = requests.get(base_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.43"
        })
    soup = BeautifulSoup(req.content, "lxml")

    # We extract events to html page
    mainContainer = soup.find("div", "entry-content")

    # It has a split structure with the <hr/> element, That's why we will split <hr/>.
    # The last list element is past events, we don't take it because we don't need it. // str(mainContainer).split("<hr/>")[0:-1]
    for event_box in str(mainContainer).split("<hr/>")[0:-1]:

        #To use the element effectively, I'll convert it back into BeautifulSoup because 'event_box' is string.
        soup = BeautifulSoup(event_box, "lxml")

        # Generraly data
        name = soup.find("h3").text.strip().replace(" Link","")
        try:
            description = soup.find("p").text.strip().replace("\xa0","")
        except:
            description = "Empty"

        sub_data = {
            "name":name,
            "description":description,
            "location":None,
            "date":None,
            "ticket_info":None,
            "time":None
        }
        
        # Data such as location, date, time are in a list. Also there is no id or class name.
        # So we can't get with 'find' or 'findall'. But we can get dynamically.
        listItemBox = soup.find("ul")
        listItems = listItemBox.findAll("li")

        for listItem in listItems:
            try:
                key = listItem.findAll("strong")[-1].text
            except IndexError:
                continue
            value = listItem.text.replace(key, "").strip()

            key = slugify(key.replace(":","")).replace("-","_")
            sub_data[key] = value

        # Main Event Informations
        event_info = {
            "event_url":None,
            "ea_name":sub_data["name"],
            "loc_name":sub_data["location"],
            "loc_address":None,
            "img_key":None,
            "lat":None,
            "lng":None,
            "day_of_event":sub_data["date"],
            "time_of_event":sub_data["time"],
            "frequency":None,
            "start_date":sub_data["date"],
            "end_date":None,
            "event_info_source":base_url,
            "category":None,
            "description":sub_data["description"],
            "state":None,
            "email":None,
            "contact_name":None,
            "contact_phone":None,
            "price":sub_data["ticket_info"],
            "except_for":None,
            "tags":None
        }

        print(event_info)

        RESULT.append(event_info)

        #------- You can write code here ---------#

    df = pd.DataFrame(RESULT)
    df.to_excel("Events.xlsx")

if __name__ == '__main__':
    SyracuseUni_OrangeAfterDark()