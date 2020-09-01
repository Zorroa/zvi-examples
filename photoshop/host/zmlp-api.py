import os
import zmlp
import json
from os import path
from pprint import pprint
from os import listdir
from os.path import isfile, join
from zmlp.search import SimilarityQuery
from zmlp import app_from_env 
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-k", "--key", dest="key", help="Path to APIKEY json file")
parser.add_argument("-s", "--server", dest="server", help="Server path, defaults to https://api.zvi.zorroa.com", default="https://api.zvi.zorroa.com")
parser.add_argument("-t", "--term", dest="term", help="Search term", default=False)
parser.add_argument("-a", "--all", dest="all", help="Get all", default=False)
parser.add_argument("-f", "--folder", dest="folder", help="Search by image.  Path to folder location of images", default=False)
parser.add_argument("-m", "--sim", dest="similarity", help="Search by image similiarty.  ID of asset to query against", default=False)

args = parser.parse_args()

md_key = args.key
md_server = args.server
md_term = args.term
md_folder = args.folder
md_sim = args.similarity
md_all = args.all

app = app_from_env()

apikey = {}
with open(md_key) as json_file:
    apikey = json.load(json_file)

app.client.apikey = apikey
app.client.server = args.server

def render_assets(assets):
    """
    generate assets json and download assets
    """
    with open("assets.json", "w") as fp:
        output = []
        for asset in assets:
            files = asset.get_attr("files")
            
            # rename with asset id
            file_ref = files[0]["id"]
            file_id = file_ref.split("/")[1]
            ext = file_ref.split(".")[-1]

            new_name = "{}.{}".format(file_id, ext)
            download_file(file_ref, new_name)

            proxy = next((x for x in files if x["name"] == "web-proxy.jpg"), None)
            proxy["file_ref"] = new_name
            
            output.append(proxy)
        
        fp.write(json.dumps({"assets": output}))

def get_all():
    search = app.assets.scroll_search(search=None)
    count = 0
    for asset in search:
        print(asset.id)
        count += 1
    print(count)

def search(md_term):
    query = {"query": {"simple_query_string": {"query": md_term}}}
    search = app.assets.scroll_search(search=query)
    render_assets(search)

def similarity_search(asset_id):
    asset = app.assets.get_asset(asset_id)
    h = asset.document['analysis']['zvi-image-similarity']['simhash']
    query = {"query": {"bool": {"must": [SimilarityQuery(h)]}}}
    search = app.assets.search(query)

    render_assets(search)
    
# def search_by_image(folder):
#     onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
#     images = []

#     for f in onlyfiles:
#         images.append("{}/{}".format(folder, f))

#     file_path = "/Users/nu/Movies/processed/IMG_9722.jpg"
#     # images = open(file_path, 'rb')
#     # pprint(images)
#     # query = {
#     #     "bool": {
#     #         "must": [
#     #             app.assets.get_sim_query([file_path], min_score=0.5)
#     #         ]
#     #     }
#     # }
#     # app.assets.get_sim_hashes(images=file_path)
#     app.client.upload_files("/ml/v1/sim-hash", [file_path], body=None)
#     # search = app.assets.search(query)
#     # render_assets(search)


def download_file(source, target):
    location = "../assets/{}".format(target)
    if not path.exists(location):
        app.assets.download_file(stored_file=source, dst_file=location)

if md_term:
    search(md_term)

# if md_folder:
#     search_by_image(md_folder)

if md_sim:
    similarity_search(md_sim)

if md_all:
    get_all()