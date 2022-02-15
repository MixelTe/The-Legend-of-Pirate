"use strict";
const inp_width = getInput("inp-width");
const inp_height = getInput("inp-height");
const inp_tilesize = getInput("inp-tilesize");
const btn_up = getButton("btn-up");
const btn_right = getButton("btn-right");
const btn_down = getButton("btn-down");
const btn_left = getButton("btn-left");
const btn_save = getButton("btn-save");
const inp_load = getInput("inp-load");
const btn_new = getButton("btn-new");
const inp_cameraSpeed = getInput("inp_cameraSpeed");
const inp_mode_pen = getInput("inp-mode-pen");
const inp_mode_fill = getInput("inp-mode-fill");
const inp_mode_view = getInput("inp-mode-view");
const inp_mode_entity = getInput("inp-mode-entity");
const inp_mode_decor = getInput("inp-mode-decor");
const inp_highlight_tiles = getInput("inp-highlight-tiles");
const inp_highlight_decor = getInput("inp-highlight-decor");
// const world_map = getTable("world-map")
const div_viewport = getDiv("viewport");
const div_palette = getDiv("palette");
const div_fast_palette = getDiv("fast-palette");
const div_palette_group = getDiv("palette-group");
const div_palette_group_imgs = getDiv("palette-group-imgs");
const canvas = getCanvas("canvas");
const ctx = getCanvasContext(canvas);
const localStorageKey = "WorldEditor-world-data";
const ViewWidth = 20;
const ViewHeight = 9;
let TileSize = 16 * 2;
// let TileSize = 16 * 4; // Temp
const entity = [];
for (const key in EntityDict)
    entity.push(EntityDict[key]);
const decor = [];
for (const key in DecorDict)
    decor.push(DecorDict[key]);
const tileImages = {};
const startViews_JSON = localStorage.getItem("WorldEditor-startViews");
const startViews = startViews_JSON ? JSON.parse(startViews_JSON) : [DefaultNewView];
let startView = 0;
let icon_move = null;
let icon_plus = null;
const icon_center_rect = () => { const size = TileSize * 2; return { x: (ViewWidth * TileSize - size) / 2, y: (ViewHeight * TileSize - size) / 2, w: size, h: size }; };
let icon_trash = null;
const icon_trash_rect = () => { const size = TileSize * 0.9; return { x: (ViewWidth - 0.5) * TileSize - size, y: TileSize / 2, w: size, h: size * 1.5 }; };
let icon_save = null;
const icon_save_rect = () => { const size = TileSize * 0.9; return { x: 0.5 * TileSize, y: ((ViewHeight - 0.5) * TileSize - size), w: size, h: size }; };
inp_tilesize.valueAsNumber = TileSize;
let camera_x = 0;
let camera_y = 0;
const camera_speed = () => {
    return Math.round(TileSize * inp_cameraSpeed.valueAsNumber / 2);
};
let penEntity = null;
let penDecor = null;
let penDecorData = null;
let selectedEntity = null;
let selectedDecor = null;
let worldFileName = localStorage.getItem("WorldEditor-world-filename") || "worldData.json";
let mousePos = { x: 0, y: 0 };
let mousePosCanvas = { x: 0, y: 0 };
let selectedEntities = [];
let selectedDecors = [];
class World {
    map = [];
    width;
    height;
    constructor(width, height, world) {
        this.width = width;
        this.height = height;
        inp_width.valueAsNumber = width;
        inp_height.valueAsNumber = height;
        this.map = [];
        if (world) {
            if (world.width > width) {
                for (let y = 0; y < world.height; y++) {
                    for (let x = width; x < world.width; x++) {
                        if (world.map[y][x]) {
                            const popup = new Popup();
                            popup.content.appendChild(Div([], [], "Уменьшение мира нельзя провести без потерь!"));
                            popup.open();
                            this.width = world.width;
                            this.height = world.height;
                            this.map = world.map;
                            return;
                        }
                    }
                }
            }
            if (world.height > height) {
                for (let y = height; y < world.height; y++) {
                    for (let x = 0; x < world.width; x++) {
                        if (world.map[y][x]) {
                            const popup = new Popup();
                            popup.content.appendChild(Div([], [], "Уменьшение мира нельзя провести без потерь!"));
                            popup.open();
                            this.width = world.width;
                            this.height = world.height;
                            this.map = world.map;
                            return;
                        }
                    }
                }
            }
            for (let y = 0; y < height; y++) {
                const line = [];
                for (let x = 0; x < width; x++) {
                    if (y < world.height && x < world.width) {
                        line.push(world.map[y][x]);
                    }
                    else {
                        line.push(undefined);
                    }
                }
                this.map.push(line);
            }
        }
        else {
            for (let y = 0; y < height; y++) {
                const line = [];
                for (let x = 0; x < width; x++) {
                    line.push(undefined);
                }
                this.map.push(line);
            }
        }
        // this.createTable();
    }
    up() {
        if (this.height == 0)
            return;
        const line = this.map.splice(0, 1);
        this.map.push(line[0]);
        this.createTable();
    }
    right() {
        if (this.width == 0)
            return;
        for (let y = 0; y < this.height; y++) {
            this.map[y].unshift(this.map[y].pop());
        }
        this.createTable();
    }
    down() {
        if (this.height == 0)
            return;
        const line = this.map.splice(this.height - 1, 1);
        this.map.unshift(line[0]);
        this.createTable();
    }
    left() {
        if (this.width == 0)
            return;
        for (let y = 0; y < this.height; y++) {
            this.map[y].push(this.map[y].shift());
        }
        this.createTable();
    }
    createTable() {
        // world_map.innerHTML = "";
        for (let y = 0; y < this.height; y++) {
            const row = document.createElement("tr");
            // world_map.appendChild(row);
            for (let x = 0; x < this.width; x++) {
                const cell = document.createElement("td");
                row.appendChild(cell);
                const btn = document.createElement("button");
                if (this.map[y][x])
                    btn.classList.add("active");
                cell.appendChild(btn);
                btn.addEventListener("click", async () => {
                    if (this.map[y][x]) {
                        const popup = new Popup();
                        popup.focusOn = "cancel";
                        popup.content.appendChild(Div([], [], "Вы уверены, что хотите удалить экран?"));
                        const r = await popup.openAsync();
                        if (r) {
                            const popup = new Popup();
                            popup.focusOn = "cancel";
                            popup.content.appendChild(Div([], [], "Вы точно уверены, что хотите удалить экран?"));
                            popup.reverse = true;
                            const r = await popup.openAsync();
                            if (!r)
                                return;
                        }
                        if (!r)
                            return;
                        this.map[y][x] = undefined;
                        btn.classList.remove("active");
                    }
                    else {
                        this.map[y][x] = new View();
                        btn.classList.add("active");
                    }
                });
            }
        }
    }
    draw() {
        const viewWidth = ViewWidth * TileSize;
        const viewHeight = ViewHeight * TileSize;
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                if (x * viewWidth + camera_x > canvas.width ||
                    y * viewHeight + camera_y > canvas.height ||
                    (x + 1) * viewWidth + camera_x < 0 ||
                    (y + 1) * viewHeight + camera_y < 0) {
                    continue;
                }
                const view = this.map[y][x];
                ctx.save();
                ctx.fillStyle = "lightblue";
                ctx.translate(x * viewWidth, y * viewHeight);
                ctx.fillRect(0, 0, viewWidth, viewHeight);
                if (view) {
                    ctx.save();
                    if (view_moving && view_moving.vx == x && view_moving.vy == y)
                        ctx.translate(view_moving.dx, view_moving.dy);
                    view.draw(x, y);
                    ctx.restore();
                }
                else {
                    if (inp_mode_view.checked && icon_plus) {
                        const rect = icon_center_rect();
                        ctx.drawImage(icon_plus, rect.x, rect.y, rect.w, rect.h);
                    }
                }
                ctx.restore();
            }
        }
        if (view_moving) {
            ctx.save();
            ctx.translate(view_moving.vx * viewWidth, view_moving.vy * viewHeight);
            ctx.translate(view_moving.dx, view_moving.dy);
            const view = this.map[view_moving.vy][view_moving.vx];
            if (view)
                view.draw();
            ctx.restore();
        }
        else if (inp_highlight_tiles.checked && !inp_mode_view.checked) {
            ctx.save();
            const { view, X, Y, vx, vy } = this.getView(mousePosCanvas.x - camera_x, mousePosCanvas.y - camera_y);
            if (vx >= this.width || vy >= this.height)
                return;
            const tilex = Math.floor(X / TileSize);
            const tiley = Math.floor(Y / TileSize);
            ctx.strokeStyle = "black";
            ctx.lineWidth = 2;
            ctx.strokeRect((vx * ViewWidth + tilex) * TileSize, (vy * ViewHeight + tiley) * TileSize, TileSize, TileSize);
            ctx.strokeStyle = "orange";
            ctx.strokeRect((vx * ViewWidth + tilex) * TileSize + 1, (vy * ViewHeight + tiley) * TileSize + 1, TileSize - 2, TileSize - 2);
            ctx.restore();
        }
    }
    getView(x, y) {
        const width = TileSize * ViewWidth;
        const height = TileSize * ViewHeight;
        const X = Math.floor(x / width);
        const Y = Math.floor(y / height);
        if (X >= this.width || Y >= this.height)
            return { view: null, X, Y, vx: X, vy: Y };
        return { view: this.map[Y][X] || null, X: x - X * width, Y: y - Y * height, vx: X, vy: Y };
    }
    findView(obj) {
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const view = this.map[y][x];
                if (!view)
                    continue;
                let i = -1;
                if (obj instanceof Decor)
                    i = view.decor.indexOf(obj);
                else
                    i = view.entity.indexOf(obj);
                if (i > -1)
                    return { view, i };
            }
        }
        return { view: null, i: -1 };
    }
    fill(x, y) {
        const { view, X, Y } = this.getView(x, y);
        if (view)
            view.fill(X, Y);
    }
    pen(x, y) {
        const { view, X, Y } = this.getView(x, y);
        if (view)
            view.pen(X, Y);
    }
    pick(x, y) {
        const { view, X, Y } = this.getView(x, y);
        if (view)
            view.pick(X, Y);
    }
    setCursor(x, y) {
        const { view, X, Y } = this.getView(x, y);
        if (view)
            view.setCursor(X, Y);
        else
            setCursor("pointer");
    }
    mousedown(x, y) {
        const { view, X, Y, vx, vy } = this.getView(x - camera_x, y - camera_y);
        if (!view)
            return;
        view.mousedown(X, Y, x, y, vx, vy);
    }
    mouseup(x, y) {
        const { view, X, Y, vx, vy } = this.getView(x - camera_x, y - camera_y);
        if (view_moving) {
            if (view)
                return;
            if (vx >= this.width || vy >= this.height || vx < 0 || vy < 0)
                return;
            this.map[vy][vx] = this.map[view_moving.vy][view_moving.vx];
            this.map[view_moving.vy][view_moving.vx] = undefined;
            return;
        }
        if (view)
            view.mouseup(X, Y, vx, vy);
        else {
            const data = JSON.parse(startViews[startView]);
            this.map[vy][vx] = View.fromData(data);
        }
    }
    getEntity(x, y) {
        const { view, X, Y, vx, vy } = this.getView(x, y);
        return { entity: view && view.getEntity(X, Y) || null, vx, vy };
    }
    getDecor(x, y) {
        const { view, X, Y, vx, vy } = this.getView(x, y);
        return { decor: view && view.getDecor(X, Y) || null, vx, vy };
    }
    entity(x, y) {
        const { view, X, Y } = this.getView(x, y);
        if (view)
            view.setEntity(X, Y);
    }
    decor(x, y) {
        const { view, X, Y } = this.getView(x, y);
        if (view)
            view.setDecor(X, Y);
    }
    saveToLocalStarage() {
        const data = this.getData();
        const json = JSON.stringify(data);
        localStorage.setItem(localStorageKey, json);
    }
    getData() {
        const data = {
            width: this.width,
            height: this.height,
            map: [],
        };
        for (let y = 0; y < this.height; y++) {
            const row = [];
            for (let x = 0; x < this.width; x++) {
                const view = this.map[y][x];
                if (view)
                    row.push(view.getData());
                else
                    row.push(undefined);
            }
            data.map.push(row);
        }
        return data;
    }
    static fromData(data) {
        const world = new World(data.width, data.height);
        for (let y = 0; y < data.height; y++) {
            for (let x = 0; x < data.width; x++) {
                const vData = data.map[y][x];
                if (vData)
                    world.map[y][x] = View.fromData(vData);
            }
        }
        return world;
    }
    static loadFromLocalStorage() {
        const json = localStorage.getItem(localStorageKey);
        if (!json)
            return;
        World.loadData(json);
    }
    static loadData(json) {
        try {
            const data = JSON.parse(json);
            const newWorld = World.fromData(data);
            world = newWorld;
        }
        catch (error) {
            console.error(error);
            const popup = new Popup();
            popup.cancelBtn = false;
            popup.content.appendChild(Div([], [], "Произошла ошибка при загрузке данных"));
            popup.open();
        }
    }
    calcSelected() {
        if (!selection)
            return;
        selectedDecors = [];
        selectedEntities = [];
        const selectionWorld = {
            x: (selection.x - camera_x) / TileSize,
            y: (selection.y - camera_y) / TileSize,
            w: (mousePosCanvas.x - selection.x) / TileSize,
            h: (mousePosCanvas.y - selection.y) / TileSize,
        };
        normalizeRect(selectionWorld);
        for (let y = 0; y < this.height; y++) {
            for (let x = 0; x < this.width; x++) {
                const view = this.map[y][x];
                if (!view)
                    continue;
                if (rectIntersect(selectionWorld, { x: x * ViewWidth, y: y * ViewHeight, w: ViewWidth, h: ViewHeight })) {
                    if (inp_mode_entity.checked) {
                        for (const entity of view.entity) {
                            if (rectIntersect(selectionWorld, { x: x * ViewWidth + entity.x, y: y * ViewHeight + entity.y, w: entity.getWidth(), h: entity.getHeight() })) {
                                selectedEntities.push(entity);
                            }
                        }
                    }
                    else if (inp_mode_decor.checked) {
                        for (const decor of view.decor) {
                            if (rectIntersect(selectionWorld, { x: x * ViewWidth + decor.x, y: y * ViewHeight + decor.y, w: decor.getWidth(), h: decor.getHeight() })) {
                                selectedDecors.push(decor);
                            }
                        }
                    }
                }
            }
        }
    }
}
class View {
    tiles = [];
    entity = [];
    decor = [];
    constructor() {
        for (let y = 0; y < ViewHeight; y++) {
            const line = [];
            for (let x = 0; x < ViewWidth; x++) {
                line.push(new Tile("water_deep"));
                // if (x == 0 || x == ViewWidth - 1 || y == 0 || y == ViewHeight - 1)
                // {
                // 	line.push(new Tile("water_deep"))
                // }
                // else
                // {
                // 	const random = Math.floor(Math.random() * 3);
                // 	if (random == 0) line.push(new Tile("sand1"));
                // 	else if (random == 1) line.push(new Tile("sand2"));
                // 	else line.push(new Tile("sand3"));
                // 	if (x == 1 || x == ViewWidth - 2 || y == 1 || y == ViewHeight - 2)
                // 	{
                // 		const d = new DecorDict["tileEdge_water_deep"](x, y);
                // 		this.decor.push(d);
                // 		if (x == 1 && y == 1) d.objData[0].value = [true, false, false, true];
                // 		else if (x == 1 && y == ViewHeight - 2)  d.objData[0].value = [false, false, true, true];
                // 		else if (x == ViewWidth - 2 && y == 1)  d.objData[0].value = [true, true, false, false];
                // 		else if (x == ViewWidth - 2 && y == ViewHeight - 2)  d.objData[0].value = [false, true, true, false];
                // 		else if (x == 1)  d.objData[0].value = [false, false, false, true];
                // 		else if (x == ViewWidth - 2)  d.objData[0].value = [false, true, false, false];
                // 		else if (y == 1)  d.objData[0].value = [true, false, false, false];
                // 		else if (y == ViewHeight - 2) d.objData[0].value = [false, false, true, false];
                // 		d.afterDataSet();
                // 	}
                // }
            }
            this.tiles.push(line);
        }
    }
    draw(x, y) {
        for (let y = 0; y < ViewHeight; y++) {
            for (let x = 0; x < ViewWidth; x++) {
                let tile = this.tiles[y][x];
                ctx.save();
                ctx.translate(x * TileSize, y * TileSize);
                tile.draw(ctx);
                ctx.restore();
            }
        }
        ctx.save();
        if (inp_highlight_decor.checked && !inp_mode_decor.checked)
            ctx.globalAlpha = 0.2;
        this.decor.forEach(d => d.draw(ctx));
        ctx.restore();
        ctx.save();
        if (!inp_mode_entity.checked)
            ctx.globalAlpha = 0.5;
        this.entity.forEach(e => e.draw(ctx));
        ctx.restore();
        ctx.strokeStyle = "black";
        ctx.lineWidth = 1;
        ctx.strokeRect(0, 0, ViewWidth * TileSize, ViewHeight * TileSize);
        if (inp_mode_view.checked) {
            ctx.save();
            ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
            ctx.fillRect(0, 0, ViewWidth * TileSize, ViewHeight * TileSize);
            if (icon_move) {
                const rect = icon_center_rect();
                ctx.drawImage(icon_move, rect.x, rect.y, rect.w, rect.h);
            }
            if (icon_trash) {
                const rect = icon_trash_rect();
                ctx.drawImage(icon_trash, rect.x, rect.y, rect.w, rect.h);
            }
            if (icon_save) {
                const rect = icon_save_rect();
                ctx.drawImage(icon_save, rect.x, rect.y, rect.w, rect.h);
            }
            if (x != undefined && y != undefined) {
                ctx.save();
                ctx.font = `${TileSize}px Arial`;
                ctx.fillStyle = "lime";
                ctx.fillText(`${x}:${y}`, TileSize * 0.3, TileSize);
                ctx.restore();
            }
            ctx.restore();
        }
    }
    drawInd(ctx) {
        for (let y = 0; y < ViewHeight; y++) {
            for (let x = 0; x < ViewWidth; x++) {
                let tile = this.tiles[y][x];
                ctx.save();
                ctx.translate(x * TileSize, y * TileSize);
                tile.draw(ctx);
                ctx.restore();
            }
        }
        this.decor.forEach(d => d.draw(ctx));
        this.entity.forEach(e => e.draw(ctx));
    }
    fill(x, y) {
        const X = Math.floor(x / TileSize);
        const Y = Math.floor(y / TileSize);
        const tile = this.tiles[Y][X].id;
        const tiles = [];
        const group = PenTiles.getGroup(tile);
        if (group && group.random) {
            for (const k in tileGroups[group.key].tiles)
                tiles.push(k);
        }
        else {
            tiles.push(tile);
        }
        this.fillR(X, Y, tiles, []);
    }
    fillR(x, y, tiles, path) {
        if (x < 0 || y < 0 || x >= ViewWidth || y >= ViewHeight)
            return;
        if (!tiles.includes(this.tiles[y][x].id))
            return;
        this.tiles[y][x].id = pen.getTile();
        const key = (x, y) => y * ViewWidth + x;
        path.push(key(x, y));
        if (path.indexOf(key(x + 1, y)) == -1)
            this.fillR(x + 1, y, tiles, path);
        if (path.indexOf(key(x - 1, y)) == -1)
            this.fillR(x - 1, y, tiles, path);
        if (path.indexOf(key(x, y + 1)) == -1)
            this.fillR(x, y + 1, tiles, path);
        if (path.indexOf(key(x, y - 1)) == -1)
            this.fillR(x, y - 1, tiles, path);
    }
    pen(x, y) {
        const X = Math.floor(x / TileSize);
        const Y = Math.floor(y / TileSize);
        this.tiles[Y][X].id = pen.getTile();
    }
    pick(x, y) {
        const X = Math.floor(x / TileSize);
        const Y = Math.floor(y / TileSize);
        const tile = this.tiles[Y][X].id;
        pen.setPen(tile);
        pen.setGroup(PenTiles.getGroup(tile));
    }
    setCursor(x, y) {
        if (rectPointIntersect(icon_trash_rect(), { x, y })) {
            setCursor("pointer");
        }
        else if (rectPointIntersect(icon_save_rect(), { x, y })) {
            setCursor("pointer");
        }
        else {
            setCursor("move");
        }
    }
    mousedown(x, y, rx, ry, vx, vy) {
        if (rectPointIntersect(icon_trash_rect(), { x, y })) { }
        else if (rectPointIntersect(icon_save_rect(), { x, y })) { }
        else {
            view_moving = { x: rx, y: ry, dx: 0, dy: 0, vx, vy };
        }
    }
    async mouseup(x, y, vx, vy) {
        if (rectPointIntersect(icon_trash_rect(), { x, y })) {
            const popup = new Popup();
            popup.focusOn = "cancel";
            popup.content.appendChild(Div([], [], "Вы уверены, что хотите удалить экран?"));
            const r = await popup.openAsync();
            if (r) {
                const popup = new Popup();
                popup.focusOn = "cancel";
                popup.content.appendChild(Div([], [], "Вы точно уверены, что хотите удалить экран?"));
                popup.reverse = true;
                const r = await popup.openAsync();
                if (!r)
                    return;
            }
            if (!r)
                return;
            world.map[vy][vx] = undefined;
        }
        else if (rectPointIntersect(icon_save_rect(), { x, y })) {
            const popup = new Popup();
            popup.focusOn = "cancel";
            popup.content.appendChild(Div([], [], "Сохранить экран в палитре?"));
            const r = await popup.openAsync();
            if (!r)
                return;
            const data = JSON.stringify(this.getData());
            div_palette.children[startView].classList.remove("palette-view-selected");
            startView = startViews.push(data) - 1;
            localStorage.setItem("WorldEditor-startViews", JSON.stringify(startViews));
            setPalete();
            div_palette.children[startView].classList.add("palette-view-selected");
        }
    }
    getEntity(x, y) {
        for (let i = 0; i < this.entity.length; i++) {
            const e = this.entity[i];
            if (e.intersect(x, y))
                return e;
        }
        return null;
    }
    getDecor(x, y) {
        for (let i = 0; i < this.decor.length; i++) {
            const e = this.decor[i];
            if (e.intersect(x, y))
                return e;
        }
        return null;
    }
    setEntity(x, y) {
        if (penEntity && !this.getEntity(x, y)) {
            const e = new penEntity(x / TileSize, y / TileSize);
            if (ctrl)
                e.snapToPixels();
            else
                e.center();
            this.entity.push(e);
            selectedEntity = e;
        }
    }
    setDecor(x, y) {
        if (penDecor && !this.getDecor(x, y)) {
            const d = new penDecor(x / TileSize, y / TileSize);
            if (penDecorData)
                d.apllyData(penDecorData);
            if (ctrl)
                d.snapToPixels();
            else
                d.center();
            this.decor.push(d);
            penDecorData = d.objData;
            selectedDecor = d;
        }
    }
    getData() {
        const data = {
            tiles: [],
            entity: [],
            decor: [],
        };
        for (let y = 0; y < ViewHeight; y++) {
            const row = [];
            for (let x = 0; x < ViewWidth; x++) {
                row.push(this.tiles[y][x].id);
            }
            data.tiles.push(row);
        }
        this.entity.forEach(e => data.entity.push(e.getData()));
        this.decor.forEach(d => data.decor.push(d.getData()));
        return data;
    }
    static fromData(data) {
        const view = new View();
        view.decor = [];
        for (let y = 0; y < ViewHeight && y < data.tiles.length; y++) {
            for (let x = 0; x < ViewWidth && x < data.tiles[y].length; x++) {
                view.tiles[y][x] = new Tile(data.tiles[y][x]);
            }
        }
        data.entity.forEach(eData => {
            const entity = Entity.fromData(eData);
            if (entity)
                view.entity.push(entity);
        });
        if (!data.decor)
            return view;
        data.decor.forEach(dData => {
            const decor = Decor.fromData(dData);
            if (decor)
                view.decor.push(decor);
        });
        return view;
    }
}
class Tile {
    id = "sand1";
    constructor(id) {
        if (id)
            this.id = id;
    }
    draw(ctx) {
        const img = tileImages[this.id];
        if (img) {
            ctx.drawImage(img, 0, 0, TileSize, TileSize);
        }
    }
}
class MiniMap {
    canvas = getCanvas("minimap");
    ctx = getCanvasContext(this.canvas);
    size = 20;
    constructor() {
        this.canvas.addEventListener("contextmenu", e => e.preventDefault());
        this.canvas.addEventListener("mousedown", e => {
            const x = Math.min(Math.floor(e.offsetX / this.size), world.width);
            const y = Math.min(Math.floor(e.offsetY / this.size), world.height);
            const X = x * TileSize * ViewWidth;
            const Y = y * TileSize * ViewHeight;
            if (e.button == 0) {
                camera_x = -(X - Math.round((canvas.width - ViewWidth * TileSize) / 2));
                camera_y = -(Y - Math.round((canvas.height - ViewHeight * TileSize) / 2));
                normalizeCamera();
            }
            else {
                centerView(X, Y);
            }
        });
    }
    draw() {
        this.canvas.width = (this.size + 1) * world.width + 2;
        this.canvas.height = (this.size + 1) * world.height + 2;
        for (let y = 0; y < world.height; y++) {
            for (let x = 0; x < world.width; x++) {
                if (world.map[y] && world.map[y][x])
                    this.ctx.fillStyle = "rgb(243, 200, 81)";
                else
                    this.ctx.fillStyle = "rgb(177, 225, 255)";
                this.ctx.fillRect(x * (this.size + 1) + 1, y * (this.size + 1) + 1, this.size, this.size);
            }
        }
        const coefX = (this.canvas.width - 2) / (world.width * ViewWidth * TileSize);
        const coefY = (this.canvas.height - 2) / (world.height * ViewHeight * TileSize);
        this.ctx.strokeStyle = "blue";
        this.ctx.strokeRect(-camera_x * coefX + 1, -camera_y * coefY + 1, canvas.width * coefX, canvas.height * coefY);
    }
}
class FastPalette {
    opened = false;
    closedByClick = false;
    imgs = [];
    tiles = [pen.getTile()];
    entity = [penEntity];
    decor = [penDecor];
    hovered = null;
    addtileI = 1;
    addentityI = 1;
    adddecorI = 1;
    constructor() {
        const imgs = div_fast_palette.querySelectorAll(".fast-palette-part");
        for (let i = 0; i < imgs.length; i++) {
            const el = imgs[i];
            if (el instanceof HTMLDivElement) {
                this.imgs.push(el);
                el.addEventListener("mouseover", () => this.hovered = i);
                el.addEventListener("click", () => {
                    this.hovered = i;
                    this.close(true);
                });
            }
        }
    }
    open() {
        if (this.opened)
            return;
        this.hovered = null;
        this.opened = true;
        this.closedByClick = false;
        if (inp_mode_entity.checked)
            this.setPaletteEntity();
        else if (inp_mode_decor.checked)
            this.setPaletteDecor();
        else
            this.setPaletteTiles();
        div_fast_palette.style.left = `${mousePos.x}px`;
        div_fast_palette.style.top = `${mousePos.y}px`;
        div_fast_palette.classList.add("fast-palette-visible");
    }
    setPaletteTiles() {
        for (let i = 0; i < this.imgs.length; i++) {
            const imgDiv = this.imgs[i];
            imgDiv.innerHTML = "";
            const imgTile = this.tiles.length > i ? tileImages[this.tiles[i]] : tileImages[this.tiles[0]];
            if (!imgTile)
                continue;
            const img = document.createElement("img");
            img.src = imgTile?.src;
            imgDiv.appendChild(img);
        }
    }
    setPaletteEntity() {
        for (let i = 0; i < this.imgs.length; i++) {
            const imgDiv = this.imgs[i];
            imgDiv.innerHTML = "";
            const e = this.entity.length > i ? this.entity[i] : this.entity[0];
            if (!e) {
                const img = document.createElement("img");
                img.src = "imgs/none.png";
                imgDiv.appendChild(img);
                continue;
            }
            const img = document.createElement("canvas");
            e.draw(img, 65);
            imgDiv.appendChild(img);
        }
    }
    setPaletteDecor() {
        for (let i = 0; i < this.imgs.length; i++) {
            const imgDiv = this.imgs[i];
            imgDiv.innerHTML = "";
            const d = this.decor.length > i ? this.decor[i] : this.decor[0];
            if (!d) {
                const img = document.createElement("img");
                img.src = "imgs/none.png";
                imgDiv.appendChild(img);
                continue;
            }
            const img = document.createElement("canvas");
            d.draw(img, 65);
            imgDiv.appendChild(img);
        }
    }
    close(closedByClick = false) {
        this.opened = false || this.closedByClick;
        div_fast_palette.classList.remove("fast-palette-visible");
        if (this.closedByClick || this.hovered == null)
            return;
        this.closedByClick = closedByClick;
        if (inp_mode_entity.checked)
            penEntity = this.entity.length > this.hovered ? this.entity[this.hovered] : this.entity[0];
        else if (inp_mode_decor.checked) {
            penDecor = this.decor.length > this.hovered ? this.decor[this.hovered] : this.decor[0];
            penDecorData = null;
        }
        else {
            const tile = this.tiles.length > this.hovered ? this.tiles[this.hovered] : this.tiles[0];
            pen.setPen(tile);
            pen.setGroup(PenTiles.getGroup(tile));
        }
    }
    addTile(tileid) {
        if (this.tiles.indexOf(tileid) != -1)
            return;
        this.tiles[this.addtileI] = tileid;
        this.addtileI = (this.addtileI + 1) % this.imgs.length;
    }
    addEntity(entity) {
        if (this.entity.indexOf(entity) != -1)
            return;
        this.entity[this.addentityI] = entity;
        this.addentityI = (this.addentityI + 1) % this.imgs.length;
    }
    addDecor(decor) {
        if (this.decor.indexOf(decor) != -1)
            return;
        this.decor[this.addentityI] = decor;
        this.adddecorI = (this.adddecorI + 1) % this.imgs.length;
    }
}
class PenTiles {
    pen = "sand1";
    group = null;
    groupTiles = ["sand1"];
    constructor() {
        div_palette_group.addEventListener("click", () => {
            div_palette_group.classList.remove("fast-palette-visible");
        });
    }
    setPen(tile, resetGroup = true) {
        if (resetGroup)
            this.group = null;
        this.pen = tile;
        fastPalette.addTile(this.pen);
    }
    getTile() {
        if (!this.group?.random)
            return this.pen;
        if (this.groupTiles.length == 0)
            return this.group.key;
        return this.groupTiles[Math.floor(Math.random() * this.groupTiles.length)];
    }
    openGroup(group) {
        if (group == undefined) {
            if (this.group && !this.group.random) {
                div_palette_group.classList.toggle("fast-palette-visible");
            }
            return;
        }
        this.setGroup(group);
        if (group.random)
            return;
        div_palette_group.classList.add("fast-palette-visible");
    }
    setGroup(group) {
        if (!group)
            return;
        this.group = group;
        this.groupTiles = [];
        if (group.random) {
            for (const k in tileGroups[group.key].tiles)
                this.groupTiles.push(k);
        }
        div_palette_group_imgs.innerHTML = "";
        for (const k in tileGroups[group.key].tiles) {
            const key = k;
            function addImg() {
                if (inp_mode_entity.checked)
                    return;
                const img = tileImages[key];
                if (img) {
                    const imgNew = document.createElement("img");
                    imgNew.src = img.src;
                    imgNew.title = key;
                    div_palette_group_imgs.appendChild(imgNew);
                    imgNew.addEventListener("click", () => {
                        pen.setPen(key, false);
                        div_palette_group.classList.remove("fast-palette-visible");
                    });
                }
                else
                    setTimeout(addImg, 100);
            }
            addImg();
        }
    }
    static getGroup(tile) {
        for (const group of tileList) {
            if (group.key == tile)
                return group;
            if (group.group) {
                const tiles = tileGroups[group.key].tiles;
                for (const key in tiles) {
                    if (key == tile)
                        return group;
                }
            }
        }
        return undefined;
    }
}
const pen = new PenTiles();
let world = new World(0, 0);
const minimap = new MiniMap();
const fastPalette = new FastPalette();
inp_width.addEventListener("change", () => {
    world = new World(inp_width.valueAsNumber, inp_height.valueAsNumber, world);
    inp_width.valueAsNumber = world.width;
    inp_height.valueAsNumber = world.height;
});
inp_height.addEventListener("change", () => {
    world = new World(inp_width.valueAsNumber, inp_height.valueAsNumber, world);
    inp_width.valueAsNumber = world.width;
    inp_height.valueAsNumber = world.height;
});
btn_up.addEventListener("click", () => world.up());
btn_right.addEventListener("click", () => world.right());
btn_down.addEventListener("click", () => world.down());
btn_left.addEventListener("click", () => world.left());
btn_save.addEventListener("click", () => {
    const text = JSON.stringify(world.getData());
    var el = document.createElement('a');
    el.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    el.setAttribute('download', worldFileName);
    el.style.display = 'none';
    document.body.appendChild(el);
    el.click();
    document.body.removeChild(el);
});
inp_load.addEventListener("input", async () => {
    const curFiles = inp_load.files;
    if (!curFiles)
        return;
    if (curFiles.length == 0)
        return;
    if (world.height != 0 && world.width != 0) {
        if (!await askForSure("заменить текущий мир"))
            return;
    }
    const file = curFiles[0];
    worldFileName = file.name;
    localStorage.setItem("WorldEditor-world-filename", worldFileName);
    const data = await file.text();
    World.loadData(data);
});
btn_new.addEventListener("click", async () => {
    if (world.height != 0 && world.width != 0) {
        if (!await askForSure("создать пустой мир"))
            return;
    }
    world = new World(inp_width.valueAsNumber, inp_height.valueAsNumber);
    worldFileName = "worldData.json";
    localStorage.setItem("WorldEditor-world-filename", worldFileName);
});
inp_tilesize.addEventListener("change", () => TileSize = inp_tilesize.valueAsNumber);
inp_mode_entity.addEventListener("change", () => {
    if (inp_mode_entity.checked)
        inp_mode_decor.checked = false;
    setPalete();
});
inp_mode_decor.addEventListener("change", () => {
    if (inp_mode_decor.checked)
        inp_mode_entity.checked = false;
    setPalete();
});
inp_mode_view.addEventListener("change", () => {
    setPalete();
});
canvas.addEventListener("wheel", e => {
    const moveSpeed = camera_speed();
    if (e.ctrlKey) {
        e.preventDefault();
        const x = (mousePosCanvas.x - camera_x) / TileSize;
        const y = (mousePosCanvas.y - camera_y) / TileSize;
        const v = 1.4;
        if (e.deltaY > 0)
            TileSize /= v;
        else
            TileSize *= v;
        TileSize = Math.max(Math.round(TileSize), 2);
        camera_x = -x * TileSize + mousePosCanvas.x;
        camera_y = -y * TileSize + mousePosCanvas.y;
        inp_tilesize.valueAsNumber = TileSize;
        normalizeCamera();
    }
    else if (e.shiftKey) {
        if (e.deltaY > 0)
            camera_x -= moveSpeed;
        else
            camera_x += moveSpeed;
        normalizeCamera();
    }
    else {
        if (e.deltaY > 0)
            camera_y -= moveSpeed;
        else
            camera_y += moveSpeed;
        normalizeCamera();
    }
});
let camera_moving = null;
let view_moving = null;
let entity_moving = null;
let decor_moving = null;
let selection = null;
let drawing = null;
let ctrl = false;
canvas.addEventListener("mousedown", e => {
    e.preventDefault();
    if (e.button == 0) {
        if (camera_moving) {
            centerView(e.offsetX - camera_x, e.offsetY - camera_y);
            camera_moving = null;
            return;
        }
        if (inp_mode_view.checked) {
            world.mousedown(e.offsetX, e.offsetY);
        }
        else if (inp_mode_entity.checked) {
            const { entity } = world.getEntity(e.offsetX - camera_x, e.offsetY - camera_y);
            if (entity) {
                if (ctrl)
                    entity.snapToPixels();
                else
                    entity.center();
                entity_moving = { x: e.offsetX, y: e.offsetY, dx: 0, dy: 0, entity };
                selectedEntity = entity;
            }
            else {
                drawing = "entity";
                selectedEntity = null;
            }
        }
        else if (inp_mode_decor.checked) {
            const { decor } = world.getDecor(e.offsetX - camera_x, e.offsetY - camera_y);
            if (decor) {
                if (ctrl)
                    decor.snapToPixels();
                else
                    decor.center();
                decor_moving = { x: e.offsetX, y: e.offsetY, dx: 0, dy: 0, decor };
                selectedDecor = decor;
            }
            else {
                drawing = "decor";
                selectedDecor = null;
            }
        }
        else {
            if (inp_mode_pen.checked) {
                drawing = "pen";
            }
            else {
                drawing = "fill";
            }
        }
    }
    if (e.button == 2) {
        if (drawing) {
            centerView(e.offsetX - camera_x, e.offsetY - camera_y);
            drawing = null;
            return;
        }
        camera_moving = { x: e.offsetX, y: e.offsetY, cx: camera_x, cy: camera_y };
        setCursor("move");
    }
    if (e.button == 1) {
        if (e.ctrlKey) {
            if (inp_mode_entity.checked) {
                const { entity } = world.getEntity(e.offsetX - camera_x, e.offsetY - camera_y);
                if (entity) {
                    const i = selectedEntities.indexOf(entity);
                    if (i >= 0)
                        selectedEntities.splice(i, 1);
                    else
                        selectedEntities.push(entity);
                }
            }
            else if (inp_mode_decor.checked) {
                const { decor } = world.getDecor(e.offsetX - camera_x, e.offsetY - camera_y);
                if (decor) {
                    const i = selectedDecors.indexOf(decor);
                    if (i >= 0)
                        selectedDecors.splice(i, 1);
                    else
                        selectedDecors.push(decor);
                }
            }
            if (selection) {
                selection.cx = e.offsetX;
                selection.cy = e.offsetY;
            }
        }
        else {
            selection = { x: e.offsetX, y: e.offsetY, cx: e.offsetX, cy: e.offsetY, changed: false };
        }
    }
});
canvas.addEventListener("mousemove", e => {
    mousePosCanvas.x = e.offsetX;
    mousePosCanvas.y = e.offsetY;
    setCursor("none");
    if (selection) {
        if (Math.abs(e.offsetX - selection.cx) > 5 || Math.abs(e.offsetY - selection.cy) > 5) {
            world.calcSelected();
            selection.changed = true;
        }
    }
    if (inp_mode_view.checked) {
        world.setCursor(e.offsetX - camera_x, e.offsetY - camera_y);
    }
    if (drawing) {
        if (drawing == "pen")
            world.pen(e.offsetX - camera_x, e.offsetY - camera_y);
        else if (drawing == "entity")
            world.entity(e.offsetX - camera_x, e.offsetY - camera_y);
        else if (drawing == "decor")
            world.decor(e.offsetX - camera_x, e.offsetY - camera_y);
    }
    else if (entity_moving) {
        // entity_moving.dx = e.offsetX - entity_moving.x;
        // entity_moving.dy = e.offsetY - entity_moving.y;
        if (ctrl) {
            entity_moving.dx = Math.floor((e.offsetX - entity_moving.x + TileSize / 16 / 2) / (TileSize / 16)) * TileSize / 16;
            entity_moving.dy = Math.floor((e.offsetY - entity_moving.y + TileSize / 16 / 2) / (TileSize / 16)) * TileSize / 16;
        }
        else {
            entity_moving.dx = Math.floor((e.offsetX - entity_moving.x + TileSize / 2) / TileSize) * TileSize;
            entity_moving.dy = Math.floor((e.offsetY - entity_moving.y + TileSize / 2) / TileSize) * TileSize;
        }
        setCursor("move");
    }
    else if (decor_moving) {
        // decor_moving.dx = e.offsetX - decor_moving.x;
        // decor_moving.dy = e.offsetY - decor_moving.y;
        if (ctrl) {
            decor_moving.dx = Math.floor((e.offsetX - decor_moving.x + TileSize / 16 / 2) / (TileSize / 16)) * TileSize / 16;
            decor_moving.dy = Math.floor((e.offsetY - decor_moving.y + TileSize / 16 / 2) / (TileSize / 16)) * TileSize / 16;
        }
        else {
            decor_moving.dx = Math.floor((e.offsetX - decor_moving.x + TileSize / 2) / TileSize) * TileSize;
            decor_moving.dy = Math.floor((e.offsetY - decor_moving.y + TileSize / 2) / TileSize) * TileSize;
        }
        setCursor("move");
    }
    else if (camera_moving) {
        camera_x = camera_moving.cx + e.offsetX - camera_moving.x;
        camera_y = camera_moving.cy + e.offsetY - camera_moving.y;
        setCursor("move");
        normalizeCamera();
    }
    else if (view_moving) {
        view_moving.dx = e.offsetX - view_moving.x;
        view_moving.dy = e.offsetY - view_moving.y;
        setCursor("move");
        normalizeCamera();
    }
});
canvas.addEventListener("mouseup", e => {
    setCursor("none");
    if (inp_mode_view.checked) {
        if (e.button == 0)
            world.mouseup(e.offsetX, e.offsetY);
        world.setCursor(e.offsetX - camera_x, e.offsetY - camera_y);
    }
    if (drawing == "pen")
        world.pen(e.offsetX - camera_x, e.offsetY - camera_y);
    if (drawing == "fill")
        world.fill(e.offsetX - camera_x, e.offsetY - camera_y);
    if (drawing == "entity")
        world.entity(e.offsetX - camera_x, e.offsetY - camera_y);
    if (drawing == "decor")
        world.decor(e.offsetX - camera_x, e.offsetY - camera_y);
    if (entity_moving)
        endEntityMove();
    if (decor_moving)
        endDecorMove();
    if (e.button == 1 && !(selection && selection.changed)) {
        if (inp_mode_entity.checked) {
            const { entity } = world.getEntity(e.offsetX - camera_x, e.offsetY - camera_y);
            if (entity) {
                penEntity = entity.constructor;
                fastPalette.addEntity(penEntity);
            }
        }
        else if (inp_mode_decor.checked) {
            const { decor } = world.getDecor(e.offsetX - camera_x, e.offsetY - camera_y);
            if (decor) {
                penDecor = decor.constructor;
                penDecorData = decor.objData;
                fastPalette.addDecor(penDecor);
            }
        }
        else {
            world.pick(e.offsetX - camera_x, e.offsetY - camera_y);
        }
    }
    if (selection && !selection.changed) {
        selectedDecors = [];
        selectedEntities = [];
    }
    drawing = null;
    camera_moving = null;
    view_moving = null;
    entity_moving = null;
    decor_moving = null;
    selection = null;
});
canvas.addEventListener("mouseleave", () => {
    drawing = null;
    camera_moving = null;
    view_moving = null;
    entity_moving = null;
    setCursor("none");
});
canvas.addEventListener("contextmenu", e => e.preventDefault());
canvas.addEventListener("dblclick", e => {
    if (inp_mode_entity.checked && e.button == 0) {
        const { entity, vx, vy } = world.getEntity(e.offsetX - camera_x, e.offsetY - camera_y);
        if (entity) {
            selectedEntity = entity;
            entity.openMenu(vx, vy);
        }
    }
    if (inp_mode_decor.checked && e.button == 0) {
        const { decor, vx, vy } = world.getDecor(e.offsetX - camera_x, e.offsetY - camera_y);
        if (decor) {
            selectedDecor = decor;
            decor.openMenu(vx, vy);
        }
    }
});
window.addEventListener("keypress", e => {
    if (Popup.Opened)
        return;
    switch (e.code) {
        case "KeyF":
            inp_mode_fill.checked = true;
            break;
        case "KeyR":
            inp_mode_pen.checked = true;
            break;
        case "KeyS":
            inp_mode_view.checked = !inp_mode_view.checked;
            setPalete();
            break;
        case "KeyH":
            inp_highlight_tiles.checked = !inp_highlight_tiles.checked;
            break;
        case "KeyJ":
            inp_highlight_decor.checked = !inp_highlight_decor.checked;
            break;
        case "KeyE": {
            inp_mode_entity.checked = !inp_mode_entity.checked;
            if (inp_mode_entity.checked)
                inp_mode_decor.checked = false;
            setPalete();
            break;
        }
        case "KeyD": {
            inp_mode_decor.checked = !inp_mode_decor.checked;
            if (inp_mode_decor.checked)
                inp_mode_entity.checked = false;
            setPalete();
            break;
        }
        case "KeyW":
            pen.openGroup();
            break;
        // case "KeyC": endEntityMove()?.center(); break;
    }
});
window.addEventListener("keydown", e => {
    if (Popup.Opened)
        return;
    switch (e.code) {
        case "ArrowUp":
            world.up();
            break;
        case "ArrowRight":
            world.right();
            break;
        case "ArrowDown":
            world.down();
            break;
        case "ArrowLeft":
            world.left();
            break;
        case "KeyQ":
            fastPalette.open();
            break;
        case "ControlLeft":
        case "ControlRight":
            ctrl = true;
            break;
    }
});
window.addEventListener("keyup", async (e) => {
    if (Popup.Opened)
        return;
    switch (e.code) {
        case "KeyQ":
            fastPalette.close();
            break;
        case "Delete":
            {
                if (selectedDecor || selectedDecors.length > 0) {
                    function del(decor) {
                        const { view, i } = world.findView(decor);
                        if (!view || i < 0)
                            return;
                        view.decor.splice(i, 1);
                    }
                    if (selectedDecor)
                        del(selectedDecor);
                    selectedDecor = null;
                    for (const decor of selectedDecors) {
                        del(decor);
                    }
                }
                else if (selectedEntity || selectedEntities.length > 0) {
                    function del(entity) {
                        const { view, i } = world.findView(entity);
                        if (!view || i < 0)
                            return;
                        view.entity.splice(i, 1);
                    }
                    if (selectedEntities.length > 0) {
                        let popup = new Popup();
                        popup.focusOn = "cancel";
                        const count = selectedEntities.length + (selectedEntity ? 1 : 0);
                        popup.content.appendChild(Div([], [], `Вы уверены, что хотите удалить этих сущностей (${count}шт)?`));
                        let r = await popup.openAsync();
                        if (!r)
                            return;
                    }
                    else {
                        let popup = new Popup();
                        popup.focusOn = "cancel";
                        popup.content.appendChild(Div([], [], "Вы уверены, что хотите удалить сущность?"));
                        let r = await popup.openAsync();
                        if (!r)
                            return;
                    }
                    if (selectedEntity)
                        del(selectedEntity);
                    selectedEntity = null;
                    for (const entity of selectedEntities) {
                        del(entity);
                    }
                }
            }
            break;
        case "ControlLeft":
        case "ControlRight":
            ctrl = false;
            break;
    }
});
window.addEventListener("mousemove", e => {
    mousePos.x = e.pageX;
    mousePos.y = e.pageY;
});
function loadImages() {
    for (const k in tileIds) {
        const key = k;
        const imgName = tileIds[key];
        tileImages[key] = undefined;
        loadImage(imgName, img => tileImages[key] = img, "tiles");
    }
    loadImage("/icon-move.png", img => icon_move = img);
    loadImage("/icon-trash.png", img => icon_trash = img);
    loadImage("/icon-plus.png", img => icon_plus = img);
    loadImage("/icon-save.png", img => icon_save = img);
    entity.forEach(e => {
        loadImage(e.imgUrl, img => e.img = img, "entities");
    });
    decor.forEach(d => {
        loadImage(d.imgUrl, img => d.img = img, "decor");
    });
}
function centerView(x, y) {
    let width = TileSize * ViewWidth;
    let height = TileSize * ViewHeight;
    const X = Math.floor(x / width);
    const Y = Math.floor(y / height);
    if (X >= world.width || Y >= world.height)
        return;
    TileSize = Math.min(canvas.width / ViewWidth, canvas.height / ViewHeight);
    TileSize = Math.floor(TileSize);
    inp_tilesize.valueAsNumber = TileSize;
    width = TileSize * ViewWidth;
    height = TileSize * ViewHeight;
    camera_x = -X * width + Math.floor((canvas.width - width) / 2);
    camera_y = -Y * height + Math.floor((canvas.height - height) / 2);
    normalizeCamera();
}
function normalizeCamera() {
    const width = world.width * ViewWidth * TileSize;
    const height = world.height * ViewHeight * TileSize;
    if (width > canvas.width) {
        camera_x = Math.max(Math.min(camera_x, 0), -width + canvas.width);
    }
    else
        camera_x = 0;
    if (height > canvas.height) {
        camera_y = Math.max(Math.min(camera_y, 0), -height + canvas.height);
    }
    else
        camera_y = 0;
}
function setCursor(cursor) {
    switch (cursor) {
        case "none":
            canvas.classList.remove("cursor-move");
            canvas.classList.remove("cursor-pointer");
            break;
        case "pointer":
            canvas.classList.remove("cursor-move");
            canvas.classList.add("cursor-pointer");
            break;
        case "move":
            canvas.classList.add("cursor-move");
            canvas.classList.remove("cursor-pointer");
            break;
    }
}
function setPalete() {
    div_palette.innerHTML = "";
    if (inp_mode_view.checked) {
        const _TileSize = TileSize;
        TileSize = 15;
        startViews.forEach((e, i) => {
            const img = document.createElement("canvas");
            img.width = TileSize * ViewWidth;
            img.height = TileSize * ViewHeight;
            const ctx = getCanvasContext(img);
            const data = JSON.parse(startViews[i]);
            const view = View.fromData(data);
            view.drawInd(ctx);
            img.addEventListener("click", () => {
                div_palette.children[startView].classList.remove("palette-view-selected");
                div_palette.children[i].classList.add("palette-view-selected");
                startView = i;
            });
            const delbtn = document.createElement("button");
            delbtn.innerText = "×";
            delbtn.addEventListener("click", async () => {
                if (startViews.length <= 1) {
                    let popup = new Popup();
                    popup.cancelBtn = false;
                    popup.content.appendChild(Div([], [], `Нельзя удалить последний экран`));
                    popup.open();
                    return;
                }
                let popup = new Popup();
                popup.focusOn = "cancel";
                popup.content.appendChild(Div([], [], `Вы уверены, что хотите удалить экран из палитры?`));
                let r = await popup.openAsync();
                if (!r)
                    return;
                popup = new Popup();
                popup.focusOn = "cancel";
                popup.content.appendChild(Div([], [], `Вы точно уверены, что хотите удалить экран из палитры?`));
                popup.reverse = true;
                r = await popup.openAsync();
                if (!r)
                    return;
                startViews.splice(i, 1);
                startView = Math.min(startView, startViews.length - 1);
                localStorage.setItem("WorldEditor-startViews", JSON.stringify(startViews));
                setPalete();
            });
            div_palette.appendChild(Div(["palette-view"], [
                img,
                delbtn
            ]));
        });
        div_palette.children[startView].classList.add("palette-view-selected");
        TileSize = _TileSize;
    }
    else if (inp_mode_entity.checked) {
        const img = document.createElement("img");
        img.title = "Отключить добавление";
        img.src = "./imgs/none.png";
        img.addEventListener("click", () => penEntity = null);
        div_palette.appendChild(img);
        entity.forEach(e => {
            const img = document.createElement("canvas");
            img.title = e.className;
            div_palette.appendChild(img);
            function addImg() {
                if (!inp_mode_entity.checked)
                    return;
                if (e.img) {
                    e.draw(img, 48);
                    img.addEventListener("click", () => {
                        penEntity = e;
                        fastPalette.addEntity(penEntity);
                    });
                }
                else
                    setTimeout(addImg, 100);
            }
            addImg();
        });
    }
    else if (inp_mode_decor.checked) {
        selectedDecor = null;
        penDecorData = null;
        decor.forEach(d => {
            const img = document.createElement("canvas");
            img.title = d.className;
            div_palette.appendChild(img);
            function addImg() {
                if (!inp_mode_decor.checked)
                    return;
                if (d.img) {
                    d.draw(img, 48);
                    img.addEventListener("click", () => {
                        penDecor = d;
                        penDecorData = null;
                        fastPalette.addDecor(penDecor);
                    });
                }
                else
                    setTimeout(addImg, 100);
            }
            addImg();
        });
    }
    else {
        selectedEntity = null;
        for (const k of tileList) {
            const key = k.key;
            function addImg() {
                if (inp_mode_entity.checked)
                    return;
                const img = tileImages[key];
                if (img) {
                    img.title = key;
                    div_palette.appendChild(img);
                    img.addEventListener("click", () => {
                        if (k.group) {
                            pen.openGroup(k);
                        }
                        else {
                            pen.setPen(key);
                        }
                    });
                }
                else
                    setTimeout(addImg, 100);
            }
            addImg();
        }
    }
}
function endEntityMove() {
    function move(entity) {
        if (!entity_moving)
            return;
        entity.x += entity_moving.dx / TileSize;
        entity.y += entity_moving.dy / TileSize;
        entity.x = Math.min(Math.max(entity.x, 0), ViewWidth - entity.getWidth());
        entity.y = Math.min(Math.max(entity.y, 0), ViewHeight - entity.getHeight());
        if (ctrl)
            entity.snapToPixels();
        else
            entity.center();
    }
    if (entity_moving) {
        move(entity_moving.entity);
        for (const entity of selectedEntities) {
            if (entity == entity_moving.entity)
                continue;
            move(entity);
        }
        entity_moving = null;
    }
}
function endDecorMove() {
    function move(decor) {
        if (!decor_moving)
            return;
        decor.x += decor_moving.dx / TileSize;
        decor.y += decor_moving.dy / TileSize;
        decor.x = Math.min(Math.max(decor.x, 0), ViewWidth - decor.getWidth());
        decor.y = Math.min(Math.max(decor.y, 0), ViewHeight - decor.getHeight());
        if (ctrl)
            decor.snapToPixels();
        else
            decor.center();
    }
    if (decor_moving) {
        move(decor_moving.decor);
        for (const decor of selectedDecors) {
            if (decor == decor_moving.decor)
                continue;
            move(decor);
        }
        entity_moving = null;
    }
}
async function askForSure(action) {
    let popup = new Popup();
    popup.focusOn = "cancel";
    popup.content.appendChild(Div([], [], `Вы уверены, что хотите ${action}?`));
    let r = await popup.openAsync();
    if (!r)
        return false;
    popup = new Popup();
    popup.focusOn = "cancel";
    popup.content.appendChild(Div([], [], `Вы точно уверены, что хотите ${action}?`));
    popup.reverse = true;
    r = await popup.openAsync();
    if (!r)
        return false;
    popup = new Popup();
    popup.focusOn = "cancel";
    popup.content.appendChild(Div([], [], `Вы уверены, что хотите ${action}? Все несохранённые данные будут потеряны!`));
    r = await popup.openAsync();
    if (!r)
        return false;
    return true;
}
loadImages();
setPalete();
World.loadFromLocalStorage();
loop();
setInterval(() => world.saveToLocalStarage(), 1000);
// btn_new.click() // Temp
// world.map[0][0] = new View(); // Temp
// penEntity = Entity_Crab; // Temp
// world.map[0][0]?.setEntity(100, 100); // Temp
// inp_mode_entity.checked = !inp_mode_entity.checked; // Temp
// setPalete(); // Temp
function loop() {
    const rect = div_viewport.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.imageSmoothingEnabled = false;
    ctx.save();
    ctx.translate(camera_x, camera_y);
    world.draw();
    ctx.restore();
    if (selection) {
        ctx.save();
        ctx.strokeStyle = "orange";
        ctx.lineWidth = 2;
        ctx.strokeRect(selection.x, selection.y, mousePosCanvas.x - selection.x, mousePosCanvas.y - selection.y);
        ctx.restore();
    }
    ctx.save();
    ctx.strokeStyle = "blue";
    ctx.lineWidth = 2;
    const partX = -camera_x / (world.width * ViewWidth * TileSize - canvas.width);
    const partY = -camera_y / (world.height * ViewHeight * TileSize - canvas.height);
    ctx.beginPath();
    ctx.moveTo(0, canvas.height - 2);
    ctx.lineTo(canvas.width * partX, canvas.height - 2);
    ctx.moveTo(canvas.width - 2, 0);
    ctx.lineTo(canvas.width - 2, canvas.height * partY);
    ctx.stroke();
    ctx.restore();
    minimap.draw();
    requestAnimationFrame(loop);
}
console.log("saveScreenImg(x = 0, y = 0, w?: number)");
console.log('saveWorldImg(w?: number, back: string | null = "lightblue")');
function saveScreenImg(x = 0, y = 0, w) {
    let tileSize = TileSize;
    if (w == undefined) {
        w = 1920;
        tileSize = Math.floor(w / ViewWidth);
    }
    let h = tileSize * ViewHeight;
    const canvas = document.createElement("canvas");
    document.body.appendChild(canvas);
    canvas.width = w;
    canvas.height = h;
    const ctx = getCanvasContext(canvas);
    ctx.imageSmoothingEnabled = false;
    const view = world.map[y][x];
    if (view == undefined) {
        console.log("view == undefined");
        return;
    }
    for (let y = 0; y < ViewHeight; y++) {
        for (let x = 0; x < ViewWidth; x++) {
            let tile = view.tiles[y][x];
            const img = tileImages[tile.id];
            if (!img)
                continue;
            ctx.drawImage(img, x * tileSize, y * tileSize, tileSize, tileSize);
        }
    }
    for (const entity of view.entity) {
        const obj = entity.constructor;
        if (obj.img == undefined)
            continue;
        ctx.drawImage(obj.img, 0, 0, obj.width, obj.height, (entity.x + obj.xImg) * tileSize, (entity.y + obj.yImg) * tileSize, obj.widthImg * tileSize, obj.heightImg * tileSize);
    }
    const hide = inp_highlight_decor.checked;
    const decor = inp_mode_decor.checked;
    const _TileSize = TileSize;
    TileSize = tileSize;
    inp_highlight_decor.checked = false;
    for (const decor of view.decor)
        decor.draw(ctx);
    TileSize = _TileSize;
    inp_highlight_decor.checked = hide;
    inp_mode_decor.checked = decor;
    canvas.addEventListener("click", () => {
        document.body.removeChild(canvas);
    });
    // const img = canvas.toDataURL("image/png");
    // var image = new Image();
    // image.src = img;
    // const W = window.open("");
    // W?.document.write(image.outerHTML);
}
function saveWorldImg(w, back = "lightblue") {
    let tileSize = TileSize;
    let h = 0;
    if (w != undefined) {
        tileSize = Math.floor(w / ViewWidth);
    }
    w = tileSize * ViewWidth * world.width;
    h = tileSize * ViewHeight * world.height;
    const canvas = document.createElement("canvas");
    document.body.appendChild(canvas);
    canvas.width = w;
    canvas.height = h;
    const ctx = getCanvasContext(canvas);
    ctx.imageSmoothingEnabled = false;
    if (back != null) {
        ctx.fillStyle = back;
        ctx.fillRect(0, 0, w, h);
    }
    for (let Y = 0; Y < world.height; Y++) {
        for (let X = 0; X < world.width; X++) {
            const view = world.map[Y][X];
            if (view == undefined)
                continue;
            ctx.translate(X * ViewWidth * tileSize, Y * ViewHeight * tileSize);
            for (let y = 0; y < ViewHeight; y++) {
                for (let x = 0; x < ViewWidth; x++) {
                    let tile = view.tiles[y][x];
                    const img = tileImages[tile.id];
                    if (!img)
                        continue;
                    ctx.drawImage(img, x * tileSize, y * tileSize, tileSize, tileSize);
                }
            }
            for (const entity of view.entity) {
                const obj = entity.constructor;
                if (obj.img == undefined)
                    continue;
                ctx.drawImage(obj.img, 0, 0, obj.width, obj.height, (entity.x + obj.xImg) * tileSize, (entity.y + obj.yImg) * tileSize, obj.widthImg * tileSize, obj.heightImg * tileSize);
            }
            const hide = inp_highlight_decor.checked;
            const decor = inp_mode_decor.checked;
            const _TileSize = TileSize;
            TileSize = tileSize;
            inp_highlight_decor.checked = false;
            for (const decor of view.decor)
                decor.draw(ctx);
            TileSize = _TileSize;
            inp_highlight_decor.checked = hide;
            inp_mode_decor.checked = decor;
            ctx.translate(-X * ViewWidth * tileSize, -Y * ViewHeight * tileSize);
        }
    }
    canvas.addEventListener("click", () => {
        document.body.removeChild(canvas);
    });
    // const img = canvas.toDataURL("image/png");
    // var image = new Image();
    // image.src = img;
    // const W = window.open("");
    // W?.document.write(image.outerHTML);
}
