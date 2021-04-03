from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from backend.face_detector import FaceDetector
from utils import ProcessingItem, base64str_to_img

processor = FaceDetector()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return FileResponse("static/ui.html")


@app.put("/image")
async def process_image(imgdata: ProcessingItem):
    img = base64str_to_img(imgdata.EncodedImg)
    img, data = processor(img)
    return JSONResponse({
        "id": imgdata.RequestId,
        "encodedImgSize": len(imgdata.EncodedImg)
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
