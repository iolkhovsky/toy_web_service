var boxes;
var canvas = document.getElementById("image-canvas");
var output_console = document.getElementById("output")
var det_table = document.getElementById("detections_table")
var samples_list = document.getElementById("samples_list")

function update_samples() {
    var request = new XMLHttpRequest();
    request.responseType = "json";
    var url = "/samples";
    request.open("GET", url, true);
    request.onload = function () {
        var samples_description = "<select id='select_sample' size='10'>";
        for (var i = 0; i < request.response.length; i++) {
            samples_description += "<option value=" + JSON.stringify(request.response[i]) + ">" + JSON.stringify(request.response[i]) +  "</option>";
        }
        samples_description += "</select>";
        samples_list.innerHTML = samples_description;

        var samples_select = document.getElementById("select_sample");
        if (samples_select != null) {
            samples_select.onchange = function() {
                var sample_id = samples_select.options[samples_select.selectedIndex].value;
                var req_url = "/image?sample_id=" + sample_id;
                var request = new XMLHttpRequest();
                request.responseType = "blob";
                request.open("GET", req_url, true);
                request.onload = function () {
                    var url = window.URL.createObjectURL(request.response);
                    var img = new Image();
                    img.onload = drawSourceImage;
                    img.onerror = failed;
                    img.src = url;
                };
                request.send();
            };
        };
    };
    request.send();
}

function init() {
    canvas.width = imageCanvasWidth;
    canvas.height = imageCanvasHeight;
    update_samples();
}

function failed() {
  window.alert("The provided file couldn't be loaded as an Image media");
}

function uploadedEventHandler(e) {
  var img = new Image();
  img.onload = drawSourceImage;
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
    var imgWidth = request.response["width"];
    var imgHeight = request.response["height"];
    var transform = getImageCanvasTransform(imgWidth, imgHeight);
    output_console.textContent = JSON.stringify(boxes);
    drawDetections(boxes, [imgWidth, imgHeight], transform);
    show_detection_table(boxes)
    update_samples()
  };
  request.send(formData);
  output_console.textContent = "Waiting for server's response...";
}

document.addEventListener('DOMContentLoaded', init);
document.getElementById("uploaded-file").onchange = uploadedEventHandler;
