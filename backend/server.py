from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from typing import Optional
from uuid import uuid4
from db import initialize_db, store_pdf_in_db, store_url_in_db


from chains import invoke_llm


from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

DATA_DIR = Path("../data")
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize db only once
vectorstore = None

@app.on_event("startup")
def get_db():
    """Initialize db if not already initialized."""
    global vectorstore
    if vectorstore is None:
        vectorstore = initialize_db()
        print("Vector store initialized successfully...")
    return vectorstore

# Request model
class QueryRequest(BaseModel):
    user_query: str

#Web URL Request model
class WebURLRequest(BaseModel):
    url: str

@app.post("/invoke")
def invoke(request: QueryRequest):
    """
    Invoke the AI response
    Args:
        request (QueryRequest) -> request model with request string
    Throws:
        e (Exception) -> if any unexpected exception occurs
    """
    try:
        response = invoke_llm(request.user_query, vectorstore)
        return {"response": str(response)}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/ingest/pdf")
async def ingest_pdf_document(file: UploadFile, vectorstore=Depends(get_db)):
        """
        Ingests a document (PDF) and stores it in VectorDB.

        Args:
            file (UploadFile): The uploaded PDF file.

        Returns:
            dict: Success message or error.
        """
        try:
            # Read uploaded file
            file_content = await file.read()

            # Call the function to store PDF in vector db
            store_pdf_in_db(file, file_content,vectorstore)

            return {"message": f"Successfully ingested {file.filename} into vector db"}
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error ingesting document: {str(e)}")


@app.post("/ingest/url")
async def ingest_from_url(request: WebURLRequest, vectorstore=Depends(get_db)):
    """
    Ingests a document from a URL and stores it in VectorDB.

    Args:
        url (str): The URL of the document.

    Returns:
        dict: Success message or error.
    """
    try:
        store_url_in_db(vectorstore,request)
        return {"message": f"Successfully ingested content from {request.url} into VectorDB."}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ingesting document from URL: {str(e)}")  




# Run with: uvicorn server:app --reload