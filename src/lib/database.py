from pymongo import MongoClient, database, collection


MONGO_HOST = 'mongo'
MONGO_PORT = 27017


def create_client():
    return MongoClient(MONGO_HOST, MONGO_PORT)


def get_database(client: MongoClient, db_name: str):
    return client[db_name]


def get_collection(db: database, collection_name: str):
    return db[collection_name]


def insert_document(db_collection: collection, document: dict):
    """
    Inserts a single document into a collection.
    :param db_collection: the collection to insert to
    :param document: the document to insert
    :return: an ObjectId for the inserted document
    """

    inserted_document = db_collection.insert_one(document)
    return inserted_document.inserted_id


def bulk_insert_documents(db_collection: collection, documents: dict):
    """
    Inserts multiple documents into a collection.
    :param db_collection: the collection to insert to
    :param documents: the documents to insert
    :return: a list of ObjectId for the inserted documents
    """

    inserted_documents = db_collection.insert_many(documents)
    return inserted_documents.inserted_ids


def query_document(db_collection: collection, filters: dict = None):
    """
    Queries a collection for the first document that matches the filters.
    :param db_collection: the collection to make the query in
    :param filters: the dict containing key-value pairs to filter with
    :return: a dict representing the found document
    """

    document = db_collection.find_one(filters)
    return document


def query_all_documents(db_collection: collection, filters: dict = None):
    """
    Queries a collection for all the documents that match the filters
    :param db_collection: the collection to make the query in
    :param filters: the dict containing the key-value pairs to filter with
    :return: a dict representing the found documents
    """

    documents = db_collection.find(filters)
    return documents
