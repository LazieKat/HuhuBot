import json, requests, random
import telegram as t
import telegram.ext as te

#	open bot token file
TOKEN = open("token", "r").read()

#	global history array to save sent messages IDs
history = [[],[]]

#	global variables for cards agains humanity
cards_num = 0
fulldeck = json.load(open("cah.json", "r"))
black_cards = fulldeck["blackCards"]
white_cards = fulldeck["whiteCards"]

#	saving messages IDs from their returned info
def saveHistory(msg_info):
	history[0].append(msg_info['chat']['id'])
	history[1].append(msg_info['message_id'])

#	features testing function
def test(bot: t.Bot, context: t.update):
	rk = [["nibba", "human", "lol", "helicopter"]]
	msg_info = bot.send_message(
		chat_id=context.message.chat_id, 
		text="hello\nWhat's your religion", 
		reply_markup=t.replykeyboardmarkup.ReplyKeyboardMarkup(rk, one_time_keyboard=True)
	)

	saveHistory(msg_info)
	print("test message sent", history[0][-1], history[1][-1], sep="\t")

#	send cute anime girls pics
def cute(bot: t.Bot, context: t.update):
	url = "http://api.cutegirls.moe/json"
	response = requests.get(url).json()
	img_url = response['data']['image']
	msg_info = bot.send_photo(
		chat_id=context.message.chat_id,
		photo=img_url
	)

	saveHistory(msg_info)
	print("moe photo sent", history[0][-1], history[1][-1], sep="\t")

#	remove last message in history array
def rem(bot: t.Bot, context: t.update):
	cid = history[0].pop()
	mid = history[1].pop()
	bot.delete_message(
		chat_id=cid,
		message_id=mid
	)
	print("message deleted", cid, mid, sep="\t")

#	display help message of the bot	
def help(bot: t.Bot, context: t.update):
	msg_info = bot.send_message(
		chat_id=context.message.chat_id,
		text="Hi, I am HuhuBot\nThose are my commands so far\n"
		"/help to display this message\n"
		"/cute to send a cute girl pic\n"
		"/rem to remove the last message I sent\n"
		"/test is just for testing stuf\n"
	)

	saveHistory(msg_info)
	print("help message sent", history[0][-1], history[1][-1], sep="\t")

#	display a card against humanity 
def cah(bot: t.Bot, context: t.update):
	global cards_num
	if cards_num == 0:
		card = int(random.randint(0,445000)/5000)
		content = black_cards[card]["text"]
		cards_num = black_cards[card]["pick"]
		msg_info = bot.send_message(
			chat_id=context.message.chat_id,
			text=content
		)

		saveHistory(msg_info)
		print("black card sent", history[0][-1], history[1][-1], sep="\t")
	else:
		for i in range(cards_num):
			card = int(random.randint(0,229500)/500)
			content = white_cards[card]
			msg_info = bot.send_message(
				chat_id=context.message.chat_id,
				text=content
			)

			saveHistory(msg_info)
			print("white card sent", history[0][-1], history[1][-1], sep="\t")
		cards_num = 0

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

	#	start polling updates
	updater.start_polling()
	print("\npolling started\n_______________\n")