# Searching for assets

## Prerequisites:

- Python

Download the contents in https://github.com/Zorroa/zvi-examples/tree/master/search

Documents are stored in Elastic Search and ZVI allows you to pass search ES queries directly into the asset search object. Users have full control on how they want to retrieve data. You are only limited by Elastic Search queries. Below are five different examples to perform searches.

For more information refer to our [gitbook documentation](https://app.gitbook.com/@zorroa/s/zmlp/client/assets/asset-search)

- Get all assets
- Search across all fields using a single term
- Search across all fields using the Python ElasticSearch DSL Library
- Search using Elastic Search queries
- Search using Elastic Search aggregation

First our script will [authenticate](https://app.gitbook.com/@zorroa/s/zmlp/client/authentication) against the server.

## Get all assets

```python
app = app_from_env()

# return the first page of 10 assets
# search = app.assets.search(search=None)

# returns all assets
search = app.assets.scroll_search(search=None)
for asset in search:
    print(asset)
```

## Search across all ES fields using a single term

```python
app = app_from_env()

payload = {"query": {"simple_query_string": {"query": "dog"}}}
# returns all assets
search = app.assets.scroll_search(search=payload)
for asset in search:
    # print the asset's source path
    print(asset["source.path"])
```

## Search across all fields using the Python ElasticSearch DSL Library

_Same search as above but using the Python ElasticSearch DSL Library to form the search request._

```python
import zmlp
import elasticsearch_dsl as es
...
...
app = app_from_env()

search = es.Search().query(es.query.SimpleQueryString(query="dog"))
for asset in app.assets.search(search=search):
    print(asset["source.path"])
```

## Search using Elastic Search queries

```python
import zmlp
import elasticsearch_dsl as es
...
...
app = app_from_env()

payload = {"query": {"match": {"analysis.gcp-vision-label-detection.predictions.label": "Horse"}}}
search = app.assets.search(search=payload)
for asset in search:
    print(asset.id)
    # namespaces such as source.path can be found in ZVI's visualizer under the Asset Metadata > RAW JSON section.
    print(asset.get_attr("source.path"))
```

## Search using Elastic Search aggregation

```python
import zmlp
import elasticsearch_dsl as es
...
...
app = app_from_env()

payload = {"aggs" : {"all_labels": {"terms": {"field": "analysis.gcp-vision-label-detection.predictions.label"}}}}
search = app.assets.search(search=payload)
print(search.aggregation("all_labels"))
```
