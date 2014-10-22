# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for, Markup
import redditHandler
import jinja2
import random

# Initialize the Flask application
app = Flask(__name__)
app.debug = True

selectedSoFar = list()

# Define a route for the default URL, which loads the form
@app.route('/')
def mainPage():
	checked_list = list()
	string = ""
	redditHandler.search(redditHandler.default_list)
	a = random.choice(redditHandler.default_list) #random subreddit from checked list.
	b = random.choice(redditHandler.subreddit_dictionary[a])
	#remove b, or keep track of it somehow. Also, ensure that the same subreddit isn't visited twice in a row
	selectedSoFar.append(b)
	title = b.title
	first = title.partition(" ")[0]
	rest  = ''.join(title.partition(" ")[1:])
	string+=b.text
	string = '<br>'.join(string.split('\n'))
	return render_template("main.html", content=string, first = first, rest = rest)

#To-do:
#-Only consider pages of a certain length
#Keep track of pages that have been seen so far.
#Same subreddit shouldn't be visited twice in a row.