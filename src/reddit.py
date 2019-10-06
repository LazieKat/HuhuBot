import reqs, re, tempfile, ffmpy, os
import random as r

TITLE = 0
TEXT = 1
IMAGE = 2
VIDEO = 3

#	A function to download audio and video of a reddit post and combine them
#	returns 0 on success and 1 on error
def download_video(url: str, path: str):
	#	append /.json to the url
	if not url.endswith('/'):
		url += '/'
	url += '.json'

	response = reqs.json_url(url=url)

	#	This will fail if url is not from reddit or is not a video
	try:
		is_video = response[0]['data']['children'][0]['data']['is_video']
		if not is_video:
			return 1
	except:
		return 1
	
	#	parse audio/video info
	mpd_list_link = response[0]['data']['children'][0]['data']['media']['reddit_video']['dash_url']
	mpd_response = reqs.get(url=mpd_list_link)
	mpd_xml = mpd_response.text

	#	get links for audio and video
	base_link = response[0]['data']['children'][0]['data']['url']
	data = re.findall('<BaseURL>(.*?)</BaseURL>', mpd_xml)
	hq_video_link = base_link + '/' + data[0]
	audio_link = base_link + '/' + data[-1]

	temp_dir = tempfile.gettempdir()
	temp_video_dir = temp_dir + '/' + next(tempfile._get_candidate_names())
	temp_audio_dir = temp_dir + '/' + next(tempfile._get_candidate_names())

	#	store data in temp files
	reqs.ulibreq.urlretrieve(hq_video_link, temp_video_dir)
	reqs.ulibreq.urlretrieve(audio_link, temp_audio_dir)

	ff = ffmpy.FFmpeg(
		inputs={
			temp_video_dir: None,
			temp_audio_dir: None
		},
		outputs={
			path: " -c copy"
		}
	)

	#	failsafe
	try:
		ff.run()
		os.remove(temp_audio_dir)
		os.remove(temp_video_dir)
	except ffmpy.FFRuntimeError:
		return 1
		
	return 0


#	return a the title and selftext of a post
def text(post: dict):
	text = post["title"] + "\n\n" + post["selftext"]
	return_value = {
		"type": TEXT,
		"value": text
	}
	return return_value


#	return video name of downloaded post video
def video(post: dict, video_name):
	url = "https://www.reddit.com" + post["permalink"]
	video = str(video_name) + ".mp4"

	video_parse = download_video(url=url, path=video)
	if video_parse != 0:
		return 1
	return_value = {
		"type": VIDEO,
		"value": video
	}
	return return_value


#	return image url of a post
def image(post: dict):
	return_value = {
		"type": IMAGE,
		"value": post["url"]
	}
	return return_value


#	Ruturn a a random post from a selected subreddit
#	returns specific type is pormpted
def random(sub_name: str, post_type=None, video_name=None):
	sub_name = sub_name.strip()
	if "r/" in sub_name or "r\\" in sub_name:
		sub_name = sub_name.replace("r" + sub_name[1], "")
	
	url = "https://www.reddit.com/r/" + sub_name + "/.json?limit=100"
	data = reqs.json_url(url)

	posts_amount = data["data"]["dist"]

	text_posts = []
	image_posts = []
	video_posts = []

	for i in range(0, posts_amount):
		post = data["data"]["children"][i]["data"]
		if post["selftext"] != "":
			text_posts.append(i)
			continue
		elif post["is_video"]:
			video_posts.append(i)
			continue
		else:
			image_posts.append(i)
			continue

	rand = int(r.randint(0, posts_amount*5000)/5000)
	post = data["data"]["children"][rand]["data"]

	if post_type == None:
		if post["selftext"] != "":
			return text(post)
		elif post["is_video"]:
			return video(post, video_name)
		else:
			return image(post)
	elif post_type == TITLE:
		return post["title"]
	elif post_type == TEXT:
		rand = r.randint(0, text_posts.__len__())
		post = data["data"]["children"][text_posts[rand]]["data"]
		return text(post)
	elif post_type == VIDEO:
		rand = r.randint(0, video_posts.__len__())
		post = data["data"]["children"][video_posts[rand]]["data"]
		return video(post, video_name)
	else:
		rand = r.randint(0, image_posts.__len__())
		post = data["data"]["children"][image_posts[rand]]["data"]
		return image(post)