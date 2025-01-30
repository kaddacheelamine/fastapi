from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
import time


import json

def json_to_html(json_data):
    """Convert JSON data to formatted HTML string."""
    data = json.loads(json_data)  # Convert JSON string to dictionary

    # Extract patient information
    sen=data.get("sendToValue", "Unknown")
    patient_name = data.get("patientName", "Unknown")
    patient_age = data.get("patientAge", "Unknown")
    current_date = data.get("currentDate", "Unknown")

    # Start building the HTML
    html = f"""
    <div class="patient-info">
        <p><strong>Patient Name:</strong> {patient_name}</p>
        <p><strong>Age:</strong> {patient_age}</p>
        <p><strong>Date:</strong> {current_date}</p>
    </div>
    <div class="medications">
        <h3>Medications:</h3>
        <ul>
    """

    # Extract medication details
    for med in data.get("medicines", []):
        name = med.get("name", "Unknown")
        dosage = med.get("dosage", "Unknown")
        note=med.get("note", "Unknown")
        frequency = med.get("frequency", "Unknown")
        html += f"            <li>{name} {dosage} - {frequency} - {note}</li>\n"

    # Close HTML tags
    html += """
        </ul>
    </div>
    """

    return html.strip(),sen


html1="""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prescription</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 20px;
        }
        .prescription {
            border: 2px solid #000;
            padding: 20px;
            max-width: 600px;
            margin: auto;
        }
        .header {
            text-align: center;
            font-weight: bold;
        }
        .doctor-info, .patient-info {
            margin-bottom: 20px;
        }
        .medications {
            border-top: 1px solid #000;
            padding-top: 10px;
        }
    </style>
</head>
<body>
    <div class="prescription">
        <div class="header">
            <h2>Medical Prescription</h2>
        </div>
        <div class="doctor-info">
            <p><strong>Doctor's Name:</strong> Dr. KADDACHE mohammed el amine</p>
            <p><strong>Specialization:</strong> General </p>
            <p><strong>Contact:</strong> (+213) 000 00 00 00</p>
        </div>
"""

html2="""
<div class="footer" style="margin-top: 20px; text-align: center;">
            <p>______________________</p>
            <p>DR . Kaddache M.A</p>
        </div>
    </div>
</body>
</html>
"""


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, sender_password, receiver_email, subject, body):
    # Email configuration
    smtp_server = "smtp.gmail.com"  # Change this if using another provider
    smtp_port = 587

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Email body
    msg.attach(MIMEText(body, "html"))

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")




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
    sendToValue: str
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
        ht,to=json_to_html(data.model_dump_json(indent=2))
        fht=html1+ht+html2
        send_email("rushitadz@gmail.com","khsgsbfifctrgqcy", to, "ordo "+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), fht)
        
        return {"message": "Prescription data received and printed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
