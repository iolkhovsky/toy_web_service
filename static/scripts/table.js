

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