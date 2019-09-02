import json
import urllib.request as q

#	Return json file from a url as a dictionary

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