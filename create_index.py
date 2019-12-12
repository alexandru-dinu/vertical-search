import os
import pickle
import re
from argparse import ArgumentParser
from tqdm import tqdm
import datetime

from whoosh.fields import Schema
from whoosh.fields import TEXT, KEYWORD, STORED, ID, DATETIME
from whoosh.analysis import StemmingAnalyzer
from whoosh import index


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
        abstract=TEXT(analyzer=StemmingAnalyzer()),
        date=DATETIME)

    return schema


def make_index(schema, indexPath, indexName):
    if not os.path.exists(indexPath):
        os.mkdir(indexPath)

    idx = index.create_in(indexPath, schema=schema, indexname=indexName)


def index_documents(documentsPath, indexPath, indexName):
    idx = index.open_dir(indexPath, indexname=indexName)
    files = os.listdir(documentsPath)
    
    for fileName in tqdm(files, desc='Indexing'):
        path = open(os.path.join(documentsPath, fileName), 'rb')
        doc = pickle.load(path)
        
        writer = idx.writer()
        
        for paper in doc:
            authorsAsString = parse_authors(paper.authors)
            date = (*paper.date, 1) # kinda hacky
            
            writer.add_document(
                paper_field=paper.field,
                title=paper.title,
                authors=authorsAsString,
                _stored_authors=paper.authors,
                pdf=paper.pdf,
                abstract=paper.abstract,
                date=datetime.datetime(*date))
            
        writer.commit()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--index_path',
        type=str,
        help='Path to the folder where the index will be built'
    )
    parser.add_argument(
        '--index_name',
        type=str,
        help='Name of the index'
    )
    parser.add_argument(
        '--documents_path',
        type=str,
        help='Path to the documents to be indexed'
    )
    return parser.parse_args()


def main():
    args = parse_args()

    schema = make_schema()
    make_index(schema, args.index_path, args.index_name)
    index_documents(args.documents_path, args.index_path, args.index_name)


if __name__ == '__main__':
    main()
