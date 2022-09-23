
import requests
import re
from bs4 import BeautifulSoup
import json

cache = {}
def hashable_cache(f):
    def inner(url, session):
        if url not in cache:
            cache[url] = f(url, session)
        return cache[url]
    return inner

s = requests.Session()
@hashable_cache
def get_first_paragraph(url,s):
    req_wiki = s.get(url)
    soup = BeautifulSoup(req_wiki.text, 'html.parser')
    first_paragraph = ""
    for paragraph in soup.find_all("p"):
        
        if paragraph.find("b"):
            first_paragraph += re.sub("\([^()]*\)", "", paragraph.get_text())
            break
   
    return first_paragraph

def get_leaders():

    print("start of get leaders")
    # Root URL  :
    root_url = 'https://country-leaders.herokuapp.com/'
    
    # Cookie request
    cookie_url = 'https://country-leaders.herokuapp.com/cookie'
    cookies = s.get(cookie_url).cookies
    print("Cookie request done")

    # Countries dictionnary request
    countries_url = 'https://country-leaders.herokuapp.com/countries'
    countries_req = s.get(countries_url, cookies = cookies)    
    countries = countries_req.json()
    print("Countries request dictionnary done")

    # Leaders dict request
    leaders_url = 'https://country-leaders.herokuapp.com/leaders'

    print("Leaders request dict")
    

    leaders_per_country = {}

    
    for country in countries: 
        country_leaders = s.get(leaders_url, params={'country':country}, cookies=cookies)
        leaders_url_req = s.get(leaders_url, cookies = cookies)
        

        if leaders_url_req.status_code == 403:
            cookies = s.get(cookie_url).cookies
            leaders_url_req = s.get(leaders_url, cookies = cookies)
        
        leaders_per_country[country] = country_leaders.json()

        for country_leader in leaders_per_country[country]:
            country_leader['first_paragraph'] = get_first_paragraph(country_leader['wikipedia_url'], s)
    return leaders_per_country
get_leaders()

leaders_per_country = get_leaders()

def save():
    filename = "leaders.json"
    json.dump(leaders_per_country, open(filename, "w"))
save()