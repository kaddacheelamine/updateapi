from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; you should restrict this in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class Medicine(BaseModel):
    name: str
    dosage: str
    frequency: str
    note: str = ""


class PrescriptionData(BaseModel):
    patientName: str
    patientAge: str
    patientDescription: str
    currentDate: str
    medicines: List[Medicine]
    sendToValue: str = ""


# Static "database"
prescriptions: Dict[str, PrescriptionData] = {
    "123": PrescriptionData(
        patientName='Test patient 1',
        patientAge='22',
        patientDescription='test description',
        currentDate='2024-02-24',
        medicines=[
            Medicine(name='Paracetamol', dosage='500mg', frequency='2X', note="take after food"),
            Medicine(name='Amoxicillin', dosage='250mg', frequency='3X', note="take before food"),
        ]
    ),
    "456": PrescriptionData(
        patientName='Test patient 2',
        patientAge='32',
        patientDescription='test description2',
        currentDate='2024-02-20',
        medicines=[
            Medicine(name='Vitamin D', dosage='1000IU', frequency='1X', note="take in the morning"),
            Medicine(name='Omega 3', dosage='500mg', frequency='2X', note="take with food"),
        ]
    )
}


@app.get("/prescriptions/{prescription_id}")
async def get_prescription(prescription_id: str):
    if prescription_id not in prescriptions:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescriptions[prescription_id]


@app.post("/prescriptions/{prescription_id}")
async def update_prescription(prescription_id: str, updated_prescription: PrescriptionData):
    if prescription_id not in prescriptions:
        raise HTTPException(status_code=404, detail="Prescription not found")
    prescriptions[prescription_id] = updated_prescription
    return {"message": "Prescription updated"}


@app.post("/store")
async def create_prescription(prescription: PrescriptionData):
     # Generate a unique ID for new prescriptions (you can use a more robust method)
     new_id = str(len(prescriptions) + 1)
     prescriptions[new_id] = prescription
     return {"message": "Prescription created with ID: "+new_id}
