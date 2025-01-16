To access the search engine, log into the UOS VPN, open your browser
and go to http://vm322.rz.uni-osnabrueck.de/u083/AI_and_the_web_project_2/search.wsgi/

On that page you will see an input box. Enter your query there.
After that you will be forwarded to another web page of the project
which contains links and content of pages which are relevant to
the query and are from the aforementioned toy website 

As for the acrchitecture of the web app, it consists of
    1) the cralwer (crawler.py)
    2) the flask interface to query the index created by the crawler (search_engine.py)
    
The search_engine.py contains 2 web pages: 
    1) the initial page with an input box to enter the first query. Its html-template is 
       in templates/start.html
    2) the second page which displays the input box with the last query and pages from 
       https://vm009.rz.uos.de/crawl/ relevant for that query. Its html-template is 
       in templates/search_for_pages.html 


Search_engine.py imports the method, which finds pages in a crawler-created index
which are relevant for the query, from query_parser.py.
Both crawler.py and query_parser.py import methods from utils.py.
