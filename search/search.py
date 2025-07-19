from elasticsearch import Elasticsearch
es = Elasticsearch(['http://localhost:9200'])

def search_videos(query_text):
    body = {
        "query": {
            "multi_match": {
                "query": query_text,
                "fields": ["title", "description", "tags"]
            }
        }
    }
    return es.search(index='videos', body=body)['hits']['hits']
