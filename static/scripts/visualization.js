const imageCanvasAspectRatio = 16. / 9.;
const imageCanvasShare = 0.65;
const imageCanvasWidth = window.innerWidth * imageCanvasShare;
const imageCanvasHeight = imageCanvasWidth / imageCanvasAspectRatio;


function drawDetection(context, box, label="", score=-1.0, color="#ff0000", lineWidth=1) {
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
  context.lineWidth = lineWidth;
  context.strokeStyle = color;
  context.stroke();

  context.font = "12pt Cambria";
  if (label.length) {
    if (score >= 0.)
        label += ": " + score.toString();
    context.fillText(label, x1, y1-10);
  }
}

function drawDetections(boxes, imgSize, transform, highlight_idx=-1) {
  var [imgWidth, imgHeight] = imgSize;
  var [x, y, w, h] = transform;
  var ctx = canvas.getContext('2d');
  var arrayLength = boxes.length;
  for (var i = 0; i < arrayLength; i++) {
    var [boxX, boxY, boxW, boxH] = boxes[i]["bbox"];
    var xScale = w / imgWidth;
    var yScale = h / imgHeight;
    boxX = x + boxX * xScale;
    boxY = y + boxY * yScale;
    boxW = boxW * xScale;
    boxH = boxH * yScale;
    if (i == highlight_idx)
        drawDetection(ctx, [boxX, boxY, boxW, boxH], boxes[i]["label"], boxes[i]["score"], color="#00ff00", lineWidth=4);
    else
        drawDetection(ctx, [boxX, boxY, boxW, boxH], boxes[i]["label"], boxes[i]["score"]);
  }
}

function getImageCanvasTransform(imageWidth, imageHeight) {
    currScaleX = canvas.width / imageWidth;
    currScaleY = canvas.height / imageHeight;
    scale = Math.min(currScaleX, currScaleY);
    targetImgWidth = imageWidth * scale;
    targetImgHeight = imageHeight * scale;
    offsetX = (imageCanvasWidth - targetImgWidth) / 2.;
    offsetY = (imageCanvasHeight - targetImgHeight) / 2.;
    return [offsetX, offsetY, targetImgWidth, targetImgHeight];
}

function drawSourceImage() {
  canvas.width = imageCanvasWidth;
  canvas.height = imageCanvasHeight;
  var [x, y, w, h] = getImageCanvasTransform(this.width, this.height);
  var ctx = canvas.getContext('2d');
  ctx.drawImage(this, x, y, w, h);
}
