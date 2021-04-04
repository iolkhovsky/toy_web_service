var boxes;
var canvas = document.getElementById("image-canvas");
var output_console = document.getElementById("output")
var det_table = document.getElementById("detections_table")

function show_detection_table(boxes) {
    var table_description = "";

    table_description = "<br>Detections</br>";
    table_description += "<table>";
    table_description += "<tr>" + "<th>#</th>" + "<th>X</th>" + "<th>Y</th>" +
        "<th>Width</th>" + "<th>Height</th>" + "</tr>";
    for (var i = 0; i < boxes.length; i++) {
        table_description += "<tr id='detection" + i + "'>";
        table_description +=
            "<td>" + i + "</td>" +
            "<td>" + JSON.stringify(boxes[i][0]) + "</td>" +
            "<td>" + JSON.stringify(boxes[i][1]) + "</td>" +
            "<td>" + JSON.stringify(boxes[i][2]) + "</td>" +
            "<td>" + JSON.stringify(boxes[i][3]) + "</td>";
        table_description += "</tr>";
    }
    table_description += "</table>";
    det_table.innerHTML = table_description;
}

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
  canvas.width = this.width;
  canvas.height = this.height;
  var ctx = canvas.getContext('2d');
  ctx.drawImage(this, 0, 0);
}

function draw_detections(boxes) {
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

  var url = "/image";
  var request = new XMLHttpRequest();
  request.responseType = "json";
  request.open("POST", url, true);
  request.onload = function () {
    boxes = request.response["detections"];
    output_console.textContent = JSON.stringify(boxes);
    draw_detections(boxes)
    show_detection_table(boxes)
  };
  request.send(formData);
  output_console.textContent = "Waiting for server's response...";
}

document.getElementById("uploaded-file").onchange = uploadedEventHandler;
