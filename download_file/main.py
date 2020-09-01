import zmlp
import gzip
import json
from zmlp import app_from_env
from argparse import ArgumentParser

'''
Download a media file.
Usage: python main.py -f <FILE ID> -s <API SERVER URL> -k <PATH TO API KEY>
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

filename = md_file.split('/')[-1]
app.assets.download_file(stored_file=md_file, dst_file=filename)
