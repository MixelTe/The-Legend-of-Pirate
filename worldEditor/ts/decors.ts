class Decor_TileEdge extends Decor
{
	private sides = [true, false, false, false];
	protected static readonly imgs = {
		top: <null | HTMLImageElement>null,
		top_right: <null | HTMLImageElement>null,
		top_right_left: <null | HTMLImageElement>null,
		top_right_left_bottom: <null | HTMLImageElement>null,
	};
	protected override canvas = document.createElement("canvas");
	private ctx = getCanvasContext(this.canvas);
	public static override readonly imgUrl: string = "/none.png";
	public override objData: ObjData = [
		{ name: "sides", type: "any", value: this.sides, }
	];
	constructor(x: number, y: number)
	{
		super(x, y);
		this.canvas.width = 16;
		this.canvas.height = 16;
		this.redraw();
	}
	protected override afterDataSet()
	{
		this.sides = this.objData[0].value;
		this.redraw();
	}
	public override openMenu(vx: number, vy: number)
	{
		const sidesCopy = [this.sides[0], this.sides[1], this.sides[2], this.sides[3]];
		const inp_top = Input([], "checkbox");
		const inp_right = Input([], "checkbox");
		const inp_bottom = Input([], "checkbox");
		const inp_left = Input([], "checkbox");
		const canvas = document.createElement("canvas");
		canvas.width = 64;
		canvas.height = 64;
		const ctx = getCanvasContext(canvas);
		const popup = new Popup();
		popup.title = "Редактирование декорации";
		popup.content.appendChild(Div(["TileEdge-picker"], [Table([], [
			TR([], [
				TD([], []),
				TD([], [inp_top]),
				TD([], []),
			]),
			TR([], [
				TD([], [inp_left]),
				TD([], [canvas]),
				TD([], [inp_right]),
			]),
			TR([], [
				TD([], []),
				TD([], [inp_bottom]),
				TD([], []),
			])
		])]));
		popup.content.appendChild(Div([], [
			Span([], [], "Удалить декорацию"),
			Button("delete-button", "Удалить", async () =>
			{
				const popup_confirm = new Popup();
				popup_confirm.focusOn = "cancel";
				popup_confirm.content.appendChild(Div([], [], "Вы уверены, что хотите удалить декорацию?"));
				let r = await popup_confirm.openAsync();
				if (!r) return
				const view = world.map[vy][vx];
				if (!view) return;
				const i = view.decor.indexOf(this);
				if (i >= 0)
				{
					view.decor.splice(i, 1);
					popup.close(true);
				}
			}),
		]));
		inp_top.checked = this.sides[0];
		inp_right.checked = this.sides[1];
		inp_bottom.checked = this.sides[2];
		inp_left.checked = this.sides[3];
		inp_top.addEventListener("change", () => {this.sides[0] = inp_top.checked; redraw();});
		inp_right.addEventListener("change", () => {this.sides[1] = inp_right.checked; redraw();});
		inp_bottom.addEventListener("change", () => {this.sides[2] = inp_bottom.checked; redraw();});
		inp_left.addEventListener("change", () => {this.sides[3] = inp_left.checked; redraw();});
		const redraw = () =>
		{
			this.redraw();
			ctx.imageSmoothingEnabled = false;
			ctx.clearRect(0, 0, canvas.width, canvas.height)
			ctx.drawImage(this.canvas, 0, 0, canvas.width, canvas.height);
		}
		redraw();
		popup.addListener("cancel", () => this.sides = sidesCopy);
		popup.addListener("close", () => this.objData[0].value = this.sides);
		popup.open();
	}
	public redraw()
	{
		const obj = <Decor_TileEdgeObj><any>this.constructor;
		if (!(obj.imgs.top && obj.imgs.top_bottom && obj.imgs.top_right && obj.imgs.top_right_left && obj.imgs.top_right_left_bottom))
		{
			setTimeout(() => this.redraw(), 200);
			return;
		}
		this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
		this.ctx.save();
		if (this.sidesIs([true, false, false, false]))
		{
			this.ctx.drawImage(obj.imgs.top, 0, 0);
		}
		else if (this.sidesIs([false, true, false, false]))
		{
			this.ctx.translate(16, 0)
			this.ctx.rotate(Math.PI / 2);
			this.ctx.drawImage(obj.imgs.top, 0, 0);
		}
		else if (this.sidesIs([false, false, true, false]))
		{
			this.ctx.translate(16, 16)
			this.ctx.rotate(Math.PI);
			this.ctx.drawImage(obj.imgs.top, 0, 0);
		}
		else if (this.sidesIs([false, false, false, true]))
		{
			this.ctx.translate(0, 16)
			this.ctx.rotate(Math.PI / 2 * 3);
			this.ctx.drawImage(obj.imgs.top, 0, 0);
		}
		else if (this.sidesIs([true, true, false, false]))
		{
			this.ctx.drawImage(obj.imgs.top_right, 0, 0);
		}
		else if (this.sidesIs([false, true, true, false]))
		{
			this.ctx.translate(16, 0)
			this.ctx.rotate(Math.PI / 2);
			this.ctx.drawImage(obj.imgs.top_right, 0, 0);
		}
		else if (this.sidesIs([false, false, true, true]))
		{
			this.ctx.translate(16, 16)
			this.ctx.rotate(Math.PI);
			this.ctx.drawImage(obj.imgs.top_right, 0, 0);
		}
		else if (this.sidesIs([true, false, false, true]))
		{
			this.ctx.translate(0, 16)
			this.ctx.rotate(Math.PI / 2 * 3);
			this.ctx.drawImage(obj.imgs.top_right, 0, 0);
		}
		else if (this.sidesIs([true, true, false, true]))
		{
			this.ctx.drawImage(obj.imgs.top_right_left, 0, 0);
		}
		else if (this.sidesIs([true, true, true, false]))
		{
			this.ctx.translate(16, 0)
			this.ctx.rotate(Math.PI / 2);
			this.ctx.drawImage(obj.imgs.top_right_left, 0, 0);
		}
		else if (this.sidesIs([false, true, true, true]))
		{
			this.ctx.translate(16, 16)
			this.ctx.rotate(Math.PI);
			this.ctx.drawImage(obj.imgs.top_right_left, 0, 0);
		}
		else if (this.sidesIs([true, false, true, true]))
		{
			this.ctx.translate(0, 16)
			this.ctx.rotate(Math.PI / 2 * 3);
			this.ctx.drawImage(obj.imgs.top_right_left, 0, 0);
		}
		else if (this.sidesIs([true, true, true, true]))
		{
			this.ctx.drawImage(obj.imgs.top_right_left_bottom, 0, 0);
		}
		else if (this.sidesIs([true, false, true, false]))
		{
			this.ctx.drawImage(obj.imgs.top_bottom, 0, 0);
		}
		else if (this.sidesIs([false, true, false, true]))
		{
			this.ctx.translate(16, 0)
			this.ctx.rotate(Math.PI / 2);
			this.ctx.drawImage(obj.imgs.top_bottom, 0, 0);
		}
		this.ctx.restore();
	}
	private sidesIs(sides: boolean[])
	{
		return this.sides[0] == sides[0] &&
			this.sides[1] == sides[1] &&
			this.sides[2] == sides[2] &&
			this.sides[3] == sides[3];
	}

	public static createTileEdge(name: string)
	{
		class Decor_TileEdge_New extends Decor_TileEdge
		{
			public static override readonly className = name;
			public static override readonly imgUrl: string = `/${name}.png`;
			protected static override readonly imgs = {
				top: <null | HTMLImageElement>null,
				top_bottom: <HTMLImageElement | null>null,
				top_right: <null | HTMLImageElement>null,
				top_right_left: <null | HTMLImageElement>null,
				top_right_left_bottom: <null | HTMLImageElement>null,
			};
			public static loadImgs()
			{
				loadImage("top.png", img => this.imgs.top = img, "decor/" + name);
				loadImage("top_bottom.png", img => this.imgs.top_bottom = img, "decor/" + name);
				loadImage("top_right.png", img => this.imgs.top_right = img, "decor/" + name);
				loadImage("top_right_left.png", img => this.imgs.top_right_left = img, "decor/" + name);
				loadImage("top_right_left_bottom.png", img => this.imgs.top_right_left_bottom = img, "decor/" + name);
			}
		}
		Decor_TileEdge_New.loadImgs();
		DecorDict[name] = Decor_TileEdge_New;
	}
}
interface Decor_TileEdgeObj extends DecorObj
{
	imgs: {
		top: HTMLImageElement | null;
		top_bottom: HTMLImageElement | null;
		top_right: HTMLImageElement | null;
		top_right_left: HTMLImageElement | null;
		top_right_left_bottom: HTMLImageElement | null;
	}
}


createSimpleDecorClass_Auto("snail", null, 0.375, 0.375)
Decor_TileEdge.createTileEdge("tileEdge_water")
Decor_TileEdge.createTileEdge("tileEdge_water_deep")
Decor_TileEdge.createTileEdge("tileEdge_sand")