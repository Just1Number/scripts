#!/usr/bin/python3
import json
from datetime import datetime
from os import rename
from urllib.request import urlopen, URLopener
from urllib.error import HTTPError
from random import randint

# Constants
download_directory = "/home/johannes/.cache/dscovr/"
api_url = "https://epic.gsfc.nasa.gov/api/natural"
image_source = "https://epic.gsfc.nasa.gov/archive/natural/"

# Parsing api 
contents = urlopen(api_url).read()
data = json.loads(contents.decode('utf-8'))
opener = URLopener()

# choosing image by index. picking a picture taken close to the current daytime
index = int(datetime.now().hour/ 24.0 * len(data)) # dates.index(max(dates))
image_name = data[index]['image'] + '.png' # epic_1b_20180630224431.png
image_id = data[index]['identifier'] # 20180630224431
image_path = download_directory + image_name
image_url = image_source + image_id[:4] + "/" + image_id[4:6] + "/" + image_id[6:8] + "/png/"
# https://epic.gsfc.nasa.gov/archive/natural/2018/06/30/png/epic_1b_20180630224431.png
check = 0
try:
	opener.retrieve(image_url + image_name, image_path)
	check = 1
except HTTPError:
	print(image_url + image_name)
if check:
	rename(image_path, download_directory + 'latest_epic.png')
	print(image_name)
