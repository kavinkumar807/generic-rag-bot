from langchain_core.output_parsers import StrOutputParser
from models import create_chat_model
from prompts import rag_retrieval_prompt
from db import retrieve_from_db


def invoke_llm(user_query, vector):
    """
    Creates a RAG chain for retrieval and generation.

    Args:
        user_query - user_query for retrieval
        vectorstore ->  Instance of vector store 

    Returns:
        rag_chain -> rag chain
    """
    # Prompt
    prompt = rag_retrieval_prompt()

    # LLM
    llm = create_chat_model()

    # Post-processing
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # retriever = retrieve_from_chroma(user_query, vectorstore=vector)
    retriever = retrieve_from_db(user_query, vectorstore=vector)

    # Chain
    rag_chain = prompt| llm | StrOutputParser()

    response = rag_chain.invoke({
        "context" : format_docs(retriever),
        "query": user_query
    })    

    return response