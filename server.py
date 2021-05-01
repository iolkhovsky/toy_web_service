from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.face_detector import FaceDetector
from utils import decode_image

processor = FaceDetector()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://localhost",
    "https://localhost:80000",
    "http://0.0.0.0",
    "http://0.0.0.0:8000",
    "https://0.0.0.0",
    "https://0.0.0.0:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return FileResponse("static/ui.html")


@app.post("/image")
async def process_image(file: UploadFile = File(...)):
    content = await file.read()
    img = decode_image(content)
    img, data = processor(img)
    data = [{
        "label": f"face#{idx}",
        "score": 1.0,
        "bbox": [int(x) for x in box],
    } for idx, box in enumerate(data)]
    return JSONResponse({
        "id": file.filename,
        "file_size": len(content),
        "width": img.shape[1],
        "height": img.shape[0],
        "detections": data
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
