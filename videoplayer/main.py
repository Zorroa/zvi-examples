import os
import time
import zmlp
import gzip
import json
from zmlp import app_from_env
from pprint import pprint
from argparse import ArgumentParser

'''
Generate a WEBVTT track file from an analysis process.  File can then be used in an HTML video track element to display contents along timeline.
example:
    <video id="video" controls preload="metadata" style="width: 100%; margin-top: 30px;">
        <track id="textDetection" label="TextDetection" kind="metadata" srclang="en" src="RENDERED-FILE.webvtt" default/>
        <track id="transcription" label="CaptionFile" kind="subtitles" srclang="en" src="RENDERED-CAPTION-FILE.webvtt" default/>
        <track id="logoDetection" label="Logos" kind="metadata" srclang="en" src="RENDERED-LOGO-DETECTION-FILE.webvtt" default/>
        ...
    </video>
Usage: python main.py -f <ANALYSIS FILE TO SAMPLE> -s <API SERVER URL> -k <PATH TO API KEY>
'''

parser = ArgumentParser()
parser.add_argument("-k", "--key", dest="key", help="Path to APIKEY json file")
parser.add_argument("-s", "--server", dest="server", help="Server path, defaults to https://api.zvi.zorroa.com", default="https://api.zvi.zorroa.com")
parser.add_argument("-f", "--file", dest="file", help="File ID.  Found in Visualizer > Info > Files. Example: assets/l5azb3Pp-lWU7F3J4yIgokvnSbGBH5pc/timeline/gcp-video-label-detection-timeline.json.gz", default=None)

args = parser.parse_args()

md_key = args.key
md_server = args.server
md_file = args.file

app = app_from_env()

apikey = {}
with open(md_key) as json_file:
    apikey = json.load(json_file)

app.client.apikey = apikey
app.client.server = md_server

b = app.assets.download_file(stored_file=md_file)

def _sort_start_clip(clip):
    return float(clip["start"])

def _generate_webvtt(name, clips):
    f = open("{}.webvtt".format(name), "a")
    f.write("WEBVTT - {}\n\n".format(name))
    count = 0
    for clip in clips:
        timestart = clip["start"]
        timeend = clip["stop"]
        content = clip['metadata']['content']

        if content:
            timestart = time.strftime("%H:%M:%S.000", time.gmtime(float(timestart)))
            timeend = time.strftime("%H:%M:%S.000", time.gmtime(float(timeend)))
            
            f.write("{}\n{} --> {}\n{}\n\n".format(count, timestart, timeend, content))
            count += 1

    f.close()

# now that we have our compressed gz file, we can open it with gzip and read it's contents
with gzip.open(b, "rb") as f:
    data = json.loads(f.read())
    name = data["name"]
    # loop through list of tracks
    for track in data["tracks"]:
        # iterate through each clip in a track
        clips = []
        for clip in track["clips"]:
            clips.append(clip)
        
        clips.sort(key=_sort_start_clip)
        _generate_webvtt(name, clips)
        


    
    

