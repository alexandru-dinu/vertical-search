import whoosh
from whoosh import index
from whoosh import qparser
from whoosh import scoring
from whoosh.qparser.dateparse import DateParserPlugin

import hug

        
@hug.post('/search')
def once(query):
    idx = index.open_dir('./index', indexname='arxiv')
    parser = qparser.QueryParser('abstract', idx.schema)
    parser.add_plugin(DateParserPlugin())
    
    query_as_string = ""

    for key in query:
        if query[key] is None or query[key] == '':
            continue
        query_as_string += key + ":(" + query[key] + ") "

    q = parser.parse(query_as_string)

    res = {}
    with idx.searcher(weighting=scoring.TF_IDF()) as searcher:
        hits = searcher.search(q, limit=10)

        if len(hits) == 0:
            return {}
        else:
            for i, hit in enumerate(hits, start=1):
                d = {k: hit[k] for k in hit.keys()}
                res[f'hit-{i}'] = d
                res[f'hit-{i}']['highlights'] = {
                    'title': hit.highlights('title'),
                    'abstract': hit.highlights('abstract')
                }

    return res