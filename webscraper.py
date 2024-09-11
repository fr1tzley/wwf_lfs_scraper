import urllib.request,sys,time
from urllib.request import build_opener, HTTPCookieProcessor
import requests
import pandas as pd
import random 
from bs4 import BeautifulSoup as Soup
from itertools import product
from pprint import pprint
import re
from datetime import datetime, timedelta
import random
import webbrowser
import os
from newspaper import Article
from newspaper import fulltext
#from extractnet import Extractor
import joblib
from geopy.geocoders import Nominatim
import numpy as np
import openai 
from pathlib import Path
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
import time
import concurrent.futures


from keywords import build_keywords
##from locate import get_coords
from locate import get_coords
from messages import CLASSIFY_MSG, classify_model, date_event_model, location_model
from querying_classify import get_classify
from querying_date import get_date
from querying_death_injury import get_death_elephant, get_death_human, get_injury_elephant, get_injury_human
from querying_location import get_loc
from sql import add_row, check_date
from temperature_data import get_lat_lon, get_temp_data

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

#date_today = datetime.datetime.now()
locator = Nominatim(user_agent="scraper_geocoder")
##earch_api_key = "AIzaSyDwRHi8ywb8EK-Sn1eyGpUMf0DRdO-oW_k"
##search_id = "02768c49b8a4b4aaa"

'''
Basic setup function 
'''
def create_workspace(date=(datetime.datetime.now() - timedelta(days=1))):
    global date_today
    date_today = date
    Path(f"data/{date_today:%b-%d-%Y}/html").mkdir(parents=True, exist_ok=True)

# Define the the phrases to be searched on google, the
def random_header():
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47'
        ]
    header = {
        'User-Agent': random.choice(user_agents),
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'Origin': 'https://www.google.com',
        'Connection': 'keep-alive'
        }
    return header

#Modify with appropriate searches
def search_terms():
    animals = ['Elephant', 'Tiger', 'calf']
    action = ['kill', 'dead', 'tusker', 'poacher', 'shot', 'electrocuted', 'tusks', 'injured', 'electrocution', 'poisoned', 'ivory']
    countries = ['Indonesia', 'Sri-lanka', 'Sri lanka', 'India', 'Malaysia', 'Thailand']
    return [' '.join(p) for p in product(animals, action, countries)]

'''
Perform the scraping operations for every language in use. Currently we only use english, but flags can be switched in flags.py to 
use other languages as well.
'''
def google_scrape_language():
    keywords_list = build_keywords()
    df = pd.DataFrame()
    for kw in keywords_list:
        keywords =  [' '.join(p) for p in product(kw.animals, kw.action, kw.countries)]
        scraped = google_scrape(keywords)
        df = pd.concat([df,scraped])
    df.to_excel(f"data/{date_today:%b-%d-%Y}/scraped.xlsx")
    print("success in scrape language")

def waitresponse(req):
    attempts = 0
    error = 0
    while attempts < 10:
        try:
            print("waiting")
            time.sleep(60)
            response = urllib.request.urlopen(req)
            return response
        except urllib.error.HTTPError as e:
            error = e
            print("error")
            attempts += 1
    raise error

'''
Search all of the given search terms and scrape the articles found into a dataframe, then saving it into the relevant directory.
'''
def google_scrape(search_terms):
    dates = []
    titles = []
    sources = []
    articles = []
    links = []
    queries = []
    search_urls = []

    for query in search_terms:
        query = "+".join(query.split(" "))
        datestring = date_today.strftime("%m/%d/%Y")

        # set query for google news tab first page
        # change url so that it only shows english language, currently some other languages appear
        url = f"https://www.google.com/search?q={query}&client=firefox-b-d&tbm=nws&sxsrf=AJOqlzVF2NLV8Y_n4p8BJCy2pKhHkUnuOw:1677835678207&source=lnt&tbs=cdr:1,cd_min:{datestring},cd_max:{datestring}&sa=X&ved=2ahUKEwiM49z8uL_9AhUMHzQIHUj5B_UQpwV6BAgCEBY&biw=1718&bih=1303&dpr=1"
        #print(query)
        #print(url)
        while(url):
            # Requesting page and result
            header = random_header()
            req = urllib.request.Request(url, headers=header)
            try:
                response = urllib.request.urlopen(req)
            except urllib.error.HTTPError as e:
                print("URL:"+url)
                print("Header:"+ str(header))
                response = waitresponse(req)
            page = response.read()
            content = Soup(page, "html.parser")
            content.prettify()
            results = content.find('div', {"id": 'rso'})
            try:
                results = results.find("div" , recursive=False).find("div" , recursive=False).findChildren("div" , recursive=False)
            except:
                print("No results:" + url)
                break
            #results = content.find_all("a",{"jsname" : re.compile(r".*")})[3:-1]
            print(len(results))
            for result in results:
                # Grab relevant information from the search results
                title = result.find("div", {"role" : "heading"}).text.replace("\n","")
                link = result.find("a").get("href")
                article = result.find("div", {"role" : "heading"}).next_sibling.text
                date = result.find("div", {"role" : "heading"}).next_sibling.findNext('div').text
                #hours = re.search(r'^\d+', date).group()
                date = date_today.date()
                source = result.find("div", {"role" : "heading"}).previous_sibling.findNext('span').text

                # Avoid duplicate articles by same queries
                if link not in links:
                    titles.append(title)
                    articles.append(article)
                    links.append(link)
                    dates.append(date)
                    sources.append(source)
                    queries.append(query)
                    search_urls.append(url)

            # Checks if there is a next page of results
            try:
                url = "https://www.google.com" + content.find("a", id="pnnext").get("href")
            except:
                response.close()
                break
            response.close()

    df = pd.DataFrame(data={'Title':titles, 'Date Published': dates, 'Article':articles, 'Source':sources, 'Links':links, 'Query':queries, 'Google URL':search_urls})
    print("Success in individual scrape")
    return df


""" Cases:
Popup
Paywall
Article is in seperate blocks

Issues:
Difference between ' and ’

Assumptions:
soup.title finds the first title element anywhere in the html document
title.string assumes it has only one child node, and that child node is a string
 """
def title_scraper():
    full_title = []
    df = pd.read_excel(f"data/{date_today:%b-%d-%Y}/scraped.xlsx")
    for index, row in df.iterrows():
        try:
            title = row["Title"]
            if title.split()[-1] == "...":
                title = ' '.join(title.split()[:-1])
            url = row["Links"]
            header = random_header()
            page = requests.get(url, headers=header)
            html = page.text
            soup = Soup(html, "html.parser")
            try:
                title = soup.title.string.strip()
            except:
                title = soup.find(text=re.compile(title))
            full_title.append(title)
            page.close()
        except:
            full_title.append("Error")
    df["FullTitle"] = full_title
    df.to_excel(f"data/{date_today:%b-%d-%Y}/titles.xlsx")
    print("Success in title scraper")


'''
Contact a finetuned model and return the content of it's response. No longer used.
'''
def contact_finetuned(content, client, model, msg, replacements):
    completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": msg},
        {"role": "user", "content": content}
        ]
    )
    response = completion.choices[0].message
    print(response)
    return replace(response.content,replacements)


def replace(input, replacements):
    for key in replacements.keys():
        input = input.replace(key, replacements[key])
    return input


'''
Old function for contacting the Assistants API. No longer used.
'''
def contact_assistant(input, client, thread, id, instructions):
    
        message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=input
        )
        timeout = 60
        attempts = 0
        while attempts < 3:

            try:
                start_time = time.time()
                run = client.beta.threads.runs.create(
                    thread_id=thread.id,
                        assistant_id=id,
                    instructions=instructions
                )

                finished = ["completed", "expired", "failed", "cancelling"]
                while run.status not in finished:
                    run = client.beta.threads.runs.retrieve(
                        thread_id=thread.id,
                        run_id=run.id
                    )
                    elapsed_time = time.time() - start_time
    
                    if elapsed_time >= timeout:
                        break

                if run.status == "completed":

                    messages = client.beta.threads.messages.list(
                        thread_id=thread.id
                    ).data

                    content = messages[0].content[0].text.value
                    return content
                else:
                    print(run.status)
                    attempts = attempts + 1
            except Exception as error:
                print(error)
                attempts = attempts + 1
                continue
            
        print("run failed")
        return "error occurred"

def filter():
    openai.api_key = openai_api_key

    df = pd.read_excel(f"data/{date_today:%b-%d-%Y}/titles.xlsx")
    ex_df = pd.read_csv("data\classification validation.csv")
    def filter_title(title):
        try:
            result = get_classify({"FullTitle": title}, ex_df, classify_model, 3)
            return result == "Y"
        except:
            return False
    mask = df["FullTitle"].apply(filter_title)

    newdf = df[mask]
    
    newdf.to_csv(f"data/{date_today:%b-%d-%Y}/filtered-{date_today:%b-%d-%Y}.csv")

    print("Success in filter")

""" Cases:
Popup
Paywall
Article is in seperate blocks

Issues:
Difference between ' and ’
 """
def readability_scraper():
    full_article = []
    df = pd.read_excel("scraped-jan31.xlsx")
    for index, row in df.iterrows():
        url = row.links
        header = random_header()
        page = requests.get(url, headers= header)
        try:
            doc = Document(page.text)
            with open(f"{date_today:%b-%d-%Y}/html/article/"+str(index)+".html", "w") as file:
                file.write(doc.summary())
        except:
            with open(f"{date_today:%b-%d-%Y}/html/article/"+str(index)+".html", "w") as file:
                file.write("""<body id="readabilityBody">
                <center><h1>Characters was not English</h1></center>
                <hr><center>nginx</center>
                </body>""")
        page.close()
    print("Success in readability scraper")

def newspaper_scraper():
    parse = []
    full = []
    directory = f"{date_today:%b-%d-%Y}/html/article/"
    files = os.listdir(f"{date_today:%b-%d-%Y}/html/article/")
    for file in files:
        filename = os.fsdecode(file)
        if filename.endswith(".html"):
            with open(os.path.join("jan31/html/", filename), 'r') as f:
                html_string = f.read()
            try:
                full.append(fulltext(html_string, language="en"))
            except:
                full.append("No xpath")
            continue
        else:
            continue
    article = pd.DataFrame(data={'Text':full})
    article.to_excel(f"{date_today:%b-%d-%Y}/fulltext-{date_today:%b-%d-%Y}.xlsx")
    print("Success in newspaper")
def full_query(article, date_published):

    main_df = pd.read_csv("data\STE HEC - Master 10.0.2 - Elephant Death & Injury(1).csv")
    manual_dates_df = pd.read_csv("manual_dates_with_candidates.csv")[:400]
    human_death_injury_df = pd.read_csv("data\human_deaths_injuries.csv")

    elephant_deaths = get_death_elephant({"Article":article}, main_df)
    elephant_injuries = get_injury_elephant({"Article":article}, main_df)

    human_deaths = get_death_human({"Article":article}, human_death_injury_df)
    human_injuries = get_injury_human({"Article":article}, human_death_injury_df)        

    date = get_date({
        "Article": article,
        "Date Published": date_published
    }, manual_dates_df, date_event_model, 0)

    location_dict = get_loc({
        "Article": article
    }, main_df, location_model, 5)
    

    dict = {}
    dict["death_elephant"] = elephant_deaths
    dict["death_human"] = human_deaths
    dict["injury_elephant"] = elephant_injuries
    dict["injury_human"] = human_injuries
    dict["Date (Event)"] = date

    if date == None:
        print("none date")
    for key in location_dict.keys():
        dict[key] = location_dict[key]
    if "Country" not in location_dict.keys():
        dict["Country"] = None
    if "State" not in location_dict.keys():
        dict["State"] = None
    if "Village/Place" not in location_dict.keys():
        dict["Village/Place"] = None

    return dict
'''
Takes the filtered list of articles and queries OpenAI to fill in the following for each row.
-Human deaths
-Elephant deaths
-Human injuries
-Elephant injures
-Date
-Country, State, Village

The filled-in dataset is then saved to a new CSV file.
'''
def openai_query():
    countries_of_interest = ["India", "Sri Lanka", "Indonesia", "Malaysia", "Thailand"]

    df =  pd.read_csv(f"data/{date_today:%b-%d-%Y}/filtered-{date_today:%b-%d-%Y}.csv")
    
    openai.api_key = openai_api_key

    articles = df["Links"].apply(lambda url: Article(url))
    arts_with_dates = zip(articles, df["Date Published"])
    rows = []

    for article, date in arts_with_dates:
        try:
            article.download()
            article.parse()
            if article.text == '':
                continue
            ret = full_query(article.text, date)
            rows.append(ret)
        except Exception as e:
            print(e)
    df2 = pd.DataFrame(rows)
    df = pd.concat([df,df2], axis=1)
    if len(df) > 0:
        try:
            df = df[df["Country"].isin(countries_of_interest)]
        except:
            df = pd.DataFrame()
    #keys_to_use = list(set(geo_keys) & set(list(df.keys())))
    #df = df.drop_duplicates(keys_to_use)
    df.to_csv(f"data/{date_today:%b-%d-%Y}/openai_{date_today:%b-%d-%Y}.csv")



'''
Using the geokeys found by openai_query, fill in the latitude and longitude of each incident. Then fill in weather data using the coordinates.
'''
def get_coords_weather_webscraper(): 
    df = pd.read_csv(f"data/{date_today:%b-%d-%Y}/openai_{date_today:%b-%d-%Y}.csv")
    if len(df) == 0:
        return
    df[["lat", "lon"]] = df.apply(get_lat_lon, axis=1)
    df = df.apply(get_temp_data, axis=1)
    df.to_csv(f"data/{date_today:%b-%d-%Y}/lonlat_{date_today:%b-%d-%Y}.csv")

def merge_in():
    try:
        df = pd.read_csv(f"data/{date_today:%b-%d-%Y}/lonlat_{date_today:%b-%d-%Y}.csv")
        for index, row in df.iterrows():
            r1 = dict(row)
            r1 = {k:(v if (not pd.isnull(v)) and v != "error" else None) for k,v in r1.items()}
            try:
                add_row(r1)
            except Exception as e:
                print("error adding row")
                print(e)
    except:
        return

if __name__ == "__main__":
    
    for i in range (0,32):
        date = datetime.datetime(2024, 6,1) - timedelta(days=i)
        if check_date(date.strftime("%Y-%m-%d")):
            print("date already ran")
            continue
        print("Working\n")
        create_workspace(date)
        google_scrape_language()
        title_scraper()
        filter()
        #readability_scraper()
        #newspaper_scraper()
        openai_query()
        get_coords_weather_webscraper()
        merge_in()
        #autoupload()
        #train()
        #title_scraper_train()
        #readability_scraper_train()
        #newspaper_scraper_train()
        #train_selenium()
        #openai_query_train()
        #readability_newspaper_soup()