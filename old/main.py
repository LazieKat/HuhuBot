##############################################
#               HuhuBot v1.5                 #
#            github.com/aziad1998            #
#  HuhuBot is a telegram bot I wrotefor fun  #
#  For functionality send the command /help  #
##############################################


import random, redditParser, os, json
import telegram as t
import telegram.ext as te
import urllib.request as q


################# Coniguration variables

#	open bot token file
TOKEN = open("token", "r").read()

#	global history array to save sent messages IDs
history = dict()

#	global counter for video sending
sentVideoCounter = 0


################# Coniguration and generic funcs

#	get chat id from a message info
def icid(msg_info):
	return msg_info['chat']['id']

#	fet chat id from context
def ccid(context: t.update):
	return context.message.chat_id

#	saving messages IDs from their returned info
def saveHistory(msg_info, log: str):
	cid = icid(msg_info)
	while True:
		try:
			history[cid].append(msg_info['message_id'])
			break
		except KeyError:
			history[cid] = list()
	print(log, "sent", cid, history[cid][-1], sep="\t")


def load(url: str):
	req = q.Request(
		url,
		data=None,
		#	user agent to avoid erro 429
		headers={
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
		}
	)
	response = q.urlopen(req)
	return json.loads(response.read())

def readFile(path: str, type: str):
	return json.load(open(path, type))


################# Bot commands' funcs


#	remove last message in history array
def rem(bot: t.Bot, context: t.update):
	cid = ccid(context)
	mid = history[cid].pop()
	bot.deleteMessage(
		chat_id=cid,
		message_id=mid
	)
	print("message deleted\t", cid, mid, sep="\t")

#	send a shower thought
def shower(bot: t.Bot, context: t.update):
	sentence = redditParser.random("Showerthoughts", redditParser.TEXT)
	sentence = sentence["value"]
	msg_info = bot.sendMessage(
		chat_id=ccid(context),
		text=sentence
	)

	saveHistory(msg_info, "Shower thought")

#	send a pun
def pun(bot: t.Bot, context: t.update):
	img_url = redditParser.random("puns", redditParser.IMAGE)
	img_url = img_url["value"]
	msg_info = bot.sendPhoto(
		chat_id=ccid(context),
		photo=img_url
	)

	saveHistory(msg_info, "Pun")

#	send a meme
def meme(bot: t.Bot, context: t.update):
	sub_name = "memes"
	if random.randint(1,2) == 2:
		sub_name = "dankmemes"
	img_url = redditParser.random(sub_name, redditParser.IMAGE)
	img_url = img_url["value"]
	msg_info = bot.sendPhoto(
		chat_id=ccid(context),
		photo=img_url
	)

	saveHistory(msg_info, "Meme")

#	two sentence horror
def hor(bot: t.Bot, context: t.update):
	sentence = redditParser.random("TwoSentenceHorror", redditParser.TEXT)
	sentence = sentence["value"]
	msg_info = bot.sendMessage(
		chat_id=ccid(context),
		text=sentence
	)

	saveHistory(msg_info, "TwoSentenceHorror")

#	dad jokes
def dad(bot: t.Bot, context: t.update):
	joke = redditParser.random("dadjokes", redditParser.TEXT)
	joke = joke["value"]
	msg_info = bot.sendMessage(
		chat_id=ccid(context),
		text=joke
	)

	saveHistory(msg_info, "dad joke")


#	send cute anime girls pics
def cute(bot: t.Bot, context: t.update):
	url = "http://api.cutegirls.moe/json"
	response = load(url)
	img_url = response['data']['image']
	msg_info = bot.sendPhoto(
		chat_id=ccid(context),
		photo=img_url
	)

	saveHistory(msg_info, "cute photo")

#	global variables for cards agains humanity
cards_num = dict()
fulldeck = readFile("cah.json", "r")
black_cards = fulldeck["blackCards"]
white_cards = fulldeck["whiteCards"]
#	display a card against humanity 
def cah(bot: t.Bot, context: t.update):
	global cards_num
	cid = ccid(context)
	
	#	check if this chat has been initilized to play cah
	try:
		cards_num[cid]
	except KeyError:
		cards_num[cid] = 0

	#	what cards to send
	if cards_num[cid] == 0:
		card = int(random.randint(0,445000)/5000)
		content = black_cards[card]["text"]
		cards_num[cid] = black_cards[card]["pick"]
		msg_info = bot.sendMessage(
			chat_id=cid,
			text=content
		)

		saveHistory(msg_info, "black card")
	else:
		for i in range(cards_num[cid]):
			card = int(random.randint(0,229500)/500)
			content = white_cards[card]
			msg_info = bot.sendMessage(
				chat_id=cid,
				text=content
			)

			saveHistory(msg_info, "white card")
		cards_num[cid] = 0

#	display help message of the bot	
def help(bot: t.Bot, context: t.update):
	msg_info = bot.sendMessage(
		chat_id=ccid(context),
		text="Hi, I am HuhuBot 1.5"
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
		"/reddit <subreddit> send a random post from the selected subreddit"
	)

	saveHistory(msg_info, "help message")

#	selective reddit parser
def reddit(bot: t.Bot, context: t.update, args):
	global sentVideoCounter
	cid = ccid(context)

	params = []
	for arg in args:
		params.append(arg)
	try:
		params[1]
	except IndexError:
		params.append(None)

	s_name = str(params[0]).lower()
	p_type = params[1]

	if p_type == None:
		request = redditParser.random(sub_name=s_name, p_type=None, videoName=sentVideoCounter)
	elif str(p_type).lower() == "image" or str(params[1]).lower() == "photo":
		parse_type = redditParser.IMAGE
		request = redditParser.random(sub_name=s_name, p_type=parse_type)
	elif str(p_type).lower() == "text":
		parse_type = redditParser.TEXT
		request = redditParser.random(sub_name=s_name, p_type=parse_type)
	elif str(p_type).lower() == "video":
		parse_type = redditParser.VIDEO
		request = redditParser.random(sub_name=s_name, p_type=parse_type, videoName=sentVideoCounter)
	else:
		parse_type = redditParser.TITLE
		request = redditParser.random(sub_name=s_name, p_type=parse_type)

	parse_type = request["type"]
	message = request["value"]

	if parse_type == redditParser.IMAGE:
		msg_info = bot.sendPhoto(
			chat_id=cid,
			photo=message
		)
	elif parse_type == redditParser.VIDEO:
		msg_info = bot.sendVideo(
			chat_id=cid,
			video=open(message, 'rb'),
			supports_streaming=True
		)
		sentVideoCounter += 1
		os.remove(message)
	else:
		msg_info = bot.sendMessage(
			chat_id=cid,
			text=message
		)	
	saveHistory(msg_info, "selective reddit")


################# Starting point


if __name__ == "__main__":
	#	create updater and dispatcher objects
	print("Bot is starting up...")
	updater = te.Updater(token=TOKEN)
	print("updater object created")
	dispatcher = updater.dispatcher
	print("dispatcher object created\n")

	#	create commands handlers
	help_h = te.CommandHandler("help", help)
	dispatcher.add_handler(help_h)
	print("/help\tcommand handler created")

	cute_h = te.CommandHandler("cute", cute)
	dispatcher.add_handler(cute_h)
	print("/cute\tcommand handler created")

	rem_h = te.CommandHandler("rem", rem)
	dispatcher.add_handler(rem_h)
	print("/rem\tcommand handler created")

	cah_h = te.CommandHandler("cah", cah)
	dispatcher.add_handler(cah_h)
	print("/cah\tcommand handler created")

	dad_h = te.CommandHandler("dad", dad)
	dispatcher.add_handler(dad_h)
	print("/dad\tcommand handler created")

	hor_h = te.CommandHandler("hor", hor)
	dispatcher.add_handler(hor_h)
	print("/hor\tcommand handler created")

	meme_h = te.CommandHandler("meme", meme)
	dispatcher.add_handler(meme_h)
	print("/meme\tcommand handler created")

	pun_h = te.CommandHandler("pun", pun)
	dispatcher.add_handler(pun_h)
	print("/pun\tcommand handler created")

	shower_h = te.CommandHandler("shower", shower)
	dispatcher.add_handler(shower_h)
	print("/shower\tcommand handler created")

	reddit_h = te.CommandHandler("reddit", reddit, pass_args=True)
	dispatcher.add_handler(reddit_h)
	print("/reddit\tcommand handler created")

	#	start polling updates
	updater.start_polling()
	print("\npolling started\n_______________\n")