'''
Constants file containing fine-tuned models and instruction messages for querying.
'''

elephant_injury_model = "ft:gpt-3.5-turbo-1106:personal:elephantinjury:9y2OPfuv"
elephant_death_model = "ft:gpt-3.5-turbo-1106:personal:death:9j9VIqI8"
human_death_model = "ft:gpt-3.5-turbo-1106:personal:humandeath:9qoGOiiG"
human_injury_model = "ft:gpt-3.5-turbo-1106:personal:humaninjury:9u7UbgQR"
#location_model = "ft:gpt-3.5-turbo-1106:personal::9Ik8iogT" #original
location_model = "ft:gpt-3.5-turbo-1106:personal:loc:9ipA4efM" 
#location_model = "ft:gpt-3.5-turbo-1106:personal::9Tj3z5Xp" #country and village only
classify_model = "ft:gpt-3.5-turbo-1106:personal:classify:9z7Ce3wt"
date_model = "ft:gpt-3.5-turbo-1106:personal::9bC2BfEw"
date_event_model = "ft:gpt-3.5-turbo-1106:personal::9in8VFdY"

CLASSIFY_MSG = "Read and classify the titles of articles to determine whether they were written about an instance of human-wildife conflict. Human-elephant conflict is any instance of either a human or elephant being injured or killed, or an elephant carcass being discovered by humans. If the statement is written about an incident of human-wildlife conflict, respond with 'Y'. If it isn't, respond with 'N'."

DATE_LIST_TASK_MSG = """

    You will be given an article, the date it was published, and a list of dates. Your task is to examine the list of dates and figure out which one is most likely to be the date
    that the most recent incident of human-elephant conflict mentioned in the article took place. Human-elephant conflict is any instance of either a human or elephant being injured or killed, or an elephant carcass being discovered by humans.
    For example, if you had an article published on 2004-01-20, with the text 'Four days ago, a man was attacked by an elephant' and the list ["Friday, Janury 20, 2004", "Monday, Janury 16, 2004"], you would choose "Monday, Janury 16, 2004". If none of the dates provided fit, return your best guess.

"""

DATE_LIST_INSTRUCTIONS_MSG = """
    Your instructions are to 
    1.Read the date the article was published. 
    2.Read the list of dates provided. 
    3.Read through the article to find the time when the most recent incident of human-elephant conflict in the article happened. 
    4.Pick the date out of the provided list that best matches this time.

"""

ELEPHANT_DEATH_TASK_MSG = """

    You will be given an article describing an incident of human-elephant conflict. Your task is to read the text of the article and determine the number of elephants that died in the most recent incident of
    human-wildlife conflict mentioned by that article.  Human-elephant conflict is defined as "any human elephant interaction which results in negative effects on human social, economic or cultural life, AND/OR on elephant conservation and the environment".
    Once you have determined the number of deaths, you may return your answer as a single integer. 

"""

ELEPHANT_DEATH_INSTRUCTIONS_MSG = """
    Your instructions are to 
    1.Read through the article provided.
    2.Determine the number of elephants who died in the most recent incident of human-elephant conflict.
    3.Reply with the number of elephants who died. For exmaple, if you read an article where 3 elephants died, you would reply with "3".

"""

HUMAN_DEATH_TASK_MSG = """

    You will be given an article describing an incident of human-elephant conflict. Your task is to read the text of the article and determine the number of humans that died in the most recent incident of
    human-wildlife conflict mentioned by that article.  Human-elephant conflict is defined as "any human elephant interaction which results in negative effects on human social, economic or cultural life, AND/OR on elephant conservation and the environment".
    Once you have determined the number of deaths, you may return your answer as a single integer. 

"""

HUMAN_DEATH_INSTRUCTIONS_MSG = """
    Your instructions are to 
    1.Read through the article provided.
    2.Determine the number of humans who died in the most recent incident of human-elephant conflict.
    3.Reply with the number of humans who died. For exmaple, if you read an article where 3 humans died, you would reply with "3".

"""

ELEPHANT_INJURY_TASK_MSG = """

    You will be given an article describing an incident of human-elephant conflict. Your task is to read the text of the article and determine the number of elephants that were injured in the most recent incident of
    human-wildlife conflict mentioned by that article.  Human-elephant conflict is defined as "any human elephant interaction which results in negative effects on human social, economic or cultural life, AND/OR on elephant conservation and the environment".
    Once you have determined the number of injuries, you may return your answer as a single integer. 

"""

ELEPHANT_INJURY_INSTRUCTIONS_MSG = """
    Your instructions are to 
    1.Read through the article provided.
    2.Determine the number of elephants who were injured in the most recent incident of human-elephant conflict.
    3.Reply with the number of elephants who were injured. For exmaple, if you read an article where 3 elephants were injured, you would reply with "3".

"""

DEFAULT_TASK_MSG = """
    You will be given an article describing an incident of human-elephant conflict. Your task is to read the text of the article and determine the number of {species}s that {incident} in the most recent incident of
    human-wildlife conflict mentioned by that article.  Human-elephant conflict is defined as "any human elephant interaction which results in negative effects on human social, economic or cultural life, AND/OR on elephant conservation and the environment".
    Once you have determined the number of {species}s that were {incident}, you may return your answer as a single integer. 
"""

DEFAULT_INSTRUCTIONS_MSG = """
    Your instructions are to 
    1.Read through the article provided.
    2.Determine the number of {species}s who {incident} in the most recent incident of human-elephant conflict.
    3.Reply with the number of {species}s who {incident}. For exmaple, if you read an article where 3 {species}s {incident}, you would reply with "3".

"""

LOCATION_TASK_MSG = """

    You will be given an article describing an incident of human-elephant conflict. Your task is to read the text of the article and figure out which ones are most likely to describe the location
    where the most recent incident of human-elephant conflict mentioned in the article took place. Human-elephant conflict is defined as "any human elephant interaction which results in negative effects on human social, economic or cultural life, AND/OR on elephant conservation and the environment".
    Once you have determined where the incident took place, you should return geographical data as a set of key-value pairs in JSON format in the format {"Country": " ", "State": " ", "District": " ", "Village/Place": " "}. If you can't determine the value
    for one of these keys from the article, set it to "NG".

"""
LOCATION_INSTRUCTIONS_MSG = """
    Your instructions are to 
    1.Read the list of provided locations.
    2.Read through the article to find the location where the most recent incident of human-elephant conflict in the article happened. 
    3.Return the location data that you found in JSON format as described above.
"""

LOCATION_TASK_MSG_STATE = """

    You will be given an article describing an incident of human-elephant conflict. Your task is to read the text of the article and figure out the state
    where the most recent incident of human-elephant conflict mentioned in the article took place. Human-elephant conflict is defined as "any human elephant interaction which results in negative effects on human social, economic or cultural life, AND/OR on elephant conservation and the environment".
    Once you have determined where the incident took place, you should return the state as a single word. I.e. if an incident occurred in Tamil Nadu, you would reply with "Tamil Nadu". If you can't determine the value
    for one of these keys from the article, set it to "NG".

"""
LOCATION_INSTRUCTIONS_MSG_STATE = """
    Your instructions are to 
    1.Read the list of provided locations.
    2.Read through the article to find the location where the most recent incident of human-elephant conflict in the article happened. 
    3.Return the state in which the incident occurred..
"""

LOCATION_TASK_MSG_VILLAGEPLACE = """

    You will be given an article describing an incident of human-elephant conflict. Your task is to read the text of the article and figure out the village or place
    where the most recent incident of human-elephant conflict mentioned in the article took place. Human-elephant conflict is defined as "any human elephant interaction which results in negative effects on human social, economic or cultural life, AND/OR on elephant conservation and the environment".
    Once you have determined where the incident took place, you should return the village or place as a single word. I.e. if an incident occurred in Tamil Nadu, you would reply with "Tamil Nadu". If you can't determine the value
    for one of these keys from the article, set it to "NG".

"""
LOCATION_INSTRUCTIONS_MSG_VILLAGEPLACE = """
    Your instructions are to 
    1.Read the list of provided locations.
    2.Read through the article to find the location where the most recent incident of human-elephant conflict in the article happened. 
    3.Return the village or place in which the incident occurred..
"""