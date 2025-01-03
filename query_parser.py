import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from collections import Counter
from whoosh.qparser import QueryParser
from whoosh.index import open_dir




def remove_non_letters(text):
    return re.sub(r'[^a-zA-Z\s]', '', text)


def get_relevant_links(query_to_parse):



    try: 
        stop_words = set(stopwords.words('english'))
    except LookupError:
        #nltk.download('stopwords')
        nltk.download('stopwords', download_dir='/home/u083/AI_and_the_web_project_2/nltk_data')
        stop_words = set(stopwords.words('english'))

    ix = open_dir("indexdir")

    #query = "sobby European intellectual mentioned in 809240923 a literature /./././. intellectual wales"
 
    query = remove_non_letters(query_to_parse)
    query = query.replace("\n", " ").replace("\r", " ").replace("  ", " ").lower()
    query_tokens = word_tokenize(query)
    query_tokens = set(query_tokens)

    query_tokens_without_stop_words = []
    for token in query_tokens:
        if token not in stop_words:
            query_tokens_without_stop_words.append(token)

    relevant_links = []
    for token in query_tokens_without_stop_words:
        with ix.searcher() as searcher:
        
            whoosh_query = QueryParser("content", ix.schema).parse(token)
            results = searcher.search(whoosh_query)
            for r in results:
                print(r['title'])
                if not r['title'] in relevant_links:
                    relevant_links.append(r['title'])
            

        """
        if token in index:
            for link in index[token]:
                if link not in relevant_links:
                    relevant_links.append(link)
        """
    return relevant_links


#print(get_relevant_links())

"""
    print (query_tokens_without_stop_words)
    print (relevant_links)

    print("********************************************************************")

"""


    # print all results
#with ix.searcher() as searcher:
 #   for r in results:
      #  print(r)