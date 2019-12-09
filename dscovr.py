#!/usr/bin/python3
import argparse
import json
from datetime import datetime
from datetime import timedelta
from os import rename, getcwd, path
from urllib.request import urlopen, URLopener
from urllib.error import HTTPError
from subprocess import run, SubprocessError

parser = argparse.ArgumentParser()
parser.add_argument("-o", dest = "output_dir", help = "set output directory", default = getcwd())
parser.add_argument("-n", dest = "pics_per_day", type = int, help = "use a day with at least PICS_PER_DAY pictures", default = 1)
parser.add_argument("-c", dest = "geometry", help = "crop image to geometry", default = "")
args = parser.parse_args()

if path.isdir(args.output_dir):
    DOWNLOAD_DIRECTORY = args.output_dir
else:
  print("Output directory invalid. Check if it exists")
  exit(1)

# Constants
API_URL_BASE = "https://epic.gsfc.nasa.gov/api/natural/date/"
IMAGE_SOURCE = "https://epic.gsfc.nasa.gov/archive/natural/"

# EPIC is out of order, so old images from 2018 are used
dtnow = datetime.utcnow().replace(year=2018)
api_url = API_URL_BASE + dtnow.strftime("%Y-%m-%d")
# https://epic.gsfc.nasa.gov/api/natural/date/2018-06-30

# Parsing api 
contents = bytes(0)
try:
  contents = urlopen(api_url).read()
except Exception as e:
  print("Cannot connect to API at " + api_url)
  print("Check your internet connection")
  print(e)
  exit(1)
data = json.loads(contents.decode('utf-8'))

# If there are to few images per day use a previous day, that has more
d = dtnow.date()
while len(data) < args.pics_per_day:
  # go back one day
  d -= timedelta(1)
  api_url = API_URL_BASE + d.strftime("%Y-%m-%d")
  try:
    contents = urlopen(api_url).read()
  except Exception as e:
    print("Cannot connect to API at " + api_url)
    print(e)
    exit(1)
  data = json.loads(contents.decode('utf-8'))

image_times = []
# Fill image_times with all timestamps of the chosen day
for meta in data:
  # convert json date into python time object, ignoring the date
  t = datetime.strptime(meta['date'], "%Y-%m-%d %H:%M:%S").time()
  # set date to today
  dt = datetime.combine(dtnow.date(), t)
  # return to timestamp
  ts = dt.timestamp()
  image_times.append(ts)

tsnow = dtnow.timestamp()
additional_data = []
early = False
late = False
# handle the special case of tsnow being in between the last and the first image of the day
if tsnow < min(image_times):
  # if tsnow is before the first timestamp:
  # load last image of previous day, if possible
  d -= timedelta(1)
  early = True

elif tsnow > max(image_times):
  # if tsnow is after the last timestamp:
  # load first image of next day, if possible
  d += timedelta(1)
  late = True

if early or late:
  api_url = API_URL_BASE + d.strftime("%Y-%m-%d")
  try:
    contents = urlopen(api_url).read()
    additional_data = json.loads(contents.decode('utf-8'))
  except Exception as e:
    print("Cannot connect to API at " + api_url)
    print(e)  

  if len(additional_data) > 0:
    # add one image to data
    if early:
      data.append(additional_data[len(additional_data) - 1])
    elif late:
      data.append(additional_data[0])
    # append additional image's timestamp to image_times
    # convert json date into python time object, ignoring the date
    t = datetime.strptime(data[len(data) - 1]['date'], "%Y-%m-%d %H:%M:%S").time()
    # set date to today
    dt = datetime.combine(dtnow.date(), t)
    # return to timestamp
    if early:
      ts = dt.timestamp() - (24 * 3600)
    elif late:
      ts = dt.timestamp() + (24 * 3600)
    image_times.append(ts)

diffs = []
for ts in image_times:
  diff = abs( tsnow - ts )
  diffs.append(diff)

# choosing image by index. picking a picture taken close to the current daytime
index = diffs.index(min(diffs))
image_name = data[index]['image'] + '.png' # epic_1b_20180630224431.png
image_id = data[index]['identifier'] # 20180630224431
image_path = path.join(DOWNLOAD_DIRECTORY, image_name)
image_url = IMAGE_SOURCE + image_id[:4] + "/" + image_id[4:6] + "/" + image_id[6:8] + "/png/" + image_name
# https://epic.gsfc.nasa.gov/archive/natural/2018/06/30/png/epic_1b_20180630224431.png

# check if metadata file exists
metadata = path.join(DOWNLOAD_DIRECTORY, "image_info.epic")
if path.exists(metadata):
  # read filename of last image 
  # and skip download if it is the same as the current one
  rf = open(metadata, "r")
  old_image = rf.read()
  rf.close()
  if old_image == image_name:
    print(image_name + " is already on local maschine. Skipping download.")
    exit()

# Download image
opener = URLopener()
try:
  opener.retrieve(image_url, image_path)
except Exception as e:
  print("Download failed")
  print(image_url + image_name)
  print(e)
  exit(1)

# write current image_name to the metadata file
wf = open(metadata, "w")
wf.write(image_name)
wf.close()

# crop image
if args.geometry != "":
  try:
    run(["convert", image_path, "-crop", args.geometry, image_path])
  except Exception as e:
    print("Cropping failed, check if you have imagemagic installed")
    print(e)

rename(image_path, path.join(DOWNLOAD_DIRECTORY, 'epic.png'))
print(image_name + " downloaded")
