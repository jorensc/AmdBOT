import requests
from datetime import datetime as d
from bs4 import BeautifulSoup
import time
import re
import hashlib

oldInfo = ""
totalInfo = ""
# Role to ping here
roleID = "826952371841138739"

def discordWebook(message, isGpu):
	cloc = d.utcnow()
	cloc = cloc.strftime("%Y-%m-%dT%H:%M:%S.000Z")
	# Discord webhook here
	url = ""
	if isGpu:
		payload = {
		"content":f"||<@&{roleID}>||",
		"embeds": [
    	    {
    	    	"author": {
    	            "name": "AMD STOCK CHECKER",
    	            "url": "https://www.amd.com/en/direct-buy/be",
    	            "icon_url": "https://logodix.com/logo/606655.png"
    	        },
    	        "description": message,
    	        "timestamp": cloc,
    	        "color": 16711680,
    	        "footer": {
    	        	"text": "By Tiddo and Joren"
    	        }
    	    }
    	]}
	else:
		payload = {"embeds": [
    	    {
    	    	"author": {
    	            "name": "AMD STOCK CHECKER",
    	            "url": "https://www.amd.com/en/direct-buy/be",
    	            "icon_url": "https://logodix.com/logo/606655.png"
    	        },
    	        "description": message,
    	        "timestamp": cloc,
    	        "color": 16711680,
    	        "footer": {
    	        	"text": "By Tiddo and Joren"
    	        }
    	    }
    	]}
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
			emoji = ":white_check_mark:"
			info = f'[{name}]({link}) {emoji}'
			hasGpu = True
		else:
			status = "In stock"
			emoji = ":white_check_mark:"
			info = f'[{name}]({link}) {emoji}'
			hasGpu = False
	elif "Out of Stock" in str(status):
		status = "Out of Stock"
		emoji = ":x:"
		link = "Imagine_discord_mobile_noob"
		info = f'{name} {emoji}'
		hasGpu = False
	return info, hasGpu

	
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

while True:
	gpuAv = False
	items = reqAmd()
	for item in items:
		# name, status, link, emoji = getInfo(item)
		info, hasGpu = getInfo(item)
		if hasGpu:
			gpuAv = True
		# info = f'Name: {name}\nStatus: {status}\nLink: {link}'
		# info = f'[{name}]({link}) {emoji}'
		totalInfo = totalInfo + info + "\n"
	if totalInfo != oldInfo:
		discordWebook(totalInfo, gpuAv)
		print(totalInfo)
		oldInfo = totalInfo
		totalInfo = ""
	else:
		print("Already send")	
		totalInfo = ""
	
	time.sleep(60)