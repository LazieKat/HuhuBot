##############################################
#               HuhuBot v1.0                 #
#            github.com/aziad1998            #
#  HuhuBot is a telegram bot I wrotefor fun  #
#  For functionality send the command /help  #
##############################################

import json, requests, random
import telegram as t
import telegram.ext as te

#	open bot token file
TOKEN = open("token", "r").read()

#	global history array to save sent messages IDs
history = dict()

#	global variables for cards agains humanity
cards_num = dict()
fulldeck = json.load(open("cah.json", "r"))
black_cards = fulldeck["blackCards"]
white_cards = fulldeck["whiteCards"]

#	dad jokes
def dad(bot: t.Bot, context: t.update):
	url = "https://icanhazdadjoke.com/slack"
	response = requests.get(url).json()
	joke = response['attachments'][0]['text']
	msg_info = bot.send_message(
		chat_id=ccid(context),
		text=joke
	)

	saveHistory(msg_info)
	cid = icid(msg_info)
	print("dad joke sent", cid, history[cid][-1], sep="\t")

#	get chat id from a message info
def icid(msg_info):
	return msg_info['chat']['id']

def ccid(context: t.update):
	return context.message.chat_id

#	saving messages IDs from their returned info
def saveHistory(msg_info):
	cid = icid(msg_info)
	while True:
		try:
			history[cid].append(msg_info['message_id'])
			break
		except KeyError:
			history[cid] = list()

#	features testing function
def test(bot: t.Bot, context: t.update):
	msg_info = bot.sendMessage(
		chat_id=ccid(context),
		text="test"
	)

	saveHistory(msg_info)
	cid = icid(msg_info)
	print("test message sent", cid, history[cid][-1], sep="\t")

#	send cute anime girls pics
def cute(bot: t.Bot, context: t.update):
	url = "http://api.cutegirls.moe/json"
	response = requests.get(url).json()
	img_url = response['data']['image']
	msg_info = bot.send_photo(
		chat_id=ccid(context),
		photo=img_url
	)

	saveHistory(msg_info)
	cid = icid(msg_info)
	print("moe photo sent", cid, history[cid][-1], sep="\t")

#	remove last message in history array
def rem(bot: t.Bot, context: t.update):
	cid = ccid(context)
	mid = history[cid].pop()
	bot.delete_message(
		chat_id=cid,
		message_id=mid
	)
	print("message deleted", cid, mid, sep="\t")

#	display help message of the bot	
def help(bot: t.Bot, context: t.update):
	msg_info = bot.send_message(
		chat_id=ccid(context),
		text="Hi, I am HuhuBot\nThose are my commands so far\n"
		"/help to display this message\n"
		"/cute to send a cute girl pic\n"
		"/rem to remove the last message I sent\n"
		"/test is just for testing stuf\n"
		"/cah play cards against humanity\n"
		"/dad send a dad joke\n"
	)

	saveHistory(msg_info)
	cid = icid(msg_info)
	print("help message sent", cid, history[cid][-1], sep="\t")

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
		msg_info = bot.send_message(
			chat_id=cid,
			text=content
		)

		saveHistory(msg_info)
		print("black card sent", cid, history[cid][-1], sep="\t")
	else:
		for i in range(cards_num[cid]):
			card = int(random.randint(0,229500)/500)
			content = white_cards[card]
			msg_info = bot.send_message(
				chat_id=cid,
				text=content
			)

			saveHistory(msg_info)
			print("white card sent", cid, history[cid][-1], sep="\t")
		cards_num[cid] = 0

#	starting point
if __name__ == "__main__":
	#	create updater and dispatcher objects
	print("Bot is starting up...")
	updater = te.Updater(token=TOKEN)
	print("updater object created")
	dispatcher = updater.dispatcher
	print("dispatcher object created\n")

	#	create commands handlers
	test_h = te.CommandHandler("test", test)
	dispatcher.add_handler(test_h)
	print("/test\tcommand handler created")

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

	#	start polling updates
	updater.start_polling()
	print("\npolling started\n_______________\n")