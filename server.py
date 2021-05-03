from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import io
import uvicorn

from backend.face_detector import FaceDetector
from utils import decode_image, init_repo, save_sample, get_processed_samples_list, read_sample, encode_image

processor = FaceDetector()
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

init_repo()

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
    return FileResponse("static/index.html")


@app.get("/samples", response_class=JSONResponse)
async def root(request: Request):
    return JSONResponse(get_processed_samples_list())


@app.get("/image", response_class=JSONResponse)
async def root(request: Request):
    processed_imgs = get_processed_samples_list()
    sample = processed_imgs[-1]
    if "sample_id" in request.query_params.keys():
        sample = request.query_params["sample_id"]
    img, report = read_sample(sample)
    encoded = encode_image(img)
    return StreamingResponse(io.BytesIO(encoded.tobytes()), media_type="image/jpg")


@app.get("/report", response_class=JSONResponse)
async def root(request: Request):
    processed_imgs = get_processed_samples_list()
    sample = processed_imgs[-1]
    if "sample_id" in request.query_params.keys():
        sample = request.query_params["sample_id"]
    img, report = read_sample(sample)
    return JSONResponse(report)


@app.post("/image")
async def process_image(file: UploadFile = File(...)):
    content = await file.read()
    img = decode_image(content)
    _, data = processor(img)
    data = [{
        "label": f"face#{idx}",
        "score": 1.0,
        "bbox": [int(x) for x in box],
    } for idx, box in enumerate(data)]
    processing_result = {
        "id": file.filename,
        "file_size": len(content),
        "width": img.shape[1],
        "height": img.shape[0],
        "detections": data
    }
    save_sample(file.filename, img, processing_result)
    return JSONResponse(processing_result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
