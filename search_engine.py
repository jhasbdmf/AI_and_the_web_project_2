from flask import Flask, request
from query_parser import get_relevant_links

app = Flask(__name__)

@app.route("/")
def start():
    return "<form action='reversed' method='get'><input name='rev'></input></form>"

@app.route("/reversed")
def reversed():
    query = request.args['rev']
    relevant_links = get_relevant_links()
    return_string = "<h1>"
    for i in relevant_links:
        return_string += i
        return_string += " "
    return_string += "</h1>"

    return return_string
    #return "<h1>"+request.args['rev'][::-1]+"NIOBA"
