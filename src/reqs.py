import json, requests
import urllib.request as ulibreq


#	load a json file from url and return it as a dict
def json_url(url: str):
	request = ulibreq.Request(
		url,
		data=None,
		headers={
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0"
		}
	)
	response = ulibreq.urlopen(request)
	return_value = json.loads(response.read())
	return return_value


#	load a json file from a local file and return it as a dict
def json_file(path: str, mode: str):
	j_file = open(path, mode)
	return_value = json.load(j_file)
	return return_value


#	get data from a url
def get(url: str):
	return_value = requests.get(
		url=url,
		headers={
			'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
		}
	)
	return return_value