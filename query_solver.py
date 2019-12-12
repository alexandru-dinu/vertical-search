from argparse import ArgumentParser

import whoosh
from whoosh import index
from whoosh import qparser
from whoosh import scoring
from whoosh.qparser.dateparse import DateParserPlugin


def pretty_print(d):
    for k, v in d.items():
        print(f'{k:>12s}: {v}')    

def get_user_query():
    query_dict = {k: None for k in ['paper_field', 'date', 'title', 'authors', 'abstract']}

    for key in query_dict:
        query_dict[key] = input(f">>> Specify <{key:>12s}> or continue: ").strip()
        
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


def main():
    args = parse_args()

    idx = index.open_dir(args.index_path, indexname=args.index_name)
    parser = qparser.QueryParser('abstract', idx.schema)
    parser.add_plugin(DateParserPlugin())

    while True:
        try:
            query = get_user_query()
            query_as_string = ""

            for key in query:
                if query[key] is None or query[key] == '':
                    continue
                query_as_string += key + ":(" + query[key] + ") "

            q = parser.parse(query_as_string)
#             print('query_as_string:', query_as_string)
#             print('parsed_query   :', q.__repr__())
#             continue
            
            with idx.searcher(weighting=scoring.TF_IDF()) as searcher:
                result = searcher.search(q, limit=args.limit)
                
                if len(result) == 0:
                    print('* NO RESULTS FOUND!')
                else:
                    for i, res in enumerate(result, start=1):
                        d = {k: res[k] for k in res.keys()}
                        print(f'* HIT {i:>2d}')
                        pretty_print(d)
                
                print('-' * 120)
                    
        except whoosh.query.qcore.QueryError as e:
            print(f'QUERY ERROR: {e}')
            
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()