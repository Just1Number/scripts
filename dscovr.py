#!/usr/bin/python3
import argparse
import json
from datetime import datetime
from os import rename, getcwd, path
from urllib.request import urlopen, URLopener
from urllib.error import HTTPError

parser = argparse.ArgumentParser()
parser.add_argument("-o", dest = "output_dir", help = "set output directory", default = getcwd())
args = parser.parse_args()

if path.isdir(args.output_dir):
  if args.output_dir[len(args.output_dir)-1] == "/":
    DOWNLOAD_DIRECTORY = args.output_dir
  else:
    DOWNLOAD_DIRECTORY = args.output_dir + "/"
else:
  print("Output directory invalid. Check if it exists")
  exit()

# Constants
API_URL = "https://epic.gsfc.nasa.gov/api/natural"
IMAGE_SOURCE = "https://epic.gsfc.nasa.gov/archive/natural/"

# Parsing api 
contents = bytes(0)
try:
  contents = urlopen(API_URL).read()
except:
  print("Cannot connect to API at " + API_URL)
  print("Check your internet connection")
  exit()
data = json.loads(contents.decode('utf-8'))
opener = URLopener()

image_times = []
tsnow = datetime.utcnow().timestamp()

for meta in data:
  # convert json date into python time object, ignoring the date
  t = datetime.strptime(meta['date'], "%Y-%m-%d %H:%M:%S").time()
  # set date to today
  dt = datetime.combine(datetime.fromtimestamp(tsnow).date(), t)
  # return to timestamp
  ts = dt.timestamp()
  image_times.append(ts)

# handle the special case of tsnow being in between the last and the first image of the day
if tsnow < image_times[0]:
  image_times[len(image_times) - 1] -= 24 * 3600
elif tsnow > image_times[len(image_times) - 1]:
  image_times[0] += 24*3600

diffs = []
for ts in image_times:
  diff = abs( tsnow - ts )
  diffs.append(diff)

# choosing image by index. picking a picture taken close to the current daytime
index = diffs.index(min(diffs))
image_name = data[index]['image'] + '.png' # epic_1b_20180630224431.png
image_id = data[index]['identifier'] # 20180630224431
image_path = DOWNLOAD_DIRECTORY + image_name
image_url = IMAGE_SOURCE + image_id[:4] + "/" + image_id[4:6] + "/" + image_id[6:8] + "/png/"
# https://epic.gsfc.nasa.gov/archive/natural/2018/06/30/png/epic_1b_20180630224431.png

# check if metadata file exists
metadata = DOWNLOAD_DIRECTORY + "image_info.epic"
if path.exists(metadata):
  # read filename of last image 
  # and skip download if it is the same as the current one
  rf = open(metadata, "r")
  old_image = rf.read()
  rf.close()
  if old_image == image_name:
    print(image_name + " is already on local maschine. Skipping download.")
    exit()

try:
  opener.retrieve(image_url + image_name, image_path)
except:
  print("Download failed")
  print(image_url + image_name)
  exit()

# write current image_name to the metadata file
wf = open(metadata, "w")
wf.write(image_name)
wf.close()

rename(image_path, DOWNLOAD_DIRECTORY + 'epic.png')
print(image_name + " downloaded")
