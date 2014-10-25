from flask import Flask, render_template, request, url_for, Markup
import redditHandler
import jinja2
import random
import markdown

# Initialize the Flask application
app = Flask(__name__)
app.debug = True

searched = False #If the list of pages has been searchd (and cached) yet
flag = False
selectedSoFar = set() #List of pages visited so far.
lastSubreddit = "" #The most recently viewed subreddit.
currentSubreddit = "" #The subreddit from where the current page is from.

def getTitles(pageList):
	s = set()
	for p in pageList:
		s.add(p.title)
	return s

def findPage(pageList, title):
	for p in pageList:
		if p.title == title:
			return p

 
 
# Define a route for the default URL
@app.route('/')
def mainPage():
	global selectedSoFar
	global searched
	global flag
	flag = not flag
	if not searched:
		redditHandler.search(redditHandler.default_list)
		searched = True
	test = ""
	randomSubreddit = random.choice(redditHandler.default_list) #random subreddit from checked list.
	pageList = redditHandler.subreddit_dictionary[randomSubreddit] #list of that subreddit's pages

	titleList = getTitles(pageList)
	diff = titleList - selectedSoFar
	if not diff: 
		#Subreddit is emptied, should move on to next subreddit.
		#remove subreddit from reddithandler.default_list
		selectedSoFar.clear()
		diff = titleList
	r = random.sample(diff, 1)[0]
	b = findPage(pageList, r)


	selectedSoFar.add(b.title)
	title = b.title
	first = title.partition(" ")[0]
	rest  = ''.join(title.partition(" ")[1:])
	string = b.text
	string = markdown.markdown(string) 

	return render_template("main.html", content=string, first = first, rest = rest)

@app.route('/search')
def searchPage():
	return mainPage()

#To-do       
#-Only consider pages of a certain length
#Keep track of pages that have been seen so far
#Same subreddit shouldn't be visited twice in a row