"""Elasticsearch search utilities for videos"""
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

def search_videos(query_text):
    body = {
        "query": {
            "multi_match": {
                "query": query_text,
                "fields": ["title", "description"]
            }
        }
    }
    results = es.search(index="videos", body=body)
    return results['hits']['hits']
