from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration
origins = [
    "*",  # البورت الذي يعمل عليه رياكت
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # السماح لجميع الطرق، بما في ذلك OPTIONS
    allow_headers=["*"],  # السماح لجميع الرؤوس
)


class Medicine(BaseModel):
    name: str
    dosage: str
    frequency: str
    note: str


class PrescriptionData(BaseModel):
    patientName: str
    patientAge: int
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
