function handlerFunction(e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type == "drop") {
        let dt = e.dataTransfer;
        let files = dt.files;
        handleFiles(files);
    }
}

function handleFiles(files) {
  ([...files]).forEach(uploadFile)
}

function uploadFile(file) {
  var img = new Image();
  img.onload = drawSourceImage;
  img.onerror = failed;
  img.src = URL.createObjectURL(file);

  var formData = new FormData();
  var url = "/image";
  var request = new XMLHttpRequest();
  request.responseType = "json";
  request.open("POST", url, true);
  request.onload = function () {
    boxes = request.response["detections"];
    imgWidth = request.response["width"];
    imgHeight = request.response["height"];
    transform = getImageCanvasTransform(imgWidth, imgHeight);
    output_console.textContent = JSON.stringify(boxes);
    update_detections_list(boxes);
    update_samples_list();
    drawDetections(boxes, [imgWidth, imgHeight], transform, highlight_idx);
  };
  formData.append('file', file);
  request.send(formData);
  output_console.textContent = "Waiting for server's response...";
}

let dropArea = document.getElementById("image-canvas")
dropArea.addEventListener('dragenter', handlerFunction, false)
dropArea.addEventListener('dragleave', handlerFunction, false)
dropArea.addEventListener('dragover', handlerFunction, false)
dropArea.addEventListener('drop', handlerFunction, false)