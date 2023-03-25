import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
import pymongo


#  Having an error passing stuff to my DB server
# I belive its a cert issue
# Will look into this anouther time
password = "Shammi011%2F%2A-"
client = pymongo.MongoClient("mongodb+srv://jlanzon:"+ password + "@alexandria.j2vxudk.mongodb.net/?retryWrites=true&w=majority")
db = client["alexandria"]
collection = db["index_files"]

def create_index(index_dir, schema):
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    return create_in(index_dir, schema)

def add_document_to_index(index, doc_id, content):
    writer = index.writer()
    writer.add_document(id=doc_id, content=content)
    writer.commit()
    # This section will upload the indexed files to the cloud, as well as the local machine
    data = {"id":doc_id, "content":content}
    collection.insert_one(data)


def search(index, query_str, top_n=10):
    parser = QueryParser("content", index.schema)
    query = parser.parse(query_str)
    with index.searcher() as searcher:
        results = searcher.search(query, limit=top_n)
        return [(r['id'], r.score) for r in results]

schema = Schema(id=ID(unique=True, stored=True), content=TEXT)
index = create_index("index_dir", schema)
