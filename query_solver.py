import lucene
from org.apache.lucene import analysis, document, index, queryparser, search, store, util
from lupyne import engine
lucene.initVM()


def main():
    analyzer = analysis.standard.StandardAnalyzer(util.Version.LUCENE_CURRENT)

    # Store the index in memory:
    directory = store.RAMDirectory()
    # To store an index on disk, use this instead:
    # Directory directory = FSDirectory.open(File("/tmp/testindex"))
    config = index.IndexWriterConfig(util.Version.LUCENE_CURRENT, analyzer)
    iwriter = index.IndexWriter(directory, config)
    doc = document.Document()
    text = "This is the text to be indexed."
    doc.add(document.Field("fieldname", text, document.TextField.TYPE_STORED))
    iwriter.addDocument(doc)
    iwriter.close()

    # Now search the index:
    ireader = index.IndexReader.open(directory)
    isearcher = search.IndexSearcher(ireader)
    # Parse a simple query that searches for "text":
    parser = queryparser.classic.QueryParser(util.Version.LUCENE_CURRENT, "fieldname", analyzer)
    query = parser.parse("text")
    hits = isearcher.search(query, None, 1000).scoreDocs
    assert len(hits) == 1
    #Iterate through the results:
    for hit in hits:
        hitDoc = isearcher.doc(hit.doc)
        assert hitDoc['fieldname'] == text
    ireader.close()
    directory.close()


if __name__ == '__main__':
    main()