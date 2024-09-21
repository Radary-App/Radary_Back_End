
# import analyser, summarizer, translator
from .analyser import analyser
from .summarizer import summarize
from .translator import translate as translator

def analyse_accident(image_data):
    retries = 0
    
    while retries < 3:
        try:
            description, title, authority, level = analyser.analyse_accident(image_data)
            break
        except:
           retries+=1

    if retries>=3:
         description, title, authority, level= "None", "None", "None", 0
         retries = 0 
        
    if authority.lower() =="fire station":
        authority = "Fire_station"
    return description, title, authority, level 


def analyse_isuue(image_data):
    retries = 0
    
    while retries < 3:
        try:
            description, title, authority, priority = analyser.analyse_isuue(image_data)
            break
        except:
           retries+=1

    if retries>=3:
         description, title, authority, priority = "None", "None", "None", -10
         retries = 0 
    
    return description, title, authority, priority 

def summarize(feedbacks):
    summary = summarize(feedbacks)
    return summary

def translate(text, lang= "Arabic"):
    return translator(text, lang)
