"use strict";
class Decor_TileEdge extends Decor {
    sides = [true, false, false, false];
    corners = [false, false, false, false];
    static imgs = {
        top: null,
        corner: null,
        top_right: null,
        top_right_left: null,
        top_right_left_bottom: null,
    };
    canvas = document.createElement("canvas");
    ctx = getCanvasContext(this.canvas);
    static imgUrl = "/none.png";
    objData = [
        { name: "sides", type: "any", value: this.sides },
        { name: "corners", type: "any", value: this.corners },
    ];
    constructor(x, y) {
        super(x, y);
        this.canvas.width = 16;
        this.canvas.height = 16;
        this.redraw();
    }
    afterDataSet() {
        this.sides = this.objData[0].value;
        this.corners = this.objData[1].value;
        this.redraw();
    }
    openMenu(vx, vy) {
        const sidesCopy = [this.sides[0], this.sides[1], this.sides[2], this.sides[3]];
        const cornesCopy = [this.corners[0], this.corners[1], this.corners[2], this.corners[3]];
        const inp_top = Input([], "checkbox");
        const inp_right = Input([], "checkbox");
        const inp_bottom = Input([], "checkbox");
        const inp_left = Input([], "checkbox");
        const inp_topR = Input([], "checkbox");
        const inp_bottomR = Input([], "checkbox");
        const inp_bottomL = Input([], "checkbox");
        const inp_topL = Input([], "checkbox");
        const canvas = document.createElement("canvas");
        canvas.width = 64;
        canvas.height = 64;
        const ctx = getCanvasContext(canvas);
        const popup = new Popup();
        popup.title = "Редактирование декорации";
        popup.content.appendChild(Div(["TileEdge-picker"], [Table([], [
                TR([], [
                    TD([], [inp_topL]),
                    TD([], [inp_top]),
                    TD([], [inp_topR]),
                ]),
                TR([], [
                    TD([], [inp_left]),
                    TD([], [canvas]),
                    TD([], [inp_right]),
                ]),
                TR([], [
                    TD([], [inp_bottomL]),
                    TD([], [inp_bottom]),
                    TD([], [inp_bottomR]),
                ])
            ])]));
        popup.content.appendChild(Div([], [
            Span([], [], "Удалить декорацию"),
            Button("delete-button", "Удалить", async () => {
                const popup_confirm = new Popup();
                popup_confirm.focusOn = "cancel";
                popup_confirm.content.appendChild(Div([], [], "Вы уверены, что хотите удалить декорацию?"));
                let r = await popup_confirm.openAsync();
                if (!r)
                    return;
                const view = world.map[vy][vx];
                if (!view)
                    return;
                const i = view.decor.indexOf(this);
                if (i >= 0) {
                    view.decor.splice(i, 1);
                    popup.close(true);
                }
            }),
        ]));
        inp_top.checked = this.sides[0];
        inp_right.checked = this.sides[1];
        inp_bottom.checked = this.sides[2];
        inp_left.checked = this.sides[3];
        inp_topR.checked = this.corners[0];
        inp_bottomR.checked = this.corners[1];
        inp_bottomL.checked = this.corners[2];
        inp_topL.checked = this.corners[3];
        inp_top.addEventListener("change", () => { this.sides[0] = inp_top.checked; redraw(); });
        inp_right.addEventListener("change", () => { this.sides[1] = inp_right.checked; redraw(); });
        inp_bottom.addEventListener("change", () => { this.sides[2] = inp_bottom.checked; redraw(); });
        inp_left.addEventListener("change", () => { this.sides[3] = inp_left.checked; redraw(); });
        inp_topR.addEventListener("change", () => { this.corners[0] = inp_topR.checked; redraw(); });
        inp_bottomR.addEventListener("change", () => { this.corners[1] = inp_bottomR.checked; redraw(); });
        inp_bottomL.addEventListener("change", () => { this.corners[2] = inp_bottomL.checked; redraw(); });
        inp_topL.addEventListener("change", () => { this.corners[3] = inp_topL.checked; redraw(); });
        const redraw = () => {
            this.redraw();
            ctx.imageSmoothingEnabled = false;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(this.canvas, 0, 0, canvas.width, canvas.height);
        };
        redraw();
        popup.addListener("cancel", () => {
            this.sides = sidesCopy;
            this.corners = cornesCopy;
        });
        popup.addListener("close", () => {
            this.objData[0].value = this.sides;
            this.objData[1].value = this.corners;
            for (const decor of selectedDecors) {
                if (decor.constructor == this.constructor) {
                    decor.apllyData(this.objData);
                }
            }
        });
        popup.open();
    }
    redraw() {
        const obj = this.constructor;
        if (!(obj.imgs.top && obj.imgs.corner && obj.imgs.top_right && obj.imgs.top_right_left && obj.imgs.top_right_left_bottom)) {
            setTimeout(() => this.redraw(), 200);
            return;
        }
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.save();
        if (this.corners[0]) {
            this.ctx.drawImage(obj.imgs.corner, 0, 0);
        }
        if (this.corners[1]) {
            this.ctx.save();
            this.ctx.translate(16, 0);
            this.ctx.rotate(Math.PI / 2);
            this.ctx.drawImage(obj.imgs.corner, 0, 0);
            this.ctx.restore();
        }
        if (this.corners[2]) {
            this.ctx.save();
            this.ctx.translate(16, 16);
            this.ctx.rotate(Math.PI);
            this.ctx.drawImage(obj.imgs.corner, 0, 0);
            this.ctx.restore();
        }
        if (this.corners[3]) {
            this.ctx.save();
            this.ctx.translate(0, 16);
            this.ctx.rotate(Math.PI / 2 * 3);
            this.ctx.drawImage(obj.imgs.corner, 0, 0);
            this.ctx.restore();
        }
        if (this.sidesIs([true, false, false, false])) {
            this.ctx.drawImage(obj.imgs.top, 0, 0);
        }
        else if (this.sidesIs([false, true, false, false])) {
            this.ctx.translate(16, 0);
            this.ctx.rotate(Math.PI / 2);
            this.ctx.drawImage(obj.imgs.top, 0, 0);
        }
        else if (this.sidesIs([false, false, true, false])) {
            this.ctx.translate(16, 16);
            this.ctx.rotate(Math.PI);
            this.ctx.drawImage(obj.imgs.top, 0, 0);
        }
        else if (this.sidesIs([false, false, false, true])) {
            this.ctx.translate(0, 16);
            this.ctx.rotate(Math.PI / 2 * 3);
            this.ctx.drawImage(obj.imgs.top, 0, 0);
        }
        else if (this.sidesIs([true, true, false, false])) {
            this.ctx.drawImage(obj.imgs.top_right, 0, 0);
        }
        else if (this.sidesIs([false, true, true, false])) {
            this.ctx.translate(16, 0);
            this.ctx.rotate(Math.PI / 2);
            this.ctx.drawImage(obj.imgs.top_right, 0, 0);
        }
        else if (this.sidesIs([false, false, true, true])) {
            this.ctx.translate(16, 16);
            this.ctx.rotate(Math.PI);
            this.ctx.drawImage(obj.imgs.top_right, 0, 0);
        }
        else if (this.sidesIs([true, false, false, true])) {
            this.ctx.translate(0, 16);
            this.ctx.rotate(Math.PI / 2 * 3);
            this.ctx.drawImage(obj.imgs.top_right, 0, 0);
        }
        else if (this.sidesIs([true, true, false, true])) {
            this.ctx.drawImage(obj.imgs.top_right_left, 0, 0);
        }
        else if (this.sidesIs([true, true, true, false])) {
            this.ctx.translate(16, 0);
            this.ctx.rotate(Math.PI / 2);
            this.ctx.drawImage(obj.imgs.top_right_left, 0, 0);
        }
        else if (this.sidesIs([false, true, true, true])) {
            this.ctx.translate(16, 16);
            this.ctx.rotate(Math.PI);
            this.ctx.drawImage(obj.imgs.top_right_left, 0, 0);
        }
        else if (this.sidesIs([true, false, true, true])) {
            this.ctx.translate(0, 16);
            this.ctx.rotate(Math.PI / 2 * 3);
            this.ctx.drawImage(obj.imgs.top_right_left, 0, 0);
        }
        else if (this.sidesIs([true, true, true, true])) {
            this.ctx.drawImage(obj.imgs.top_right_left_bottom, 0, 0);
        }
        else if (this.sidesIs([true, false, true, false])) {
            this.ctx.drawImage(obj.imgs.top, 0, 0);
            this.ctx.translate(16, 16);
            this.ctx.rotate(Math.PI);
            this.ctx.drawImage(obj.imgs.top, 0, 0);
        }
        else if (this.sidesIs([false, true, false, true])) {
            this.ctx.translate(16, 0);
            this.ctx.rotate(Math.PI / 2);
            this.ctx.drawImage(obj.imgs.top, 0, 0);
            this.ctx.translate(16, 16);
            this.ctx.rotate(Math.PI);
            this.ctx.drawImage(obj.imgs.top, 0, 0);
        }
        this.ctx.restore();
    }
    sidesIs(sides) {
        return this.sides[0] == sides[0] &&
            this.sides[1] == sides[1] &&
            this.sides[2] == sides[2] &&
            this.sides[3] == sides[3];
    }
    static createTileEdge(name) {
        class Decor_TileEdge_New extends Decor_TileEdge {
            static className = name;
            static imgUrl = `/${name}.png`;
            static imgs = {
                top: null,
                corner: null,
                top_right: null,
                top_right_left: null,
                top_right_left_bottom: null,
            };
            static loadImgs() {
                loadImage("top.png", img => this.imgs.top = img, "decor/" + name);
                loadImage("corner.png", img => this.imgs.corner = img, "decor/" + name);
                loadImage("top_right.png", img => this.imgs.top_right = img, "decor/" + name);
                loadImage("top_right_left.png", img => this.imgs.top_right_left = img, "decor/" + name);
                loadImage("top_right_left_bottom.png", img => this.imgs.top_right_left_bottom = img, "decor/" + name);
            }
        }
        Decor_TileEdge_New.loadImgs();
        DecorDict[name] = Decor_TileEdge_New;
    }
}
createSimpleDecorClass_Auto("snail", null, 0.375, 0.375);
Decor_TileEdge.createTileEdge("tileEdge_water");
Decor_TileEdge.createTileEdge("tileEdge_water_deep");
Decor_TileEdge.createTileEdge("tileEdge_sand");
