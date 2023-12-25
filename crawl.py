import requests
from bs4 import BeautifulSoup
import logging

def get_content(url,tag=None):
    '''
        Parse the html content for the optional tag form the url
        args :
                url : the url of the target site
                tag: the html tag for which text content is parsed. eg. "title"
    '''
    try:
        logging.info('Crawling the url received ...')
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 403:
            logging.error("Access to the website is denied.")
        else:
            logging.info('Processing the text from the url...')
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            if tag:
                tag_body = soup.find(tag)
                if tag_body:
                    tag_text = tag_body.text
                else: tag_text=None
            text_content = soup.get_text()
            return text_content, tag_text
    except requests.exceptions.HTTPError as errh:
        logging.error ("HTTP Error: %s"%errh.args[0])
    except requests.exceptions.ConnectionError as errc:
        logging.error ("Error Connecting:")
    except requests.exceptions.Timeout as errt:
        logging.error ("Timeout Error:")
    except requests.exceptions.RequestException as err:
        logging.error ("Oops, something went wrong:")

