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
    