import requests
import json

def Alltrails():
    EVENTS = []
    api_endpoint = "https://9ioacg5nhe-dsn.algolia.net/1/indexes/alltrails_index3/query?x-algolia-agent=Algolia%20for%20JavaScript%20(4.8.6)%3B%20Browser"
    cities = {
        31524:"West Lafeyette"
    }
    
    session = requests.session()
    session.headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36 OPR/90.0.4480.84",
        "x-algolia-api-key": "63a3cf94e0042b9c67abf0892fc1d223",
        "x-algolia-application-id": "9IOACG5NHE"
    }
    

    for city_id, city_name in cities.items():
        payload = {"query":"","hitsPerPage":1000,"attributesToRetrieve":["description","ID","_cluster_geoloc","_geoloc","activities","area_id","area_name","area_slug","avg_rating","city_id","city_name","country_id","country_name","created_at","difficulty_rating","duration_minutes","duration_minutes_cycling","duration_minutes_hiking","duration_minutes_mountain_biking","duration_minutes_trail_running","elevation_gain","filters","has_profile_photo","is_closed","is_private_property","length","name","num_photos","num_reviews","photo_count","popularity","profile_photo_data","route_type","slug","state_id","state_name","type","units","user","verified_map_id","visitor_usage","area_name_en-US","area_name_en","city_name_en-US","city_name_en","country_name_en-US","country_name_en","state_name_en-US","state_name_en","name_en-US","name_en","description_en-US","description_en"],"filters":"(city_id={}) AND ((length>=0)) AND ((elevation_gain>=0)) AND type:trail".format(city_id),"attributesToHighlight":[],"responseFields":["hits","hitsPerPage","nbHits"]}
        req = session.post(api_endpoint, json=payload)
        jsonData = json.loads(req.text)
        
        for event in jsonData["hits"]:
            print(event) # Informations of event
            
            EVENTS.append(event)
            
    
    return EVENTS
            

print("start scrapping...")
data = Alltrails()
print("Total Scraped Event Count : {}".format(len(data)))
print("Done scrapping.")
