import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from whoosh.qparser import QueryParser
from whoosh.index import open_dir

#written by GPT to remove non-letters from a string
#via regular expressions
from utils import remove_non_letters


# Function to ensure required NLTK resources are available
from utils import get_nltk_resources_in


def get_relevant_links(query_to_parse):

    #download stop_words such as 'a', 'the', etc. if necessary
    get_nltk_resources_in('/home/u083/public_html/venv/nltk_data')
    #store each stop word at most once
    stop_words = set(stopwords.words('english'))

    #open index
    ix = open_dir("indexdir")

    
    #remove irrelevant charachters such as non-letters, extra spaces and page breaks from a query
    query = remove_non_letters(query_to_parse)
    query = query.replace("\n", " ").replace("\r", " ").replace("  ", " ").lower()

    #tokenize a query
    query_tokens = word_tokenize(query)
    #only store unique query tokens
    query_tokens = set(query_tokens)

    #remove stop words from a query i.e. remove irrelevant tokens from the query
    query_tokens_without_stop_words = []
    for token in query_tokens:
        if token not in stop_words:
            query_tokens_without_stop_words.append(token)
    
    #this is the list of whoosh scheme instances which are relevant for a query
    #this list is to be returned by this method i.e.
    #by the method get_relevant_links
    relevant_links = []
    #look for relevant pages given each relevant query token
    for token in query_tokens_without_stop_words:
        #get pages from the index which are relevant for a given token
        with ix.searcher() as searcher:
            whoosh_query = QueryParser("content", ix.schema).parse(token)
            results = searcher.search(whoosh_query)
            #add to relevant_links only those whoosh schema instances
            #which are not already there
            for r in results:
                if not r in relevant_links:
                    relevant_links.append(r)
            

        """
        if token in index:
            for link in index[token]:
                if link not in relevant_links:
                    relevant_links.append(link)
        """
    #return the list of whoosh shema instances
    #such that every instance is relevant
    #to at least some non-stop-word from the query
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