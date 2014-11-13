from flask import Flask, render_template, request, url_for, Markup
import redditHandler
import jinja2
import random
import markdown

# Initialize the Flask application
app = Flask(__name__)
app.debug = True

searched = False #If the list of pages has been searchd (and cached) yet
selectedSoFar = set() #List of pages visited so far.

def ensureUniqueness(sr):

	global selectedSoFar
	t = set()
	for s in sr:
		t.add(s.url)
	return random.sample(t - selectedSoFar, 1)[0]
 
# Define a route for the default URL
@app.route('/')
def mainPage():
	global selectedSoFar
	global searched
	if not searched:
		redditHandler.search(redditHandler.default_list)
		searched = True
	
	randomSubreddit = random.choice(redditHandler.default_list) #random subreddit from checked list.
	pageList = redditHandler.subreddit_dictionary[randomSubreddit] #list of that subreddit's pages
	selectedPage = redditHandler.url_mapping[ensureUniqueness(pageList)]


	selectedSoFar.add(selectedPage.url)
	title = selectedPage.title
	first = title.partition(" ")[0]
	rest  = ''.join(title.partition(" ")[1:])
	string = selectedPage.text
	string = markdown.markdown(string) 

	return render_template("main.html", content=string, first = first, rest = rest)

@app.route('/search')
def searchPage():
	return mainPage()

#To-do       
#-Only consider pages of a certain length
#Keep track of pages that have been seen so far
#Same subreddit shouldn't be visited twice in a row