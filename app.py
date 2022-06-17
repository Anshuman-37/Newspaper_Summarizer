## Header Files
from pygooglenews import *
import newspaper 
from transformers import pipeline
from tokenizers import Tokenizer
from summarizer import Summarizer,TransformerSummarizer
import streamlit as st
from stqdm import stqdm
import pickle
from datetime import datetime
import os.path
import torch

## To remove the cache
torch.cuda.empty_cache()

## Title for the news
st.title('NewsPaper Summarizer')

# Variable to check wether we need to show new news or old one
Flag = 0

# Check wether the application has run already run once today
if(os.path.isfile('News.pickle')):

    # Opening the pickle file
    with open('News.pickle', 'rb') as handle:
            News_article_dict = pickle.load(handle)
    time_now = datetime.now()

    c = str(time_now-News_article_dict['Time'])
    c = c.split(':')
    
    # Check wether 3 hours have been passed from the last time the agent was used 
    if int(c[1]) < 3:
        for key,value in News_article_dict.items():
            if key == 'News':
                for i in value:
                    print(i['Summary'])
                    st.header(i['Category'])
                    st.subheader(str(i['Title']))
                    st.write(str(i['Summary']))
        Flag = 1

## We need to fetch new news
if Flag == 0:

    st.write('Please wait for a bit ...... Fetching new News')

    ### container for the news
    class News_article:
        # Category : The type of news
        # Title : The title of the news
        # News : The news
        # Hyper_link : to Store the link
        # Summay : Stores the summary of the news
        def __init__(self, category):
            '''Update category of the news'''
            self.category = category
        def set_title(self,title,link):
            ''' Update the news and the Category '''
            self.title = title
            self.hyper_link = link
        def get_link(self):
            ''' Return the link '''
            return self.hyper_link
        def set_news(self,news):
            ''' Updates the news for the link '''
            self.news = news
        def get_news(self):
            ''' Return the news for specific article '''
            return self.news 
        def set_summary(self,summary):
            ''' Updates the summary for the news '''
            self.summary = summary
        def get_category(self):
            ''' Returns the category of the news '''
            return self.category
        def get_summary(self):
            ''' Returns the Title of the news and its summary '''
            return self.title , self.summary
        def get_category(self):
            ''' Return the category '''
            return self.category
        def get_n(self):
            '''Return the category, title and the link of the news'''
            return  self.category,self.title,self.hyper_link
        def get_n1(self):
            '''Return the category, title, the link, and news'''
            return  self.category,self.title,self.hyper_link,self.news


    ## Just to show the summary 
    st.write('Grabbing news...... ')


    # Google news object
    gn = GoogleNews(country='GB')
    # Topics array
    topics = ['Sports' , 'Technology', 'Business', 'Science']
    news_lst = []
    # Traverse in the topics array and store them for the objects 
    for i in stqdm(topics):
        news_article = News_article(i)
        news_lst.append(news_article)

    ## printing the category of the news for the objects
    for i in news_lst:
        print(i.get_category())
   


    ## Traverse in the news article
    for article in stqdm(news_lst):
        category = article.get_category()
        news = gn.topic_headlines(category)
        z=0
        ## Getting the title of the news
        for n in news['entries']: 
            if z>0 : break;
            title = n['title']
            print(n['title']); 
            z+=1; k=0;
            # Getting the link for the specific news
            for l in n['links']:
                if k>0 : break;
                link = l['href']
                print(l['href']); 
                k+=1
        ## popluate the objects with title and link
        article.set_title(title,link)



    # Printing to make sure everything is running smooth
    for article in news_lst:
        c , t , l = article.get_n()
        print('Category : ',c,'\n\t Title : ', t,'\n\t Link :',l) 


    ##
    st.write('Grabbing the content of news')
    ##

    ## Now getting the news for the specific link using Newspaper3k 
    for article in stqdm(news_lst):
        try:
            url = article.get_link()
            url_i = newspaper.Article(url="%s"%(url), language='en')
            url_i.download()
            url_i.parse()
            text = url_i.text
        except:
            text = "Sorry unable to grab news"
        article.set_news(text)


    ## Printing to make sure everything runs fine
    for article in news_lst:
        c , t , l , n = article.get_n1()
        print('Category : ',c,'\n\t Title : ', t,'\n\t Link :',l)
        print('\n\t NEWS : ',n)
        print('\n','---'*50) 

    ##
    st.write('Making the BERT summary')
    ##

    ## Using BERT model to get the summary
    for article in stqdm(news_lst):
        n = article.get_news() 
        bert_model = Summarizer()
        bert_summary = ''.join(bert_model(n, min_length=60))
        article.set_summary(str(bert_summary))

    ## Printing the summary done by BERT model
    for i in news_lst:
        title , summary = i.get_summary()
        print('\n Title : ', title)
        print('\n\t Summary : ', summary)
        print('--'*100)
        
    ## FOR the sake of testing it
    # ##
    # st.write('Making the GPT-2 summary')
    # ##

    # ## Using GPT-2 model to get the summary
    # for article in stqdm(news_lst):
    #     n = article.get_news() 
    #     GPT2_model = TransformerSummarizer(transformer_type="GPT2",transformer_model_key="gpt2-medium")
    #     full = ''.join(GPT2_model(n, min_length=60))
    #     article.set_summary(str(full)) 

    # ## Printing the summary done by GPT-2 model
    # for i in stqdm(news_lst):
    #     title , summary = i.get_summary()
    #     print('\n Title : ', title)
    #     print('\n\t Summary : ', summary)
    #     print('--'*100)



    for i in news_lst:
        c = i.get_category()
        st.header(str(c))
        t , s = i.get_summary()
        st.subheader(str(t))
        st.write(str(s))

    res_dict = {}
    res_dict['Time'] = datetime.now()
    News = []
    for news in news_lst:
        news_dict = {}
        category = news.get_category() ; title , summary = news.get_summary();
        news_dict['Category'] = category ; news_dict['Title'] = title ; news_dict['Summary'] = summary;
        News.append(news_dict)

    res_dict['News'] = News

    for key,value in res_dict.items():
        if key == 'News':
            for i in value:
                print(i['Summary'])
                print(100*'+')

    with open('News.pickle', 'wb') as handle:
        pickle.dump(res_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open('News.pickle', 'rb') as handle:
        b = pickle.load(handle)


    for key,value in b.items():
        if key == 'News':
            for i in value:
                print(i['Summary'])
                print(100*'+')
