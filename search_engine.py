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
    relevant_links = get_relevant_links(query)
    #return_string = "<h1>"
    return_string = ""
    for i in range(len(relevant_links)):
        return_string += '<a href = "'
        return_string += relevant_links[i]
        return_string += '">'
        return_string += str(i+1)
        return_string += '</a><br>'
        #return_string += " "
    #return_string += "</h1>"

    if return_string != "": 
        return return_string
    else:
        return "<h1>no results found</h1>"
    #return '<a href = "google.com">123</a>'
    #return "<h1>"+request.args['rev'][::-1]+"NIOBA"
