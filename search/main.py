import os
import zmlp
import json
from zmlp import app_from_env
import elasticsearch_dsl as es
from pprint import pprint
from argparse import ArgumentParser

'''
Searching for assets in ZVI

Usage: python main.py -k <PATH TO API KEY>

Getting started with Elastic Search queries: https://www.elastic.co/guide/en/elasticsearch/guide/master/getting-started.html
'''

parser = ArgumentParser()
parser.add_argument("-k", "--key", dest="key", help="Path to APIKEY json file")
parser.add_argument("-s", "--server", dest="server", help="Server path, defaults to https://api.zvi.zorroa.com", default="https://api.zvi.zorroa.com")

args = parser.parse_args()

md_key = args.key
md_server = args.server

app = app_from_env()

apikey = {}
with open(md_key) as json_file:
    apikey = json.load(json_file)

app.client.apikey = apikey
app.client.server = md_server

# loop through all items
def get_all():
    search = app.assets.scroll_search(search=None)
    for asset in search:
        print(asset)

def all_fields(payload):
    search = app.assets.scroll_search(search=payload)
    for asset in search:
        print(asset["source.path"])

# search by es term
def by_es_term(payload):
    search = app.assets.search(search=payload)
    for asset in search:
        print(asset.id)
        # namespaces such as source.path can be found in ZVI's visualizer under the Asset Metadata > RAW JSON section.
        print(asset.get_attr("source.path"))

def by_aggregation(payload):
    search = app.assets.search(search=payload)
    pprint(search.aggregation("all_labels"))

# get all assets
get_all()

# search term across all fields
search = {"query": {"simple_query_string": {"query": "dog"}}}
all_fields(search)

# same search as above but using the Python ElasticSearch DSL Library to form the search request.
search = es.Search().query(es.query.SimpleQueryString(query="dog"))
for asset in app.assets.search(search=search):
    print(asset["source.path"])

# queries
# namespaces such as analysis.gcp-vision-label-detection.predictions.label can be found in ZVI's visualizer under the Asset Metadata > RAW JSON section.
# ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/_search_with_query_dsl.html
# ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/_more_complicated_searches.html
search = {"query": {"match": {"analysis.gcp-vision-label-detection.predictions.label": "Horse"}}}
by_es_term(search)

# aggregation
# ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/_analytics.html
# ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/aggregations.html
search = {"aggs" : {"all_labels": {"terms": {"field": "analysis.gcp-vision-label-detection.predictions.label"}}}}
by_aggregation(search)
