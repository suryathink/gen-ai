from fastapi import FastAPI, Query
from .queue.connection import queue
from .queue.worker import process_query # importing function from different pages

app = FastAPI()

@app.get('/')
def root():
    return {"status":"Server is up and running"}



@app.post('/chat')
def chat(
    query: str = Query(..., description="Chat Message")
):
    # Query ko Queue mei daal do
    job = queue.enqueue(process_query, query)  # this (process_query, query) means -> process_query(query), means process_query function is getting called with argument as query

    # User ko bolo your job received
    return {"status": "queued", "job_id": job.id}


# command to run  python server
# Install uvicorn -> pip install uvicorn
# python -m uvicorn server:app --reload
# check other command to run the server present in main.py