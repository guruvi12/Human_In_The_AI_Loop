import logging

logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
import json
from datetime import datetime

app = FastAPI()

# File paths
HELP_REQUESTS_FILE = "help_requests.json"
KNOWLEDGE_BASE_FILE = "knowledge_base.json"

# Helper functions
def load_json(file):
    try:
        with open(file, 'r') as f:
            return json.load(f)
    except:
        return [] if "requests" in file else {}

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Request models
class HelpRequest(BaseModel):
    question: str
    caller: str

class SupervisorResponse(BaseModel):
    request_id: str
    answer: str

@app.post("/request_help")
async def request_help(req: HelpRequest):
    help_requests = load_json(HELP_REQUESTS_FILE)
    new_request = {
        "id": str(uuid.uuid4()),
        "question": req.question,
        "caller": req.caller,
        "status": "pending",
        "timestamp": str(datetime.now())
    }
    help_requests.append(new_request)
    save_json(HELP_REQUESTS_FILE, help_requests)
    print(f"Supervisor Alert: {req.question}")
    return {"msg": "Supervisor contacted", "request_id": new_request["id"]}

@app.get("/pending_requests")
async def get_pending_requests():
    help_requests = load_json(HELP_REQUESTS_FILE)
    return [r for r in help_requests if r["status"] == "pending"]

@app.post("/supervisor_response")
async def supervisor_response(res: SupervisorResponse):
    help_requests = load_json(HELP_REQUESTS_FILE)
    kb = load_json(KNOWLEDGE_BASE_FILE)

    for r in help_requests:
        if r['id'] == res.request_id:
            r['status'] = 'resolved'
            r['answer'] = res.answer
            kb[r['question']] = res.answer
            print(f"Texting back caller {r['caller']}: {res.answer}")
            break
    else:
        return JSONResponse(status_code=404, content={"error": "Request not found"})

    save_json(HELP_REQUESTS_FILE, help_requests)
    save_json(KNOWLEDGE_BASE_FILE, kb)
    return {"msg": "Answer recorded and user notified."}

@app.get("/knowledge_base")
async def get_knowledge():
    kb = load_json(KNOWLEDGE_BASE_FILE)
    return kb

@app.get("/history")
async def get_history():
    return load_json(HELP_REQUESTS_FILE)
