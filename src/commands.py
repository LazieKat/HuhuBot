import telegram as t
import config, reddit, reqs, os

#	help command
def help(bot: t.Bot, context: t.update):
	msg_info = bot.send_message(
		chat_id=config.chat_id(context=context),
		text="Hi, I am HuhuBot 1.5.2"
		"\nThose are my commands:\n"
		"/help to display this message\n"
		"/rem to remove the last message sent\n"
		"/cute to send a cute girl pic\n"
		"/cah play cards against humanity\n"
		"/dad send a dad joke\n"
		"/meme send a meme\n"
		"/hor send a two sentence horror\n"
		"/shower send a shower thought\n"
		"/pun send a pun photo\n"
		"/reddit <subreddit> send a random post from the selected subreddit\n"
		"/rvd download a reddit video from link"
	)

	config.save_history(msg_info, "help message")


#	start command
def start(bot: t.Bot, context: t.update):
	help(bot, context)


#	remove last message sent
def rem(bot: t.Bot, context: t.update):
	chat_id = config.chat_id(context=context)
	message_id = config.history[chat_id].pop()
	bot.delete_message(
		chat_id=chat_id,
		message_id=message_id
	)

	print("message deleted\t", chat_id, message_id, sep="\t")


#	send a shower thought
def shower(bot: t.Bot, context: t.update):
	sentence = reddit.random("showerthoughts", reddit.TEXT)["value"]
	msg_info = bot.send_message(
		chat_id=config.chat_id(context=context),
		text=sentence
	)

	config.save_history(msg_info, "shower thought")


#	send a pun image
def pun(bot: t.Bot, context: t.update):
	img_url = reddit.random("puns", reddit.IMAGE)["value"]
	msg_info = bot.send_photo(
		chat_id=config.chat_id(context=context),
		photo=img_url
	)

	config.save_history(msg_info, "pun")


#	send a meme
def meme(bot: t.Bot, context: t.update):
	sub_name = "memes"
	if reddit.r.randint(1,2) == 2:
		sub_name = "dankmemes"
	img_url = reddit.random(sub_name, reddit.IMAGE)["value"]
	msg_info = bot.send_photo(
		chat_id=config.chat_id(context=context),
		photo=img_url
	)

	config.save_history(msg_info, "meme")


#	send a two sentence horror
def horror(bot: t.Bot, context: t.update):
	sentence = reddit.random("twosentencehorror", reddit.TEXT)["value"]
	msg_info = bot.send_message(
		chat_id=config.chat_id(context=context),
		text=sentence
	)

	config.save_history(msg_info, "two sentence horror")


#	send a dad joke
def dad(bot: t.Bot, context: t.update):
	sentence = reddit.random("dadjokes", reddit.TEXT)["value"]
	msg_info = bot.send_message(
		chat_id=config.chat_id(context=context),
		text=sentence
	)

	config.save_history(msg_info, "dad joke")


#	send a cute anime girl pic
def cute(bot: t.Bot, context: t.update):
	url = "http://api.cutegirls.moe/json"
	response = reqs.json_url(url)
	img_url = response["data"]["image"]
	msg_info = bot.send_photo(
		chat_id=config.chat_id(context=context),
		photo=img_url
	)

	config.save_history(msg_info, "cute photo")


sent_video_count = 0
#	reddit video downloader
def rvd(bot: t.Bot, context: t.update, args):
	global sent_video_count

	params = []
	for arg in args:
		params.append(arg)

	url = params[0]
	path= "./"+ str(sent_video_count) + ".mp4"
	reddit.download_video(url, path)
	
	try:
		video=open(path, "rb")
		msg_info = bot.send_video(
			chat_id=config.chat_id(context=context),
			video=video,
			supports_streaming=True
		)

		config.save_history(msg_info, "rvd")
	except Exception as e:
		print(f"{type(e).__name__}\t {e}")
	finally:
		sent_video_count += 1
		video.close()
		os.remove(path)


#	selective reddit command
def selective_reddit(bot: t.Bot, context: t.update, args):
	global sent_video_count

	params = []
	for arg in args:
		params.append(arg)
	try:
		params[1]
		post_type = True
	except IndexError:
		post_type = None

	sub_name = str(params[0]).lower()
	if post_type == True:
		post_type = str(params[1]).lower()

	if post_type == None:
		request = reddit.random(sub_name=sub_name, post_type=None, video_name=sent_video_count)
	elif post_type == "image" or post_type == "photo":
		request = reddit.random(sub_name=sub_name, post_type=reddit.IMAGE)
	elif post_type == "text":
		request = reddit.random(sub_name=sub_name, post_type=reddit.TEXT)
	elif post_type == "video":
		request = reddit.random(sub_name=sub_name, post_type=reddit.VIDEO)

	post_type = request["type"]
	message = request["value"]

	if post_type == reddit.IMAGE:
		msg_info = bot.send_photo(
			chat_id=config.chat_id(context=context),
			photo=message
		)
	elif post_type == reddit.VIDEO:
		try:
			video=open(path, "rb")
			msg_info = bot.send_video(
				chat_id=config.chat_id(context=context),
				video=video,
				supports_streaming=True
			)
		except Exception as e:
			print(f"{type(e).__name__}\t {e}")
		finally:
			sent_video_count += 1
			video.close()
			os.remove(message)
	else:
		msg_info = bot.send_message(
			chat_id=config.chat_id(context=context),
			text=message
		)

	config.save_history(msg_info, "selective reddit")


#	cards agains humanity
cards_num = dict()
fulldeck = reqs.json_url("https://raw.githubusercontent.com/crhallberg/json-against-humanity/master/full.md.json")
black_cards = fulldeck["black"]
white_cards = fulldeck["white"]

def cah(bot: t.Bot, context: t.update):
	global cards_num
	chat_id = config.chat_id(context=context)

	try:
		cards_num[chat_id]
	except KeyError:
		cards_num[chat_id] = 0

	if cards_num[chat_id] == 0:
		card = int(reddit.r.randint(0, 1480500)/500)
		content = str(black_cards[card]["text"]).replace("_", "___")
		cards_num[chat_id] = black_cards[card]["pick"]
		msg_info = bot.send_message(
			chat_id=chat_id,
			text=content
		)

		config.save_history(msg_info, "black card")
	else:
		for i in range(cards_num[chat_id]):
			card = int(reddit.r.randint(0, 4059000)/500)
			content = white_cards[card]["text"]
			msg_info = bot.send_message(
				chat_id=chat_id,
				text=content
			)

			config.save_history(msg_info, "white card")
		cards_num[chat_id] = 0
