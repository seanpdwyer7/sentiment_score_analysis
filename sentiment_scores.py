import pandas as pd
import datetime as dt
import os
import numpy as np
from src.storage.googlesheets import getSheet,appendTo,clearSheet
from datetime import datetime 
from datetime import date,timedelta
from pygooglenews import GoogleNews
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_da_news(random_text):
    gn = GoogleNews(country = 'US')
    result = gn.search(random_text)
    data = pd.DataFrame.from_dict(result['entries'])
    return data

def sentiment_analyzer_scores(sentence):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(sentence)
    return score #pd.DataFrame(score, index = [0])

def sentiment_scores(text):
    data = get_da_news(text)
    scores = []

    for i in data['title']:
        #print(i)
        scores.append(sentiment_analyzer_scores(i))
        
    final = pd.DataFrame.from_dict(scores)
    final['title']= data['title']
    final['link']= data['link']
    return final


def get_da_news_and_dump_to_slack(random_text):
    gn = GoogleNews(country = 'US')
    result = gn.search(random_text, when = '7d')
    data = pd.DataFrame.from_dict(result['entries'])
    news = pd.DataFrame({"published_date":data['published'],'title':data['title'],'link':data['link']})
    sheet = '1_7iPt4JCdAJGU-4jwdifKMIjqX_ncTCPxEimmcDo_Us'
    tab = 'news!A:Z'
    clearSheet(sheet,tab)
    appendTo(sheet,tab,news,header=True)
    return news



def stock_sentiment():
    news = []
    position = []
    sheet = '1_7iPt4JCdAJGU-4jwdifKMIjqX_ncTCPxEimmcDo_Us'
    tab1 = 'Robinhood_Watchlist!A:AE'
    tab2 = 'watch_list_sentiment_scores!A:Z'
    tab3 = 'owned_sentiment!A:Z'
    tab4 = 'Robinhood Positions!A:Z'
    clearSheet(sheet,tab2)
    clearSheet(sheet,tab3)
    positions = getSheet(sheet,tab4, header = False)
    watchlist = getSheet(sheet,tab1, header = False)
    for i in watchlist['name']:
        shit = sentiment_scores(i)
        shit['name'] = watchlist['name']
        news.append(shit)
        
    for i in positions['name']:
        print(i)
        shitty = sentiment_scores(i)
        shitty['name'] = positions['name']
        position.append(shitty)
        


    da_news = pd.concat(news)
    da_news2 = pd.concat(position)
    appendTo(sheet,tab2,da_news,header=True)
    appendTo(sheet,tab3,da_news2,header=True)
    
    
def get_da_business_and_dump_to_slack():
    gn = GoogleNews(country = 'US')
    result =  gn.topic_headlines('BUSINESS')
    data = pd.DataFrame.from_dict(result['entries'])
    news = pd.DataFrame({"published_date":data['published'],'title':data['title'],'link':data['link']})
    sheet = '1_7iPt4JCdAJGU-4jwdifKMIjqX_ncTCPxEimmcDo_Us'
    tab = 'business_news!A:Z'
    clearSheet(sheet,tab)
    appendTo(sheet,tab,news,header=True)
    return news

def main():
    stock_sentiment()
    get_da_news_and_dump_to_slack("S&P500")
    get_da_business_and_dump_to_slack()
    
    
if __name__ == "__main__":
    main()
