from fastapi import FastAPI

app = FastAPI()

@app.post("/store")
async def store_text(content: str):
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(content + "\n")
    return {"message": "Text stored successfully"}
