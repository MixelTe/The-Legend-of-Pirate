"use strict";
class Decor {
    x;
    y;
    objData = [];
    canvas;
    static className = "Decor";
    static imgUrl = "none.png";
    static width = 1;
    static height = 1;
    static img;
    getWidth = () => this.constructor.width;
    getHeight = () => this.constructor.height;
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
    static draw(canvas, size) {
        if (!this.img)
            return;
        const coef = size / this.width;
        canvas.width = this.width * coef;
        canvas.height = this.height * coef;
        canvas.style.width = `${canvas.width}px`;
        canvas.style.height = `${canvas.height}px`;
        const ctx = getCanvasContext(canvas);
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(this.img, 0, 0, canvas.width, canvas.height);
    }
    ;
    draw(ctx) {
        const obj = this.constructor;
        if (obj.img == undefined)
            return;
        const selected = selectedDecors.includes(this);
        ctx.save();
        if (decor_moving && (decor_moving.decor == this || selected))
            ctx.translate(decor_moving.dx, decor_moving.dy);
        if (this.canvas) {
            ctx.drawImage(this.canvas, this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
        }
        else {
            ctx.drawImage(obj.img, this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
        }
        if (inp_mode_decor.checked) {
            if (selectedDecor == this)
                ctx.strokeStyle = "rgba(255, 0, 0, 0.5)";
            else
                ctx.strokeStyle = "rgba(0, 0, 0, 0.5)";
            ctx.strokeRect(this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
            if (selected) {
                ctx.strokeStyle = "rgba(255, 0, 0, 1)";
                if (selectedDecor == this)
                    ctx.lineWidth = 4;
                else
                    ctx.lineWidth = 2;
                ctx.strokeRect(this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
            }
        }
        ctx.restore();
    }
    ;
    intersect(x, y) {
        const obj = this.constructor;
        const X = x / TileSize;
        const Y = y / TileSize;
        return X >= this.x && X <= this.x + obj.width && Y >= this.y && Y <= this.y + obj.height;
    }
    center() {
        const obj = this.constructor;
        this.x = Math.floor(this.x) + (1 - obj.width) / 2;
        this.y = Math.floor(this.y) + (1 - obj.height) / 2;
    }
    snapToPixels() {
        this.x = Math.floor(this.x * 16) / 16;
        this.y = Math.floor(this.y * 16) / 16;
    }
    openMenu(vx, vy) {
        new ObjDataEditor(this, vx, vy).show();
    }
    getData() {
        const obj = this.constructor;
        const data = {
            className: obj.className,
            x: this.x,
            y: this.y,
        };
        this.objData.forEach(dataEl => {
            data[dataEl.name] = dataEl.value;
        });
        return data;
    }
    static fromData(data) {
        const classObj = DecorDict[data.className];
        if (!classObj) {
            console.error(`Cant create decor: No such class name "${data.className}"`);
            return;
        }
        ;
        const decor = new classObj(data.x, data.y);
        for (let i = 0; i < decor.objData.length; i++) {
            const dataEl = decor.objData[i];
            const value = data[dataEl.name];
            if (value === undefined) {
                console.error(`No such field "${dataEl.name}"`, data);
                continue;
            }
            dataEl.value = value;
        }
        decor.afterDataSet();
        return decor;
    }
    apllyData(data) {
        for (let i = 0; i < this.objData.length; i++) {
            const dataEl = this.objData[i];
            for (let j = 0; j < data.length; j++) {
                const el = data[j];
                if (el.name == dataEl.name) {
                    dataEl.value = JSON.parse(JSON.stringify(el.value));
                }
            }
        }
        this.afterDataSet();
    }
    afterDataSet() {
    }
}
const DecorDict = {};
function createSimpleDecorClass(name, imgUrl, width, height, objData) {
    class Decor_New extends Decor {
        static imgUrl = imgUrl;
        static width = width;
        static height = height;
        static className = name;
        objData = JSON.parse(JSON.stringify(objData));
    }
    DecorDict[name] = Decor_New;
}
function createSimpleDecorClass_Auto(name, folder, width, height, objData) {
    let imgUrl = name + ".png";
    if (folder)
        imgUrl = folder + "/" + name + ".png";
    createSimpleDecorClass(folder || name, imgUrl, width, height, objData || []);
}
