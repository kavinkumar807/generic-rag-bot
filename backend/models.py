from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
import os


def create_chat_model(
    model="llama3-70b-8192",
):
    """
    Creates and returns a configured instance of the LLM model.

    Args:
        model -> str: The model to use (default: "mixtral-8x7b-32768").
        temperature -> float: Sampling temperature for randomness (default: 0).
        max_tokens -> int or None: Maximum number of tokens to generate (default: None).
        timeout -> int or None: Timeout for requests in seconds (default: None).
        max_retries -> int: Number of retries on request failures (default: 2).

    Returns:
        LLM: Configured LLM model instance
    """
    return ChatOpenAI(model=os.getenv("MODEL", model),base_url=os.getenv("BASE_URL"),api_key=os.getenv("API_KEY"))

def create_hugging_face_embedding_model(model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Creates and returns a configured instance of the huggingface embeddings model.

    Args:
        model_name -> str: The model to use (default: "sentence-transformers/all-MiniLM-L6-v").

    Returns:
        HuggingFaceEmbeddings: Configured HuggingFaceEmbeddings model instance
    """
    return HuggingFaceEmbeddings(model_name=model_name, cache_folder="./hf_cache")