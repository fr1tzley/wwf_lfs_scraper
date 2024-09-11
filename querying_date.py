from datetime import datetime
import json
import random
import time
import openai
import pandas as pd
from dateparser.search import search_dates
import spacy

from messages import DATE_LIST_TASK_MSG
from messages import DATE_LIST_INSTRUCTIONS_MSG

nlp = spacy.load("en_core_web_sm")

date_label = ['DATE']

from dotenv import load_dotenv
import os


'''
Used by the webscraper to query the model for the date an article took place.

Firstly, NLP is used on the text of the article to extract every date found within that article. This accounts for situations where several dates are 
mentioned(often including the date of publication)

We then present the article and the list of extracted dates to the model. The model is asked to read the article and list of dates, and pick which
date is the one where the incident of human-elephant conflict took place.
'''


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=openai_api_key)


'''
Take an individual row, and return the list of dates found in that row's article
'''
def get_candidate_dates(row):
    date_label = ['DATE']
    art = row["Article"]
    date_pub = row["Date Published"]
    try:
        pubdate = datetime.strptime(date_pub, "%d-%m-%Y")
    except:
        try:
            pubdate = datetime.strptime(date_pub, "%Y-%m-%d")
        except:
            row["Candidate Dates"] = ""
            return row
        
    dates_list = []
    dates_language_list = []
    doc = nlp(art)
    for ent in doc.ents:
        if ent.label_ in date_label:
            expression = ent.text
            result = search_dates(expression, languages=['en'], settings={'RELATIVE_BASE': pubdate})
            if result:
                dates_language_list.append(result)
                dates_list.append(result[0][1])

    return_list = [pubdate]
    for date in dates_list:
        if abs((date-pubdate).days) <= 15:
            return_list.append(date)
    row["Candidate Dates"] = str(list(map(lambda x: x.strftime("%A, %d %B, %Y"), return_list)))
    return row


'''
Turn a row into messages for use in querying the model. If the row is meant to be used as an example, include an
assistant message with the correct answer to the query.
'''
def get_messages(row, example):
    try:
        pubdate = datetime.strptime(row["Date Published"], "%d-%m-%Y")
    except:
        try:
            pubdate = datetime.strptime(row["Date Published"], "%Y-%m-%d")
        except:
            return []
        
    m1 = {
        "role": "user",
        "content": "The article was published on " + pubdate.strftime("%A, %d %B, %Y")
    }
    m2 = {
        "role": "user",
        "content": "The list of dates is " + str(row["Candidate Dates"])
    }

    m3 = {
        "role": "user",
        "content": "Which of the above candidate dates is the date of the events described in this article: \n" + str(row["Article"])
    }
    if example:
        m4 = {
            "role": "assistant",
            "content": datetime.strptime(row["Datefixed"], "%Y-%m-%d").strftime("%A, %d %B, %Y")
        }
        return [m1, m2, m3, m4]
    return [m1, m2, m3]


'''
Query the model to find the date for a given row. shots determines how many examples are used, if any, and those examples are drawn from df.
'''
def contact_date_model(row, df, model, shots):
    
    m1 = {
            "role": "system",
            "content": DATE_LIST_TASK_MSG
        }
    m2 = {
            "role": "system",
            "content": DATE_LIST_INSTRUCTIONS_MSG
        }
    
    messages = [m1, m2]

    for i in range(0,shots):
        index = random.randint(0, len(df)-1)
        testrow = df.iloc[index]
        ex_messages = get_messages(testrow, True)
        messages += ex_messages

    pred_messages = get_messages(row, False)
    messages = messages + pred_messages

    attempts = 0
    retval = "error"
    while attempts < 5:
        try:
            completion = client.chat.completions.create(
                model=model,
                messages=messages
            )
            
            response = completion.choices[0].message
            retval = datetime.strptime(response.content, "%A, %d %B, %Y")
            break
        except Exception as e:
            try:
                if hasattr(e, 'status') and e.status == 429:
                    time.sleep(10)
                attempts += 1
            except:
                attempts += 1


    return retval

'''
Wrapper for querying dates. Used in case the contract for querying changes later.
'''
def get_date(row, test_df, model, shots):
    row = get_candidate_dates(row)
    date = contact_date_model(row, test_df, model, shots)
    if date != "error":
        return date.strftime("%Y-%m-%d")
    return date