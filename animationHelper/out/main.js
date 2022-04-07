"use strict";
const canvas = getCanvas("canvas");
const ctx = getCanvasContext(canvas);
const inp_width = getInput("inp-width");
const inp_height = getInput("inp-height");
const inp_rotate = getSelect("inp-rotate");
const inp_flip = getInput("inp-flip");
const inp_reverse = getInput("inp-reverse");
const inp_shift = getInput("inp-shift");
const inp_img = getInput("inp-img");
const inp_name = getInput("inp-name");
const btn_save = getButton("btn-save");
let img = document.createElement("img");
let frame = { w: 16, h: 16, c: 1, l: [] };
function setCanvasSize(origSize = false) {
    if (origSize) {
        const width = img.width;
        frame.c = img.width / inp_width.valueAsNumber;
        frame.w = inp_width.valueAsNumber;
        frame.h = inp_height.valueAsNumber;
        canvas.width = width;
        canvas.height = frame.h;
    }
    else {
        const width = Math.min(600, document.body.offsetWidth);
        frame.c = img.width / inp_width.valueAsNumber;
        frame.w = width / frame.c;
        frame.h = (frame.w / inp_width.valueAsNumber) * inp_height.valueAsNumber;
        canvas.width = width;
        canvas.height = frame.h;
    }
}
function splitImg() {
    let resolveF = () => { };
    frame.l = [];
    let loaded = 0;
    function onLoad() {
        loaded += 1;
        if (frame.l.length <= loaded)
            resolveF();
    }
    for (let i = 0; i < frame.c; i++) {
        const canvas = document.createElement('canvas');
        canvas.width = inp_width.valueAsNumber;
        canvas.height = inp_height.valueAsNumber;
        const context = canvas.getContext('2d');
        if (context) {
            context.drawImage(img, i * inp_width.valueAsNumber, 0, inp_width.valueAsNumber, inp_height.valueAsNumber, 0, 0, canvas.width, canvas.height);
            const image = document.createElement("img");
            image.src = canvas.toDataURL();
            image.addEventListener("load", () => onLoad());
            frame.l.push(image);
        }
    }
    return new Promise((resolve, reject) => {
        resolveF = resolve;
    });
}
inp_img.addEventListener("change", async () => {
    const curFiles = inp_img.files;
    if (!curFiles)
        return;
    if (curFiles.length == 0)
        return;
    const reader = new FileReader();
    const file = curFiles[0];
    inp_name.value = file.name;
    reader.onload = () => {
        img.src = `${reader.result}`;
    };
    reader.readAsDataURL(file);
});
img.addEventListener("load", async () => {
    setCanvasSize();
    await splitImg();
    redraw();
});
window.addEventListener("resize", () => redraw());
btn_save.addEventListener("click", () => {
    redraw(true);
    var dataURL = canvas.toDataURL("image/png", 1.0);
    downloadImage(dataURL, inp_name.value);
    redraw();
});
inp_width.addEventListener("change", async () => { await splitImg(); redraw(); });
inp_height.addEventListener("change", async () => { await splitImg(); redraw(); });
inp_rotate.addEventListener("change", () => redraw());
inp_flip.addEventListener("change", () => redraw());
inp_reverse.addEventListener("change", () => redraw());
inp_shift.addEventListener("change", () => redraw());
function redraw(origSize = false) {
    setCanvasSize(origSize);
    ctx.imageSmoothingEnabled = false;
    for (let i = 0; i < frame.l.length; i++) {
        let imgI = i;
        if (!isNaN(inp_shift.valueAsNumber))
            imgI = (imgI + inp_shift.valueAsNumber + frame.l.length) % frame.l.length;
        let img = frame.l[imgI];
        if (inp_reverse.checked)
            img = frame.l[frame.l.length - imgI - 1];
        ctx.save();
        ctx.translate(frame.w * i, 0);
        if (inp_rotate.value == "90") {
            ctx.rotate(Math.PI / 2);
            ctx.translate(0, -frame.h);
        }
        else if (inp_rotate.value == "180") {
            ctx.rotate(Math.PI);
            ctx.translate(-frame.w, -frame.h);
        }
        else if (inp_rotate.value == "270") {
            ctx.rotate(Math.PI / 2 * 3);
            ctx.translate(-frame.w, 0);
        }
        if (inp_flip.checked) {
            ctx.translate(frame.w, 0);
            ctx.scale(-1, 1);
        }
        ctx.drawImage(img, 0, 0, frame.w, frame.h);
        ctx.restore();
    }
}
function downloadImage(data, filename) {
    var el = document.createElement('a');
    el.setAttribute('href', data);
    el.setAttribute('download', filename);
    el.style.display = 'none';
    document.body.appendChild(el);
    el.click();
    document.body.removeChild(el);
}
