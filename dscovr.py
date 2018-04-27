#!/usr/bin/python3
import json
from datetime import datetime
from os import rename
from time import strftime, sleep
from urllib.request import urlopen, URLopener
from urllib.error import HTTPError
download_directory="/home/johannes/.cache/dscovr/"
apiurl="https://epic.gsfc.nasa.gov/api/natural"
contents = urlopen(apiurl).read()
data = json.loads(contents.decode('utf-8'))
opener = URLopener()
dates = []
for image in data:
	dates.append(image['date'])
imgnum = dates.index(max(dates))
image_name = data[imgnum]['image'] + '.png'
imgpath = download_directory + image_name
imgurl1="https://epic.gsfc.nasa.gov/archive/natural/" + strftime("%Y/%m/") + str(datetime.now().day - 2) + "/png/" 
imgurl2="https://epic.gsfc.nasa.gov/archive/natural/" + strftime("%Y/%m/") + str(datetime.now().day - 1) + "/png/"
imgurl3="https://epic.gsfc.nasa.gov/archive/natural/" + strftime("%Y/%m/") + str(datetime.now().day - 0) + "/png/" 
check = 0
try:
	opener.retrieve(imgurl2 + image_name, imgpath)
	check = 1
except HTTPError:
	print("Nicht Gestern")
if not check:
	try:
		opener.retrieve(imgurl1 + image_name, imgpath)
		check = 1
	except HTTPError:
		print("Nicht Vorgestern")
if not check:
	try:
		opener.retrieve(imgurl3 + image_name, imgpath)
		check = 1
	except HTTPError:
		print("Nicht Heute")
if check:
	rename(imgpath, download_directory + 'latest.png')
	print(image_name)