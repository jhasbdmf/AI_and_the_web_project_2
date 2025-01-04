from flask import Flask, request
from query_parser import get_relevant_links
import traceback

app = Flask(__name__)



@app.errorhandler(500)
def internal_error(exception):
    return "<pre>" + traceback.format_exc() + "</pre>"

@app.route("/")
def start():
    return "<form action='reversed' method='get'><input name='rev'></input></form>"

@app.route("/reversed")
def reversed():
    query = request.args['rev']
    search_results = get_relevant_links(query)
    #return_string = "<h1>"
    return_string = "<form action='reversed' method='get'><input name='rev'></input></form>"
    for i in range(len(search_results)):
        return_string += '<a href = "' + search_results[i]["page_url"] + '">'
        return_string += search_results[i]["title"]
        return_string += '</a><br>'
        return_string += '<p>' + search_results[i]["content_summary"] + '</p><br>'
        #return_string += " "
    #return_string += "</h1>"

    if return_string != "": 
        return return_string
    else:
        return "<h1>no results found</h1>"
    #return '<a href = "google.com">123</a>'
    #return "<h1>"+request.args['rev'][::-1]+"NIOBA"
