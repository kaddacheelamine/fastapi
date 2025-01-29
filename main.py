from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/store")
async def store_text(content: str):
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(content + "\n")
    return {"message": "Text stored successfully"}
