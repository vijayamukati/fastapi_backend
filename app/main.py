from fastapi import FastAPI, File, UploadFile, HTTPException
from app.utils import scrape_url, extract_pdf_text
from app.embeddings import generate_embeddings, find_relevant_content
from uuid import uuid4

app = FastAPI()

# In-memory storage for content
content_storage = {}

@app.post("/process_url")
async def process_url(url: str):
    try:
        # Scrape content from the URL
        content = scrape_url(url)
        if not content:
            raise HTTPException(status_code=400, detail="Failed to scrape content")
        
        # Generate a unique chat ID
        chat_id = str(uuid4())
        
        # Store the content
        content_storage[chat_id] = content

        return {"chat_id": chat_id, "message": "URL content processed and stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/process_pdf")
async def process_pdf(file: UploadFile = File(...)):
    try:
        # Extract text from the uploaded PDF
        content = extract_pdf_text(await file.read())
        if not content:
            raise HTTPException(status_code=400, detail="Failed to extract text from PDF")
        
        # Generate a unique chat ID
        chat_id = str(uuid4())
        
        # Store the content
        content_storage[chat_id] = content

        return {"chat_id": chat_id, "message": "PDF content processed and stored successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(chat_id: str, question: str):
    try:
        # Retrieve content associated with the chat_id
        content = content_storage.get(chat_id)
        if not content:
            raise HTTPException(status_code=404, detail="Chat ID not found")
        
        # Generate embeddings for the content and the question
        response = find_relevant_content(content, question)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

