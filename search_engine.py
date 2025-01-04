from flask import Flask, request
from query_parser import get_relevant_links
import traceback

app = Flask(__name__)



@app.errorhandler(500)
def internal_error(exception):
    return "<pre>" + traceback.format_exc() + "</pre>"

@app.route("/")
def start():
    return "<form action='search_for_pages' method='get'><input name='search_query'></input></form>"

@app.route("/search_for_pages")
def search_for_pages():
    query = request.args['search_query']
    search_results = get_relevant_links(query)
    
    #return_string = "<h1>"
    return_string = "<html><head></head><body>"
    return_string += "<div id='header' align='center'><form action='search_for_pages' method='get'><input name='search_query' value=" + query + "></input></form></div>"
    return_string += "<div id='main-content' style='width: 50%; margin-left: auto; margin-right: auto;'>"
    if len(search_results) > 0:
        for i in range(len(search_results)):
            return_string += '<a href = "' + search_results[i]["page_url"] + '">'
            return_string += search_results[i]["title"]
            return_string += '</a>'
            return_string += '<p>' + search_results[i]["content_summary"] + '</p><br>'
    else:
        return_string += "<h3>no results found</h3>"
    return_string += "</div></body></html>"
    return return_string
    
 
