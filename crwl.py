import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from collections import Counter
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT
#from query_parser import get_relevant_links


def remove_non_letters(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)

try: 
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
stop_words = set(stopwords.words('english'))



prefix = 'https://vm009.rz.uos.de/crawl/'
start_url = prefix + 'index.html'


agenda = [start_url]
visited_links = []
index = {}

schema = Schema(title=TEXT(stored=True), content=TEXT)
ix = create_in("indexdir", schema)
writer = ix.writer()


while agenda:
    url = agenda.pop()
    visited_links.append(url)
    print("Get ",url)
    
    r = requests.get(url)
    #print(r, r.encoding)
    if r.status_code == 200:
        #print(r.headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        #get lowercase of a web page without line breaks and double spaces
        page_text = soup.get_text().replace("\n", " ").replace("\r", " ").replace("  ", " ").lower()

        writer.add_document(title=url, content=page_text)

        #these are lines of code which do indexing without whoosh
        """
        #clean page text by removing punctuations signs from it
        page_text_without_punctuation = remove_non_letters(page_text)
        #tokenize cleaned page text
        tokens_of_a_page = word_tokenize(page_text_without_punctuation)
        #leave stop words, which are irrelevant for information retrieval, out of consideration
        tokens_of_a_page_without_stop_words = []
        for token in tokens_of_a_page:
            if token not in stop_words:
                tokens_of_a_page_without_stop_words.append(token)
        #counted_tokens_of_a_page = Counter(tokens_of_a_page_without_stop_words)
        #print (counted_tokens_of_a_page)

        new_index_items = dict.fromkeys(set(tokens_of_a_page_without_stop_words), url)
        #print (new_index_items)
   
        for key, value in new_index_items.items():
            if not key in index:
                index[key] = [value]
            elif not value in index[key]:
                index[key].append(value) 
        """

        #agenda.extend(soup.find_all('a'))
  
        list_of_all_links_on_a_page = soup.find_all('a')
        for href in list_of_all_links_on_a_page:
            if href.get('href'):
                
                if prefix in href.get('href'):
                    link = href.get('href')
                #this ensures that the crawler does not scrap other websites
                else:
                    link = prefix + href.get('href')
                if not link in visited_links and not link in agenda:
                    agenda.append(link)

            #print (prefix + link.get('href'))
        
        #print(soup.find_all('a'))
        #print (type(soup.find_all('a')[0]))
        #print("Agenda: ", agenda)
        print("_________________________________________________________________")

#print (index)

#for key, value in sorted(index.items()):
#    print(f"{key}: {value}")


writer.commit()

#print(get_relevant_links())


