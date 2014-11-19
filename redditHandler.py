import json
import requests
import urllib2
import re
import markdown

MAIN_URL = "http://www.reddit.com"
default_list = list()  #List of subreddits to be searched.
subreddit_dictionary = dict()  #Mapping from subreddit name to subreddit class (and the corresponding list of pages).
url_mapping = dict()
url_score = dict()

class Page:
    def __init__(self, url, text, title, author):
        self.url = url
        self.text = text
        self.author = author
        self.title = title

    def printPage(self):
        print(self.title)
        print("By " + self.author)
        print(self.text)

def formatName(name):
    return name.replace(" ", "").lower()


def getStories(subreddit):
    return subreddit_dictionary[subreddit]


def search(sr_list):
    global subreddit_dictionary
    header = {'User-Agent' : 'My borrt yo'}
    subreddit_dictionary.clear()
    for subreddit in sr_list:
        s = MAIN_URL + "/r/" + formatName(subreddit) + ".json"
        r = requests.get(s, headers = header)
        #print(r.status_code)
        data = json.loads(r.text)
        length = len(data['data']['children'])
        length = min(length, 11)
        pageList = list()
        for i in range(0, length):
            element = data['data']['children'][i]
            if element['data']['selftext']:
                text = element['data']['selftext']
                author = element['data']['author']
                title= re.sub("([\(\[]).*?([\)\]])", '', element['data']['title']) #regexp to strip tags (ie, content inside parentheses)
                title = title.lstrip(' ') #strips any leading whitespace, to ensure the title is later coloured correctly.
                url= element['data']['url']

                p = Page(url, text, title, author)
                url_mapping[url] = p
                pageList.append(p)

        subreddit_dictionary[subreddit] = pageList

def isValidSubreddit(name):
    header = {'User-Agent' : 'My borrt yo'}
    s = MAIN_URL + "/r/" + formatName(name) + ".json"
    r = requests.get(s, headers = header)
    data = json.loads(r.text)
    return (data['data']['children'])

def setup():
    #default_list.append("No Sleep")
    default_list.append("Short Scary Stories")
    #default_list.append("Creepy Pasta")
    #default_list.append("Dark Tales")
    #default_list.append("Horror")
    #default_list.append("Lovecraft")
    #default_list.append("The Truth Is Here")
    #default_list.append("True Creepy")
    #default_list.append("Glitch_in_the_Matrix")
    #default_list.append("Paranormal")
    #default_list.append("Slenderman")    

setup()