from flask import current_app


def create_index(index, model):
    if not current_app.elasticsearch:
        return
    settings = {
        "analysis": {
            "filter": {
                "french_elision": {
                    "type": "elision",
                    "articles_case": True,
                    "articles": ["l", "m", "t", "qu", "n", "s", "j", "d", "c", "jusqu", "quoiqu", "lorsqu", "puisqu"]
                },
                "french_synonym": {
                    "type": "synonym",
                    "ignore_case": True,
                    "expand": True,
                    "synonyms": []
                },
                "french_stop": {
                    "type": "stop",
                    "stopwords": "_french_"
                },
                "french_stemmer": {
                    "type": "stemmer",
                    "language": "light_french"
                }
            },
            "analyzer": {
                "french_heavy": {
                    "tokenizer": "icu_tokenizer",
                    "filter": [
                        "french_elision",
                        "icu_folding",
                        "french_stop",
                        "french_synonym",
                        "french_stemmer"
                    ]
                },
                "french_light": {
                    "tokenizer": "icu_tokenizer",
                    "filter": [
                        "french_elision",
                        "icu_folding",
                        "french_stop"
                    ]
                },
                "quote_french": {
                    "tokenizer": "icu_tokenizer",
                    "filter": [
                        "lowercase",
                    ]
                }
            }
        }
    }
    mappings = {
        "properties": {}
    }
    for field in model.__searchable__:
        mappings["properties"][field] = {
            "type": "text",
            "analyzer": "french_light",
            "fields": {
                "stemmed": {
                    "type": "text",
                    "analyzer": "french_heavy",
                    "search_quote_analyzer": "quote_french"
                }
            }
        }

    current_app.elasticsearch.indices.create(index=index, settings=settings, mappings=mappings)


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    if not current_app.elasticsearch.indices.exists(index=index):
        create_index(index, model)
    payload = {}

    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    model_id = model.id if hasattr(model, 'id') else model.nomfichier
    current_app.elasticsearch.index(index=index, id=model_id, body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    model_id = model.id if hasattr(model, 'id') else model.nomfichier
    current_app.elasticsearch.delete(index=index, id=model_id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index,
        body={
            "query": {
                'simple_query_string': {
                    'query': query,
                    # 'type': 'best_fields',
                    "minimum_should_match": "100%",
                    'fields': ['titrenoir.stemmed', 'titre.stemmed', 'fulltext.stemmed'],
                    "quote_field_suffix": ".exact"
                }
            },
            "highlight": {
                "require_field_match": "true",
                "pre_tags": ["<span>"],
                "post_tags": ["</span>"],
                "fields": [
                    {
                        "titre*": {
                            "matched_fields": ["titre*"],
                            "number_of_fragments": 0
                        }
                    },
                    {
                        "fulltext*": {
                            "fragment_size": 100,
                            "number_of_fragments": 4}
                    }
                ],
                "highlight_query": {
                    'multi_match': {
                        'query': query,
                        "analyzer": "french_heavy",
                        'fields': ['titrenoir.stemmed', 'titre.stemmed', 'fulltext.stemmed']
                    }
                }
            },
            'from': (page - 1) * per_page, 'size': per_page
        })
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    highlights = []
    for hit in search['hits']['hits']:
        if "highlight" in hit:
            highlights.append({"id": int(hit['_id']), "highlight": hit["highlight"]})

    return ids, search['hits']['total']['value'], highlights
