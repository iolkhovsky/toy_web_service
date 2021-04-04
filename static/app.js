function draw() {
  var canvas = document.getElementById("image-canvas");
  canvas.width = this.width;
  canvas.height = this.height;
  var ctx = canvas.getContext('2d');
  ctx.drawImage(this, 0, 0);
}

function failed() {
  window.alert("The provided file couldn't be loaded as an Image media");
}

function uploadedEventHandler(e) {
  var img = new Image();
  img.onload = draw;
  img.onerror = failed;
  img.src = URL.createObjectURL(this.files[0]);

  var formData = new FormData();
  formData.append("file", this.files[0]);

  var url = "http://localhost:8000/image";
  var request = new XMLHttpRequest();
  request.responseType = "json";
  request.open("POST", url, true);
  request.onload = function () {
    var data = request.response;
    document.getElementById("output").textContent = JSON.stringify(data);
  };
  request.send(formData);
}

document.getElementById("uploaded-file").onchange = uploadedEventHandler;
