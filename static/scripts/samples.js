

function update_samples_list() {
    var request = new XMLHttpRequest();
    request.responseType = "json";
    var url = "/samples";
    request.open("GET", url, true);
    request.onload = function () {
        var samples_description = "<select id='samples_select' size='10'>";
        for (var i = 0; i < request.response.length; i++) {
            samples_description += "<option value=" + JSON.stringify(request.response[i]) + ">" + JSON.stringify(request.response[i]) +  "</option>";
        }
        samples_description += "</select>";
        samples_list.innerHTML = samples_description;

        var samples_select = document.getElementById("samples_select");
        if (samples_select != null) {
            samples_select.onchange = function() {
                var sample_id = samples_select.options[samples_select.selectedIndex].value;
                var img_req_url = "/image?sample_id=" + sample_id;
                var image_request = new XMLHttpRequest();
                image_request.responseType = "blob";
                image_request.open("GET", img_req_url, true);
                image_request.onload = function () {
                    var url = window.URL.createObjectURL(image_request.response);
                    var img = new Image();
                    img.onload = drawSourceImage;
                    img.onerror = failed;
                    img.src = url;

                    var rep_req_url = "/report?sample_id=" + sample_id;
                    var report_request = new XMLHttpRequest();
                    report_request.responseType = "json";
                    report_request.open("GET", rep_req_url, true);
                    report_request.onload = function () {
                        boxes = report_request.response["detections"];
                        imgWidth = report_request.response["width"];
                        imgHeight = report_request.response["height"];
                        transform = getImageCanvasTransform(imgWidth, imgHeight);
                        output_console.textContent = JSON.stringify(boxes);
                        update_detections_list(boxes);
                        drawDetections(boxes, [imgWidth, imgHeight], transform, highlight_idx);
                    };
                    report_request.send();
                };
                image_request.send();
            };
        };
    };
    request.send();
}