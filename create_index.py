import os
import pickle
import re
from argparse import ArgumentParser
from tqdm import tqdm

from common import Paper
from whoosh.fields import Schema
from whoosh.fields import TEXT, KEYWORD, STORED, ID, DATETIME
from whoosh.analysis import StemmingAnalyzer
from whoosh import index


def index_document():
    pass


def parse_authors(authors):

    authorsName = []
    for author in authors:
        names = author.split(' ')
        for name in names:
            if name[-1] != '.':
                authorsName.append(name)

    return ' '.join(authorsName)



def make_schema():

    schema = Schema(
        paper_field=KEYWORD(stored=True, lowercase=True, scorable=True),
        title=TEXT(stored=True),
        authors=KEYWORD(stored=True, lowercase=True),
        pdf=ID(stored=True),
        abstract=TEXT(analyzer=StemmingAnalyzer())
    )

    return schema


def make_index(schema, indexPath='indexdir', indexName='my_index'):

    if not os.path.exists(indexPath):
        os.mkdir(indexPath)

    idx = index.create_in(indexPath, schema=schema, indexname=indexName)


def index_documents(documentsPath='out', indexPath='indexdir', indexName='my_index'):

    idx = index.open_dir(indexPath, indexname=indexName)
    files = os.listdir(documentsPath)
    for fileName in tqdm(files[1:10]):
        with open(documentsPath + '/' + fileName, 'rb') as f:
            doc = pickle.load(f)
            writer = idx.writer()
            for paper in doc:
                authorsAsString = parse_authors(paper.authors)
                writer.add_document(
                    paper_field=paper.field,
                    title=paper.title,
                    authors=authorsAsString,
                    _stored_authors=paper.authors,
                    pdf=paper.pdf,
                    abstract=paper.abstract
                )
            writer.commit()

    print(files[1:10])



def main():

    schema = make_schema()
    make_index(schema)
    index_documents()



if __name__ == '__main__':
    main()
