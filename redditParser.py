import jsonUrl
import random as r
import urllib.request as q

TITLE = 0
TEXT = 1
IMAGE = 2
VIDEO = 3

#	A function that returns a random post from the home page of the desired sub reddit
#	The function can return different types of data
#	TITLE: returens a string containing the random post title
#	TEXT: returns a string containing the random post title and text content if any
#	IMAGE: returns a url for the image of the post, if there is no image a url to the post is returned
#TODO	VIDEO: ??

def random(sub_name=None, type=TITLE):
	if sub_name == None:
		print("Error: no subreddit chosen")
		return -1
	
	sub_name = sub_name.strip()
	if "r/" in sub_name:
		sub_name = sub_name.replace("r/", "")
	elif "r\\" in sub_name:
		sub_name = sub_name.replace("r\\", "")

	url = "https://www.reddit.com/r/" + sub_name + "/.json?limit=100"
	data = jsonUrl.load(url)

	dist = data["data"]["dist"]
	rand = int(r.randint(0, dist*5000)/5000)

	if type == TITLE:
		return data["data"]["children"][rand]["data"]["title"]
	if type == TEXT:
		a = data["data"]["children"][rand]["data"]["title"]
		b = data["data"]["children"][rand]["data"]["selftext"]
		a += ("\n\n" + b)
		return a
	if type == IMAGE:
		return data["data"]["children"][rand]["data"]["url"]
	if type == VIDEO:
		#	This branch is unfinished
		url = data["data"]["children"][rand]["data"]["url"]
		media = data["data"]["children"][rand]["data"]["media"]
		mp4 = media["reddit_video"]["fallback_url"]
		audio = url + "/HLS_AUDIO_64_K.ts"
		return mp4, audio