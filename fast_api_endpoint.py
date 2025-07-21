from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from main import main  # Your search/solution logic
import uvicorn

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

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get_words")
async def get_words(req: Request):
    data = await req.json()
    color_string = data.get("colors", "")
    if len(color_string) != 30:
        return JSONResponse({"Response": 400, "Message": "Color string must be 30 characters", "Solution": []})
    words = main(color_string)
    return words

if __name__ == "__main__":
    # For debugging: hot reload, port 8080
    uvicorn.run("fast_api_endpoint:app", host="0.0.0.0", port=8080, reload=True)
