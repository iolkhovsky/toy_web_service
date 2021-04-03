from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import io
import random
from pydantic import BaseModel
import uvicorn

from backend.face_detector import FaceDetector


processor = FaceDetector()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return FileResponse("static/ui.html")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
