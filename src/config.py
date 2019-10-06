import telegram as t

#	config variables
token = open("token", "r").read()
history = dict()


#	get the chat id from context or messsage info
def chat_id(msg_info=None, context=None):
	if msg_info != None:
		return msg_info['chat']['id']
	else:
		return context.message.chat_id

#	save a message in history using message info
def save_history(msg_info, log=''):
	cid = chat_id(msg_info=msg_info)
	while True:
		try:
			history[cid].append(msg_info['message_id'])
			break
		except KeyError:
			history[cid] = list()
	print(log, "sent", cid, history[cid][-1], sep="\t")