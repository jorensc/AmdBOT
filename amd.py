import requests
from bs4 import BeautifulSoup
import time
import re
import hashlib

totalInfo = ""

def discordWebook(message):
	url = "https://discord.com/api/webhooks/822966258592383016/mSYQWmpeaOK6-73SYHneBgFxPZEkjJLhQTI5Sgp6amEjum2fyxpxsuymIuoWyKscdaQS"
	payload = {"content": message}
	headers = {
	    "Content-Type": "application/json"
	}
	response = requests.request("POST", url, json=payload, headers=headers)

def getInfo(item):
	soup = BeautifulSoup(str(item), 'html.parser')
	name = (soup.find("div", {"class": "shop-title"})).get_text().strip()
	status = (soup.find("div", {"class": "shop-links"}))
	link = soup.find("div", {"class": "shop-full-specs-link"})
	soup = BeautifulSoup(str(link), 'html.parser')
	for link in soup.find_all('a'):
		link = "https://amd.com" + link.get('href')
	if "Add to cart" in str(status):
		if "Graphics" in name:
			status = "In stock"
			emoji = ":white_check_mark: <@&826952371841138739>"
		else:
			status = "In stock"
			emoji = ":white_check_mark:"
	elif "Out of Stock" in str(status):
		status = "Out of Stock"
		emoji = ":x:"
		link = ""
	return name, status, link, emoji

	
def reqAmd():
	url = "https://www.amd.com/en/direct-buy/be"
	headers = {
	    "cookie": "pmuser_country=be",
	    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0"
	}
	response = requests.request("GET", url, headers=headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	items = soup.find_all("div", {"class": "direct-buy"})
	return items

items = reqAmd()
for item in items:
	name, status, link, emoji = getInfo(item)
	# info = f'Name: {name}\nStatus: {status}\nLink: {link}'
	info = f'{name} {emoji} {link}'
	print(info)
	totalInfo = totalInfo + info + "\n"

discordWebook(totalInfo)