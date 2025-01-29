from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class Medicine(BaseModel):
    name: str
    dosage: str
    frequency: str
    note: str

class PrescriptionData(BaseModel):
    patientName: str
    patientAge: str
    patientDescription: str
    currentDate: str
    medicines: List[Medicine]
    
@app.post("/store")
async def store_prescription(data: PrescriptionData):
    """
    Receives and stores prescription data.
    """
    try:
        print("Received Prescription Data:")
        print(data.model_dump_json(indent=2))
        return {"message": "Prescription data received and printed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
