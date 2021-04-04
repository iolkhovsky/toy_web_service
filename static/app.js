var boxes;

function draw_box(context, box) {
  x1 = box[0]
  y1 = box[1]
  x2 = x1 + box[2]
  y2 = y1 + box[3]

  context.beginPath();
  context.moveTo(x1, y1);
  context.lineTo(x2, y1);
  context.lineTo(x2, y2);
  context.lineTo(x1, y2);
  context.lineTo(x1, y1);
  context.strokeStyle = '#ff0000';
  context.stroke();
}

function draw_source_image() {
  var canvas = document.getElementById("image-canvas");
  canvas.width = this.width;
  canvas.height = this.height;
  var ctx = canvas.getContext('2d');
  ctx.drawImage(this, 0, 0);
}

function draw_detections(boxes) {
  var canvas = document.getElementById("image-canvas");
  var ctx = canvas.getContext('2d');
  var arrayLength = boxes.length;
  for (var i = 0; i < arrayLength; i++) {
    draw_box(ctx, boxes[i])
  }
}

function failed() {
  window.alert("The provided file couldn't be loaded as an Image media");
}

function uploadedEventHandler(e) {
  var img = new Image();
  img.onload = draw_source_image;
  img.onerror = failed;
  img.src = URL.createObjectURL(this.files[0]);

  var formData = new FormData();
  formData.append("file", this.files[0]);

  var url = "http://localhost:8000/image";
  var request = new XMLHttpRequest();
  request.responseType = "json";
  request.open("POST", url, true);
  request.onload = function () {
    boxes = request.response["detections"];
    document.getElementById("output").textContent = JSON.stringify(boxes);
    draw_detections(boxes)
  };
  request.send(formData);
  document.getElementById("output").textContent = "Waiting for server's response...";
}

document.getElementById("uploaded-file").onchange = uploadedEventHandler;
