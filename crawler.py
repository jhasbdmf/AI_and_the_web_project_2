import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from collections import Counter
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, STORED
from whoosh.analysis import StemmingAnalyzer
from openai import OpenAI


#written by GPT to remove non-letters from a string
#via regular expressions
from utils import remove_non_letters


# Function to ensure required NLTK resources are available
from utils import get_nltk_resources_in

class Response_Generator:
    def __init__(self, api_key):
        self.model = OpenAI(api_key=api_key)
    def get_a_response(self, prompt, desired_temperature=1.1, max_response_length=200):
            #this one generates a response with given parameters
            chat_completion = self.model.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", 
                     "content": prompt
                    }
                ],
                temperature=desired_temperature,  
                max_tokens=max_response_length
            )
            #this one returns the best response option gpt provides to the prompt given parameters
            return chat_completion.choices[0].message.content



#from query_parser import get_relevant_links






"""
def generate_a_response_via_openAI(prompt, desired_temperature=1.1, max_response_length=200):
    #this one generates a response with given parameters
    chat_completion = OpenAI.
    Openai.сhat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", 
                     "content": prompt
                    }
                ],
                temperature=desired_temperature,  
                max_tokens=max_response_length
            )
    #this one returns the best response option gpt provides to the prompt given parameters
    return chat_completion.choices[0].message.content
"""

#api_key = "sk-svcacct-sasYDh93HtW8T-ZtXNCUElcOwmpB__D0ql2JJXLPl3kTrwrVeY2W_hTXl1AhYMsT3BlbkFJLcW4LbU2SOAgDFeOFXJyCA-l_xvOKYqPDTy1YJ2lGsEqPHLIXGwctBw7FOuGVAA"
api_key = "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"


#response_generator_instance = Response_Generator(api_key)

get_nltk_resources_in("")
stop_words = set(stopwords.words('english'))

"""
try: 
    stop_words = set(stopwords.words('english'))
except LookupError:
    nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
"""



#set the website to be crawler
url_prefix_of_the_crawled_website = 'https://vm009.rz.uos.de/crawl/'
#set the intial web page for a crawler
start_url = url_prefix_of_the_crawled_website + 'index.html'

#push the initial web page url to the list of urls to be visited by the crawler
agenda = [start_url]
#initialize the list of visited links
visited_links = []

#index = {}

#initialize the index schema with 4 attributes/columns
schema = Schema(
    #page title as determined by <head><title></title></head>
    #page counted as twice as relevant if a query token is there
    #copared to the case when the same token is in any other 
    #part of a page
    title=TEXT(stored=True, field_boost=2.0),
    #page url which is stored in the schema and yet is irrelevant for page ranking
    page_url = STORED, 
    #page text
    content=TEXT(analyzer=StemmingAnalyzer()),
    #summary of the page text
    content_summary = STORED
)

#created an index instance with a given schema
ix = create_in("indexdir", schema)
writer = ix.writer()

#while there are still links to be visited
while agenda:
    #remove one item from the agenda and store it in the url variable
    url = agenda.pop()
    #add that url to the list of visited links
    visited_links.append(url)
    print("Get ",url)
    
    
    #send an http get request to a web page referred to by the content of the url variable
    #and store the result in the r variable 
    r = requests.get(url)

    #if get request is successful
    if r.status_code == 200:
        
        #initialize a bs4 parser with that web page
        soup = BeautifulSoup(r.content, 'html.parser')

        #find all a-tags on a page
        list_of_all_links_on_a_page = soup.find_all('a')
        #iterate over all a-tags of a page
        for href in list_of_all_links_on_a_page:
            #if a-tag contains an url then continue
            if href.get('href'):
                
                #if the iterated a-tag points to page from the website to crawl,
                #then store the url of that page
                if url_prefix_of_the_crawled_website in href.get('href'):
                    link = href.get('href')
                #otherwise append the url of the a-tag to the website url-prefix
                #this would make dynamic urls from the website to be crawled complete
                #and invalidate urls from other websites 
                #a crawler would fail to get info from those
                #invalidated urls later
                else:
                    link = url_prefix_of_the_crawled_website + href.get('href')
                #if the resultant url is neither visited already nor is in the agenda,
                #then add it to the agenda
                if not link in visited_links and not link in agenda:
                    agenda.append(link)


        #get page title
        page_title = "Untitled page"
        if soup.title:
            page_title = soup.title.text

        #leave head- as well as a-tags out of consideration of the parser  
        for a in soup.find_all('a'):
            a.decompose()
        for head in soup.find_all('head'):
            head.decompose()

        #get lowercase text of a web page without line breaks and double spaces
        page_text = soup.get_text().replace("\n", " ").replace("\r", " ").replace("  ", " ").lower()

        prompt = "Summarize the following text in two sentences. The text to summarize is: {"
        prompt += page_text
        prompt += "}"
        #page_text_summary = generate_a_response_via_openAI(prompt)
        #page_text_summary = response_generator_instance.get_a_response(prompt)
        #print (page_text_summary)
        
        writer.add_document(title = page_title, page_url=url, content=page_text, content_summary=page_text)

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

       
       


        print("_________________________________________________________________")



#save crawling results
writer.commit()




