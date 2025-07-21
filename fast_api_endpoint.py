import os
import json
import uvicorn
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from index_solutions import generate_all_solutions
from main import main

app = FastAPI()

# Allow CORS for local and production frontend domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_words")
async def get_words(req: Request):
    data = await req.json()
    color_string = data.get("colors", "")
    if len(color_string) != 30:
        return JSONResponse({"Response": 400, "Message": "Color string must be 30 characters", "Solution": []})
    words = main(color_string)
    return words

@app.get('/get_all_solutions')
async def get_all_solutions():
    SOLUTIONS_PATH = "./DB/all_solutions.json"
    if os.path.exists(f"{SOLUTIONS_PATH}"):
        with open(f"{SOLUTIONS_PATH}","r") as f:
            return JSONResponse(json.load(f))
    else:
        res = generate_all_solutions()
        print("New solutions generated")
        return JSONResponse(res)
    
if __name__ == "__main__":
    # For debugging: hot reload, port 8080
    uvicorn.run("fast_api_endpoint:app", host="0.0.0.0", port=8080, reload=True)
    # os.system("gunicorn fast_api_endpoint:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080 --workers 4")