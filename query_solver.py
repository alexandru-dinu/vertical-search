import pprint
from argparse import ArgumentParser

from whoosh import index
from whoosh import qparser


def get_user_query():
    query_dict = {
        "paper_field": None,
        "title": None,
        "authors": None,
        "abstract": None,
    }

    print("$>> New query:")
    for key in query_dict:
        query_dict[key] = input(
            "$>> Specify values for field {} or continue: ".format(key)
        ).lower()

    print("$>> Query result: ")
    return query_dict


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        'index_path',
        type=str,
        help='Path to the folder where the index was built'
    )
    parser.add_argument(
        'index_name',
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

    printer = pprint.PrettyPrinter()

    while True:
        query = get_user_query()
        query_as_string = ""
        for key in query:
            if query[key] is None or query[key] == '':
                continue

            query_as_string += key + ":(" + query[key] + ") "

        q = parser.parse(query_as_string)
        with idx.searcher() as searcher:
            result = searcher.search(q, limit=args.limit)
            dict_res = {}
            for res in result:
                for key in res.keys():
                    dict_res[key] = res[key]
                printer.pprint(dict_res)

        new_input = input("$ >> Do you want to search for anything else ? [Y/N] ")
        if new_input.lower() == 'n':
            break


if __name__ == '__main__':
    main()
