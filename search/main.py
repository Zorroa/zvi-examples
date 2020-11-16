import os
import zmlp
import json
from zmlp import app_from_env
# import elasticsearch_dsl as es
from pprint import pprint
import logging
from argparse import ArgumentParser

logger = logging.getLogger(__name__)

"""
Demonstrates searching for ZVI assets

Usage: python main.py -k <PATH TO API KEY> [-a, -s, -e, -et, -ea, -estt]

Getting started with Elastic Search queries: https://www.elastic.co/guide/en/elasticsearch/guide/master/getting-started.html
"""

parser = ArgumentParser()
parser.add_argument("-k", "--key", dest="key", help="Path to APIKEY json file")
parser.add_argument("-s", "--server", dest="server", help="Server path, defaults to https://api.zvi.zorroa.com", default="https://api.zvi.zorroa.com")
parser.add_argument("-a", "--all", dest="all", help="Get all assets")
parser.add_argument("-q", "--query", dest="query", help="Simple query")
parser.add_argument("-e", "--eslibrary", dest="eslibrary", help="Simple query using Elastic Search library")
parser.add_argument("-et", "--esterm", dest="esterm", help="Query with Elastic Search term targetting analysis.gcp-vision-label-detection.predictions.label ns")
parser.add_argument("-ea", "--esaggregation", dest="esaggregation", help="Query with Elastic Search aggregation targetting analysis.gcp-vision-label-detection.predictions.label ns")
parser.add_argument("-estt", "--estermtype", dest="estermtype", help="Search by asset type(video, document, image) and term. Usage Sample: python main.py -estt 'video:cats'")

args = parser.parse_args()

md_key = args.key
md_server = args.server
md_all = args.all
md_query = args.query
md_eslibrary = args.eslibrary
md_esterm = args.esterm
md_esaggregation = args.esaggregation
md_estermtype = args.estermtype


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

def by_file_type_term(payload):
    search = app.assets.search(search=payload)
    for asset in search:
        print(asset.id)

def main():
    # get all assets
    if md_all:
        get_all()

    # search term across all fields
    if md_query:
        search = {"query": {"simple_query_string": {"query": md_query}}}
        all_fields(search)

    # same search as above but using the Python ElasticSearch DSL Library to form the search request.
    # if md_eslibrary:
    #     search = es.Search().query(es.query.SimpleQueryString(query=md_eslibrary))
    #     for asset in app.assets.search(search=search):
    #         print(asset["source.path"])

    # queries
    # namespaces such as analysis.gcp-vision-label-detection.predictions.label can be found in ZVI's visualizer under the Asset Metadata > RAW JSON section.
    # ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/_search_with_query_dsl.html
    # ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/_more_complicated_searches.html
    if md_esterm:
        search = {"query": {"match": {"analysis.gcp-vision-label-detection.predictions.label": md_esterm}}}
        by_es_term(search)

    # aggregation
    # ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/_analytics.html
    # ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/aggregations.html
    if md_esaggregation:
        search = {"aggs" : {"all_labels": {"terms": {"field": "analysis.gcp-vision-label-detection.predictions.label"}}}}
        by_aggregation(search)

    # by file type and term
    # ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/_analytics.html
    # ES reference: https://www.elastic.co/guide/en/elasticsearch/guide/master/aggregations.html
    if md_estermtype:
        args = md_estermtype.split(":")
        search = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"media.type": args[0]}},
                        {"simple_query_string": {"query": args[1]}}
                        ]
                }
            }
        }
        by_file_type_term(search)

if __name__ == "__main__":
    main()