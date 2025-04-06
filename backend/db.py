from pymongo import MongoClient
from pymongo.operations import SearchIndexModel
from langchain_mongodb import MongoDBAtlasVectorSearch
from uuid import uuid4
from langchain_community.document_loaders import WebBaseLoader
from models import create_hugging_face_embedding_model
import utils
import os
import certifi
import time

def initialize_db():
    """
    Initializes and returns a Chroma vector store.

    Args:
        persist_directory - Directory to store ChromaDB.
    
    Returns:
        vectorstore - Initialized Chroma vector store.
    """
    # initialize MongoDB python client
    MONGODB_URI = os.getenv("MONGO_API_KEY")
    if not MONGODB_URI:
        raise ValueError("MONGODB_URI is not set. Make sure to set it in the environment.")
    
    try:
        # Create MongoDB client
        mongo_client= MongoClient(MONGODB_URI)
        print("MongoDB connection established successfully.")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

    DB_NAME = os.getenv("MONGO_DB_NAME")
    COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")
    ATLAS_VECTOR_SEARCH_INDEX_NAME = os.getenv("MONGO_ATLAS_VECTOR_SEARCH_INDEX_NAME")

    MONGODB_COLLECTION = mongo_client[DB_NAME][COLLECTION_NAME]
    # Initialize the Chroma vector store
    vectorstore = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding=create_hugging_face_embedding_model(),
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        relevance_score_fn="cosine",
    )
    # Check if the search index already exists
    message = ensure_vector_search_index(mongo_client, DB_NAME, COLLECTION_NAME,ATLAS_VECTOR_SEARCH_INDEX_NAME)
    print(message)
    
    return vectorstore

#### INDEXING ####
def store_pdf_in_db(uploaded_file, file_content,vectorstore):
    """
    Stores it in a local ChromaDB.

    Args:
        uploaded_file -> file for RAG ingestion pipeline
        vectorstore ->  Instance of vector store        

    Returns:
        vectorstore -> Instance of vector store        
    """

    splits = utils.process_pdf_for_rag(uploaded_file, file_content)

    uuids = [str(uuid4()) for _ in range(len(splits))]

    # Embed and store in local ChromaDB
    vectorstore.add_documents(documents=splits, ids=uuids)

def store_url_in_db(vector_store,request):
    """
    Stores it in a local ChromaDB.

    Args:
        uploaded_file -> file for RAG ingestion pipeline
        vectorstore ->  Instance of vector store        

    Returns:
        vectorstore -> Instance of vector store        
    """

     # Load webpage content
    loader = WebBaseLoader(request.url)
    docs = loader.load()

    splits = utils.doc_splitter(docs)

    uuids = [str(uuid4()) for _ in range(len(splits))]

    # Store documents in ChromaDB
    vector_store.add_documents(documents=splits, ids=uuids)

#### RETRIEVAL ####
def retrieve_from_db(query, vectorstore):
    """
    Retrieves the most relevant documents from the Chroma vector store
    based on the user's query.

    Args:
        query -> The query string for searching the vector store.
        vectorstore -> The Chroma vector store instance for document retrieval.

    Returns:
        documents - The most relevant documents retrieved from Chroma.
    """
    retriever = vectorstore.as_retriever()
    results =retriever.invoke(query)

    return results

def ensure_vector_search_index(mongo_client, db_name, collection_name, index_name, path="embedding", dimensions=384):
    """
    Ensures a vector search index exists in MongoDB Atlas. If not found, it creates one.

    :param uri: MongoDB connection URI
    :param db_name: Database name
    :param collection_name: Collection name
    :param index_name: Name of the vector search index
    :param path: Field storing the embedding vectors
    :param dimensions: Number of dimensions in the vector embeddings
    :return: Status message (str)
    """

    database = mongo_client[db_name]
    collection = database[collection_name]

    # Check if the search index already exists
    existing_search_indexes = list(collection.list_search_indexes())
    index_exists = any(idx["name"] == index_name for idx in existing_search_indexes)

    if index_exists:
        message = f"Search index '{index_name}' already exists."
    else:
        # Define the vector search index model
        search_index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "vector",
                        "numDimensions": dimensions,
                        "path": path,
                        "similarity": "cosine"
                    }
                ]
            },
            name=index_name,
            type="vectorSearch"
        )

        # Create the search index
        result = collection.create_search_index(model=search_index_model)
        message = f"New search index named '{result}' is building."

        # Wait for the index to be ready
        predicate = lambda index: index.get("queryable") is True

        while True:
            indices = list(collection.list_search_indexes(result))
            if len(indices) and predicate(indices[0]):
                break
            time.sleep(5)  # Wait before checking again
        
        message = f"Search index '{result}' is ready for querying."
        
    return message