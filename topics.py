import crawl
from urllib.parse import urlparse
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
from vectorize import Vectorize as vec 
import logging

class Topics:
    def __init__(self, url) -> None:
        self.url = url
        if not url:
            logging.error('No url received. Try again.')
            return
        self.text, self.title = crawl.get_content(self.url,'title')
        self.text = re.sub(r'[^\w\s-]',' ',self.text)
        self.text = self.text.lower()
        self.text = self.text.strip()
        self.tokens = {}

    def get_topics(self,n,m):
        logging.info('Proceeding to tokenize the content')
        self._get_url_tokens()
        self._get_title_tokens()
        self._get_tokens()
        logging.info('Vectorizing the content and reshaping..')
        v=vec(self.tokens['cumulative'],self.text)
        result = v.predict(n,m)
        return result
    
    def _get_url_tokens(self):
        '''
        We extract the tokens from the urls.
        '''
        p = urlparse(self.url)
        path = p.path
        query = p.query
        params = p.params
        res = ''
        if path:
            res += re.sub(r'[^\w\s-]',' ',path)
        if query:
            res += ' '+re.sub(r'[^\w\s]',' ',query)
        if params:
            res  += ' '+re.sub(r'[^\w\s]',' ',params)
        logging.info('Parsed url text : %s' %res)
        self.tokens['url'] = word_tokenize(res) if res else []

    def _get_title_tokens(self):
        '''
            Given a title text, extract the tokens from the title.
        '''
        if not self.title:
            self.tokens['title'] = []
            return
        logging.info('Parsing for the title..')
        title_text = re.sub(r'[^\w\s-]',' ',self.title)
        logging.info('Parsed title of the content is %s' %title_text)
        self.tokens['title'] = word_tokenize(title_text)
    
    def _get_tokens(self):
        logging.info('Tokenizing the page text content')
        stop_words = set(stopwords.words('english'))
        stop_words.update(['com','add','ad','ads','chat','ago','reply','email','upload'])
        self.tokens['body'] = word_tokenize(self.text)
        self.tokens['cumulative'] = [token.lower() for token in 
                                     set().union(self.tokens['body'],
                                                 self.tokens['url'],
                                                 self.tokens['title'])                                     
                                     if token.lower() not in stop_words
                                     and not token.isnumeric() 
                                     and len(token) > 2] 

