from argparse import ArgumentParser

import whoosh
from whoosh import index
from whoosh import qparser
from whoosh import scoring
from whoosh.qparser.dateparse import DateParserPlugin

from bs4 import BeautifulSoup


red_text    = lambda s: f'\033[1;31m{s}\033[0m'
green_text  = lambda s: f'\033[1;32m{s}\033[0m'
blue_text   = lambda s: f'\033[1;34m{s}\033[0m'
purple_text = lambda s: f'\033[1;35m{s}\033[0m'


def pretty_print(d, indent=False):
    for k, v in d.items():
        k = f'{k:>16s}'
        if isinstance(v, dict):
            print(f'{blue_text(k)}:')
            pretty_print(v, indent=True)
        else:
            ind = '  ' if indent else ''
            print(f'{ind}{blue_text(k)}: {v}')    

def get_user_query():
    query_dict = {k: None for k in ['paper_field', 'date', 'title', 'authors', 'abstract']}

    for key in query_dict:
        ks = f'{key:>12s}'
        query_dict[key] = input(f">>> Specify (or skip) {blue_text(ks)}: ").strip()
        
    return query_dict


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        '--index_path',
        type=str,
        help='Path to the folder where the index was built'
    )
    parser.add_argument(
        '--index_name',
        type=str,
        help='Name of the index'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=10,
        help='Maximum number of results to return'
    )

    return parser.parse_args()

def get_highlights(hs):
    soup = BeautifulSoup(hs, features='lxml')
    for m in soup.findAll('b'):
        hs = hs.replace(str(m), green_text(m.text))
    return hs

def main():
    args = parse_args()

    idx = index.open_dir(args.index_path, indexname=args.index_name)
    parser = qparser.QueryParser('abstract', idx.schema)
    parser.add_plugin(DateParserPlugin())

    while True:
        try:
            print()
            query = get_user_query()
            query_as_string = ""

            for key in query:
                if query[key] is None or query[key] == '':
                    continue
                query_as_string += key + ":(" + query[key] + ") "

            q = parser.parse(query_as_string)
            # print('query_as_string:', query_as_string)
            # print('parsed_query   :', q.__repr__())
            # continue
            
            print()
            with idx.searcher(weighting=scoring.TF_IDF()) as searcher:
                hits = searcher.search(q, limit=args.limit)
                
                if len(hits) == 0:
                    print(red_text('* NO RESULTS FOUND!'))
                else:
                    for i, hit in enumerate(hits, start=1):
                        d = {k: hit[k] for k in hit.keys() if k != 'abstract'}
                        d['highlights'] = {}
                        
                        for h in ['title', 'abstract']:
                            hs = hit.highlights(h)
                            if hs != '':
                                d['highlights'][h] = get_highlights(hs)
                                
                        print(purple_text(f'* HIT {i:>2d}'))
                        pretty_print(d)
                
                print('-' * 120)
                    
        except whoosh.query.qcore.QueryError as e:
            print(red_text(f'QUERY ERROR: {e}'))
            
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()