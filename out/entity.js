"use strict";
class Entity {
    x;
    y;
    objData = [];
    static img;
    static imgUrl = "none.png";
    static className = "Entity";
    static width = 1;
    static height = 1;
    static widthImg = 1;
    static heightImg = 1;
    static xImg = 0;
    static yImg = 0;
    static widthHitbox = 1;
    static heightHitbox = 1;
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.center();
    }
    static draw(canvas, size) {
        if (this.img == undefined)
            return;
        const coef = size / this.width;
        canvas.width = this.width * coef;
        canvas.height = this.height * coef;
        canvas.style.width = `${canvas.width}px`;
        canvas.style.height = `${canvas.height}px`;
        const ctx = getCanvasContext(canvas);
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(this.img, 0, 0, this.width, this.height, 0, 0, canvas.width, canvas.height);
    }
    ;
    draw() {
        const obj = this.constructor;
        if (obj.img == undefined)
            return;
        const width = obj.widthImg * TileSize;
        const height = obj.heightImg * TileSize;
        ctx.save();
        if (entity_moving && entity_moving.entity == this)
            ctx.translate(entity_moving.dx, entity_moving.dy);
        ctx.drawImage(obj.img, 0, 0, obj.width, obj.height, (this.x + obj.xImg) * TileSize, (this.y + obj.yImg) * TileSize, width, height);
        ctx.strokeStyle = "rgba(0, 0, 0, 0.5)";
        ctx.strokeRect(this.x * TileSize, this.y * TileSize, obj.widthHitbox * TileSize, obj.heightHitbox * TileSize);
        ctx.restore();
        if (selectedEntity == this) {
            const fontSize = TileSize / 5;
            ctx.save();
            ctx.font = `${fontSize}px Arial`;
            let line = 0;
            const drawLine = (text) => {
                ctx.fillText(text, this.x * TileSize + 2, this.y * TileSize + line * fontSize);
                line += 1;
            };
            for (let i = 0; i < this.objData.length; i++) {
                const data = this.objData[i];
                if (!data.displayColor)
                    continue;
                ctx.fillStyle = data.displayColor;
                ctx.strokeStyle = data.displayColor;
                ctx.lineWidth = 2;
                if (data.type == "bool" || data.type == "number" || data.type == "text") {
                    drawLine(`${data.name}: ${data.value}`);
                }
                else if (data.type == "area") {
                    const rect = data.value;
                    if (rect == null)
                        continue;
                    ctx.strokeRect(rect[0] * TileSize, rect[1] * TileSize, rect[2] * TileSize, rect[3] * TileSize);
                }
                else if (data.type == "aura") {
                    const rect = data.value;
                    if (rect == null)
                        continue;
                    ctx.strokeRect(this.x * TileSize + obj.widthHitbox * TileSize / 2 - rect[0] * TileSize, this.y * TileSize + obj.heightHitbox * TileSize / 2 - rect[1] * TileSize, rect[2] * TileSize, rect[3] * TileSize);
                }
                else if (data.type == 'tile') {
                    const point = data.value;
                    if (point == null)
                        continue;
                    ctx.save();
                    ctx.globalAlpha = 0.6;
                    ctx.fillRect(point[0] * TileSize, point[1] * TileSize, TileSize, TileSize);
                    ctx.restore();
                }
                else if (data.type == 'tiles') {
                    const points = data.value;
                    if (points == null)
                        continue;
                    ctx.save();
                    ctx.globalAlpha = 0.6;
                    for (let j = 0; j < points.length; j++) {
                        const point = points[j];
                        ctx.fillRect(point[0] * TileSize, point[1] * TileSize, TileSize, TileSize);
                    }
                    ctx.restore();
                }
            }
            ctx.restore();
        }
    }
    ;
    intersect(x, y) {
        const obj = this.constructor;
        const X = x / TileSize;
        const Y = y / TileSize;
        return X >= this.x && X <= this.x + obj.widthHitbox && Y >= this.y && Y <= this.y + obj.heightHitbox;
    }
    center() {
        const obj = this.constructor;
        this.x = Math.floor(this.x + obj.widthHitbox / 2) + (1 - obj.widthHitbox) / 2;
        this.y = Math.floor(this.y + obj.heightHitbox / 2) + (1 - obj.heightHitbox) / 2;
    }
    openMenu(vx, vy) {
        new EntityEditor(this, vx, vy).show();
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
        const classObj = EntityDict[data.className];
        if (!classObj) {
            console.error(`Cant create entity: No such class name "${data.className}"`);
            return;
        }
        ;
        const entity = new classObj(data.x, data.y);
        for (let i = 0; i < entity.objData.length; i++) {
            const dataEl = entity.objData[i];
            const value = data[dataEl.name];
            if (value === undefined) {
                console.error(`No such field "${dataEl.name}"`, data);
                dataEl.value = null;
                continue;
            }
            dataEl.value = value;
        }
        return entity;
    }
}
;
const EntityDict = {};
function createNewEntityClass(name, imgUrl, width, height, widthHitbox, heightHitbox, xImg, yImg, widthImg, heightImg, objData) {
    class Entity_New extends Entity {
        static imgUrl = imgUrl;
        static width = width;
        static height = height;
        static widthHitbox = widthHitbox;
        static heightHitbox = heightHitbox;
        static xImg = xImg;
        static yImg = yImg;
        static widthImg = widthImg;
        static heightImg = heightImg;
        static className = name;
        objData = JSON.parse(JSON.stringify(objData));
    }
    EntityDict[name] = Entity_New;
}
function createNewEntityClass_Auto(name, hasFolder, width, height, widthHitbox, heightHitbox, xImg, yImg, widthImg, heightImg, objData) {
    let imgUrl = name + ".png";
    if (hasFolder)
        imgUrl = name + "/stay.png";
    createNewEntityClass(name, imgUrl, width, height, widthHitbox, heightHitbox, xImg || 0, yImg || 0, widthImg || widthHitbox, heightImg || heightHitbox, objData || []);
}
