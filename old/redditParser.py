import json, re, requests, tempfile, ffmpy, os
import random as r
import urllib.request

TITLE = 0
TEXT = 1
IMAGE = 2
VIDEO = 3


#	A function that download a redit video and combines it with its audio
#	returns 1 on errors and 0 on success
def parseRedditVideo(link: str, outPath: str):
	# Check the link to add the .json request
	if link.endswith('/'):
		link += '.json'
	else:
		link += '/.json'

	# This would fail if the link is not actually from reddit
	try:
		response = requests.get(
			url=link,
			headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'}
		)
		json = response.json()

		isVideo = json[0]['data']['children'][0]['data']['is_video']
	except:
		print('Error: Is the link correctly spelled?')
		return 1

	if not isVideo:
		print('Error: The URL does not contain a video')
		return 1

	# Parse the link for the audio and video info
	mpdListLink = json[0]['data']['children'][0]['data']['media']['reddit_video']['dash_url']
	mpdResponse = requests.get(url=mpdListLink, headers={
		'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'})
	mpdXMLData = mpdResponse.text

	# Base link contains everything
	baseLink = json[0]['data']['children'][0]['data']['url']

	# This returns something like ['720p', '360p', 'audio'] or whatever
	reSearchData = re.findall('<BaseURL>(.*?)</BaseURL>', mpdXMLData)

	highestVideoQualityPartialLink = reSearchData[0]
	audioPartialLink = reSearchData[-1]

	highestVideoQualityFullLink = baseLink + '/' + highestVideoQualityPartialLink
	audioFullLink = baseLink + '/' + audioPartialLink

	tempDir = tempfile.gettempdir()
	tempVideoFilepath = tempDir + '/' + next(tempfile._get_candidate_names())
	tempAudioFilepath = tempDir + '/' + next(tempfile._get_candidate_names())

	# Store the actual data in the temp directory
	urllib.request.urlretrieve(highestVideoQualityFullLink, tempVideoFilepath)
	urllib.request.urlretrieve(audioFullLink, tempAudioFilepath)

	# Combine stuff into an actual video
	ff = ffmpy.FFmpeg(
		inputs={tempVideoFilepath: None, tempAudioFilepath: None},
		outputs={outPath: " -c copy "}
	)

	# A failsafe
	try:
		ff.run()
	except ffmpy.FFRuntimeError:
		print('Error: video generation failed, does a file with the same name already exist?')
		return 1

	try:
		os.remove(tempVideoFilepath)
		os.remove(tempAudioFilepath)
	except:
		print('Error: Could not delete temporary files, files still in use?')
		return 1

	return 0 


#	A function that returns a random post from the home page of the desired sub reddit
#	The function can return different types of data
#	TITLE: returens a string containing the random post title
#	TEXT: returns a string containing the random post title and text content if any
#	IMAGE: returns a url for the image of the post, if there is no image a url to the post is returned
#	VIDEO: downloads 
def random(sub_name=None, p_type=None, videoName=None):
	if sub_name == None:
		print("Error: no subreddit chosen")
		return -1
	
	sub_name = sub_name.strip()
	if "r/" in sub_name:
		sub_name = sub_name.replace("r/", "")
	elif "r\\" in sub_name:
		sub_name = sub_name.replace("r\\", "")

	url = "https://www.reddit.com/r/" + sub_name + "/.json?limit=100"

	req = urllib.request.Request(
		url,
		data=None,
		#	user agent to avoid erro 429
		headers={
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
		}
	)
	response = urllib.request.urlopen(req)
	data = json.loads(response.read())

	dist = data["data"]["dist"]
	rand = int(r.randint(0, dist*5000)/5000)

	post = data["data"]["children"][rand]["data"]

	if p_type == None:
		if post["selftext"] != '':
			a = data["data"]["children"][rand]["data"]["title"]
			b = data["data"]["children"][rand]["data"]["selftext"]
			a += ("\n\n" + b)

			returnValue = {"type": TEXT, "value": a}
			return returnValue
		else:
			if post["is_video"]:
				url = data["data"]["children"][rand]["data"]["permalink"]
				url = "https://www.reddit.com" + url
				videoName = str(videoName) + ".mkv"

				a = parseRedditVideo(url, videoName)
				if a == 0:
					returnValue = {"type": VIDEO, "value": videoName}
					return returnValue
			else:
				value = data["data"]["children"][rand]["data"]["url"]
				returnValue = {"type": IMAGE, "value": value}
				return returnValue

	if p_type == TITLE:
		return post["title"]
	if p_type == TEXT:
		i = 0
		while post["selftext"] == '':
			rand = int(r.randint(0, dist*5000)/5000)
			post = data["data"]["children"][rand]["data"]
			i += 1
			if i == 500:
				break
		a = post["title"]
		b = post["selftext"]
		a += ("\n\n" + b)
		returnValue = {"type": TEXT, "value": a}
		return returnValue
	if p_type == IMAGE:
		i = 0
		while post["selftext"] != '' or post["is_video"]:
			rand = int(r.randint(0, dist*5000)/5000)
			post = data["data"]["children"][rand]["data"]
			i += 1
			if i == 500:
				break
		value = post["url"]
		returnValue = {"type": IMAGE, "value": value}
		return returnValue
	if p_type == VIDEO:
		i = 0
		while not post["is_video"]:
			rand = int(r.randint(0, dist*5000)/5000)
			post = data["data"]["children"][rand]["data"]
			i += 1
			if i == 500:
				break
		url = post["permalink"]
		url = "https://www.reddit.com" + url
		videoName = str(videoName) + ".mkv"
		a = parseRedditVideo(url, videoName)
		if a == 0:
			returnValue = {"type": VIDEO, "value": videoName}
			return returnValue