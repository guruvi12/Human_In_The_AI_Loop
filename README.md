# Human_In_The_AI_Loop
# Human-in-the-Loop AI Supervisor System

This project builds upon Twilio's `call-gpt` to create a self-improving receptionist agent that:
- Answers calls using GPT.
- Escalates questions it can't handle to a human.
- Lets supervisors resolve issues via UI.
- Updates its knowledge base over time.

## Features

✅ AI Agent escalation  
✅ Supervisor dashboard  
✅ Request lifecycle handling (Pending → Resolved/Unresolved)  
✅ Auto KB updates  
✅ Minimal setup, clean architecture  

## Tech Stack

- Python + FastAPI
- JSON files (TinyDB alternative)
- HTML + Vanilla JS for UI
- Console for simulating messages

## Setup Instructions

```bash
git clone https://github.com/YOUR-USERNAME/call-gpt-hotline.git
cd call-gpt-hotline
pip install fastapi uvicorn
uvicorn main:app --reload


How It Works
AI gets a customer question.

If unknown, calls /request_help.

Supervisor uses the UI to respond.

AI texts caller (simulated via print()).

The KB is updated in knowledge_base.json.


Improvements for Phase 2
Real-time supervisor handoff

Timeout daemons to auto-mark as unresolved

Persistent DB (Firebase / DynamoDB)

Deploy to cloud