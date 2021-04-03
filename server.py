from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from backend.face_detector import FaceDetector
from utils import ProcessingItem, decode_image

processor = FaceDetector()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return FileResponse("static/ui.html")


@app.post("/image")
async def process_image(file: UploadFile = File(...)):
    content = await file.read()
    img = decode_image(content)
    img, data = processor(img)

    def preprocess_box(box):
        return [int(x) for x in box]

    data = [preprocess_box(x) for x in list(data)]
    return JSONResponse({
        "id": file.filename,
        "file_size": len(content),
        "detections": data
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
