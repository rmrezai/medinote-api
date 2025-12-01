from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from core_modules import medinote_ap_handler

app = FastAPI()

class MedinotePayload(BaseModel):
    labs: Dict[str, float]
    vitals: Dict[str, str] = {}
    meds: List[str] = []

@app.post("/medinote/ap")
async def process_medinote_input(payload: MedinotePayload):
    return medinote_ap_handler(payload.dict())
