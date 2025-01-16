from flask import Flask, request, render_template
from query_parser import get_relevant_links
import traceback
import pdb; 


app = Flask(__name__)

#this one is supposed to handle errors
@app.errorhandler(500)
def internal_error(exception):
    return "<pre>" + traceback.format_exc() + "</pre>"

#this one creates the initial page of the web app from a start.html template
@app.route("/")
def start():
    return render_template('start.html')




@app.route("/search_for_pages")
def search_for_pages():
    #the initial page has one input box to input a query
    #this command stores the query from the input box of 
    #the initial page in the variable "query"
    query = request.args['search_query']

    #this one calls the method "get_relevant_links" from the query_parser.py file
    #get_relevant_links(query) looks up pages in the index which are relevant for
    #at least one word from the query
    #the list of those pages is returned by the get_relevant_links method and 
    #stored in the search_results_variable
    search_results = get_relevant_links(query)
    #the flask app then returns a jinja-enhanced html page with the search results
    #the exact content of that page depends on the query and the web pages 
    #which the get_relevant_links method identified as relevant for that query
    #the template also has comments, so feel free to look into it
    return render_template('search_for_pages.html', found_pages=search_results, search_query=query)
    

 
