## Header Files
from pygooglenews import *
import newspaper 
from transformers import pipeline
from tokenizers import Tokenizer
from summarizer import Summarizer,TransformerSummarizer
import streamlit as st


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


# Google news object
gn = GoogleNews(country='GB')
# Topics array
topics = ['Sports' , 'Technology', 'Business', 'Science']
news_lst = []
# Traverse in the topics array and store them for the objects 
for i in topics:
    news_article = News_article(i)
    news_lst.append(news_article)

## printing the category of the news for the objects
for i in news_lst:
    print(i.get_category())



## Traverse in the news article
for article in news_lst:
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



## Now getting the news for the specific link using Newspaper3k 
for article in news_lst:
    url = article.get_link()
    url_i = newspaper.Article(url="%s"%(url), language='en')
    url_i.download()
    url_i.parse()
    text = url_i.text
    article.set_news(text)


## Printing to make sure everything runs fine
for article in news_lst:
    c , t , l , n = article.get_n1()
    print('Category : ',c,'\n\t Title : ', t,'\n\t Link :',l)
    print('\n\t NEWS : ',n)
    print('\n','---'*50) 



## Using BERT model to get the summary
for article in news_lst:
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
    

## Using GPT-2 model to get teh summary
for article in news_lst:
    n = article.get_news() 
    GPT2_model = TransformerSummarizer(transformer_type="GPT2",transformer_model_key="gpt2-medium")
    full = ''.join(GPT2_model(n, min_length=60))
    article.set_summary(str(full)) 

## Printing the summary done by GPT-2 model
for i in news_lst:
    title , summary = i.get_summary()
    print('\n Title : ', title)
    print('\n\t Summary : ', summary)
    print('--'*100)


## Streamlit display 
for i in news_lst:
    c = i.get_category()
    st.header(i)
    st.subheader('Title')

