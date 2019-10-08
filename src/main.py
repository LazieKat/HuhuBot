###############################################
#               HuhuBot v1.5.1                #
#            github.com/aziad1998             #
###############################################


import config, commands
import telegram as t
import telegram.ext as te


def main():
	print("Bot is starting up...")
	updater = te.Updater(token=config.token)
	print("updater object created")
	dispatcher = updater.dispatcher
	print("dispatcher object created\n")

	#	Commands handlers
	help_h = te.CommandHandler("help", commands.help)
	dispatcher.add_handler(help_h)
	print("/help\tcommand handler created")

	start_h = te.CommandHandler("start", commands.help)
	dispatcher.add_handler(start_h)
	print("/start\tcommand handler created")

	cute_h = te.CommandHandler("cute", commands.cute)
	dispatcher.add_handler(cute_h)
	print("/cute\tcommand handler created")

	rem_h = te.CommandHandler("rem", commands.rem)
	dispatcher.add_handler(rem_h)
	print("/rem\tcommand handler created")

	cah_h = te.CommandHandler("cah", commands.cah)
	dispatcher.add_handler(cah_h)
	print("/cah\tcommand handler created")

	dad_h = te.CommandHandler("dad", commands.dad)
	dispatcher.add_handler(dad_h)
	print("/dad\tcommand handler created")

	hor_h = te.CommandHandler("hor", commands.horror)
	dispatcher.add_handler(hor_h)
	print("/hor\tcommand handler created")

	meme_h = te.CommandHandler("meme", commands.meme)
	dispatcher.add_handler(meme_h)
	print("/meme\tcommand handler created")

	pun_h = te.CommandHandler("pun", commands.pun)
	dispatcher.add_handler(pun_h)
	print("/pun\tcommand handler created")

	shower_h = te.CommandHandler("shower", commands.shower)
	dispatcher.add_handler(shower_h)
	print("/shower\tcommand handler created")

	reddit_h = te.CommandHandler("reddit", commands.selective_reddit, pass_args=True)
	dispatcher.add_handler(reddit_h)
	print("/reddit\tcommand handler created")

	#	Start polling
	updater.start_polling()
	print("\npolling started\n_______________\n")


if __name__ == "__main__":
	main()