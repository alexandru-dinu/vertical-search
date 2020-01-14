from argparse import ArgumentParser

import whoosh
from whoosh import index
from whoosh import qparser
from whoosh import scoring
from whoosh.qparser.dateparse import DateParserPlugin

import flask

from flask import Flask, render_template, request
app = Flask(__name__)

keys = ["paper_field",
		"date",
		"title",
		"authors",
		"abstract"]

@app.route('/')
def student():
    return render_template('query.html')

@app.route('/result', methods = ['POST'])
def once():
    idx = index.open_dir('./index', indexname='arxiv')
    parser = qparser.QueryParser('abstract', idx.schema)
    parser.add_plugin(DateParserPlugin())
    
    query = dict(request.form)
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

    print(res)
    
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='7007')