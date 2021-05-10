

function update_detections_list(boxes) {
        var detections_description = "<select id='detections_select' size='10'>";
        for (var i = 0; i < boxes.length; i++) {
            var [x, y, w, h] = boxes[i]["bbox"];
            detections_description += "<option value=" + i + ">";
            detections_description += "#" + i + ": " + boxes[i]["label"] + " " + boxes[i]["score"] + " ";
            detections_description += x + " " + y + " " + w + " " + h + "</option>";
        }
        detections_description += "</select>";
        detections_list.innerHTML = detections_description;
        var detections_select = document.getElementById("detections_select");
        if (detections_select != null) {
            detections_select.onchange = function() {
                highlight_idx = detections_select.selectedIndex;
                redrawSourceImage();
                drawDetections(boxes, [imgWidth, imgHeight], transform, highlight_idx);
                redrawSubframe();
            }
        }
}