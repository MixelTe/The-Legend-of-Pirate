class Decor
{
	public x: number;
	public y: number;
	public objData: ObjData = [];
	public static readonly className: string = "Decor"
	public static readonly imgUrl: string = "none.png";
	public static width = 1;
	public static height = 1;
	public static img: HTMLImageElement | undefined;
	public getWidth = () => (<DecorObj><any>this.constructor).width;
	public getHeight = () => (<DecorObj><any>this.constructor).height;

	constructor(x: number, y: number)
	{
		this.x = x;
		this.y = y;
	}
	public static draw(canvas: HTMLCanvasElement, size: number)
	{
		if (!this.img) return;
		const coef = size / this.width;
		canvas.width = this.width * coef;
		canvas.height = this.height * coef;
		canvas.style.width = `${canvas.width}px`;
		canvas.style.height = `${canvas.height}px`;
		const ctx = getCanvasContext(canvas);
		ctx.imageSmoothingEnabled = false;
		ctx.drawImage(this.img, 0, 0, canvas.width, canvas.height);
	};
	public draw()
	{
		const obj = <DecorObj><any>this.constructor;
		if (obj.img == undefined) return;
		ctx.save();
		if (decor_moving && decor_moving.decor == this) ctx.translate(decor_moving.dx, decor_moving.dy);
		ctx.drawImage(obj.img, this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
		if (inp_mode_decor.checked)
		{
			ctx.strokeStyle = "rgba(0, 0, 0, 0.5)";
			ctx.strokeRect(this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
		}
		ctx.restore();
	};
	public intersect(x: number, y: number)
	{
		const obj = <DecorObj><any>this.constructor;
		const X = x / TileSize;
		const Y = y / TileSize;
		return X >= this.x && X <= this.x + obj.width && Y >= this.y && Y <= this.y + obj.height;
	}
	public center()
	{
		const obj = <DecorObj><any>this.constructor;
		this.x = Math.floor(this.x + obj.width / 2) + (1 - obj.width) / 2;
		this.y = Math.floor(this.y + obj.height / 2) + (1 - obj.height) / 2;
	}
	public openMenu(vx: number, vy: number)
	{
		new ObjDataEditor(this, vx, vy).show();
	}
	public getData(): DecorSaveData
	{
		const obj = <DecorObj><any>this.constructor;
		const data: DecorSaveData = {
			className: obj.className,
			x: this.x,
			y: this.y,
		}
		this.objData.forEach(dataEl =>
		{
			data[dataEl.name] = dataEl.value;
		});
		return data;
	}
	public static fromData(data: DecorSaveData)
	{
		const classObj = DecorDict[data.className];
		if (!classObj)
		{
			console.error(`Cant create decor: No such class name "${data.className}"`);
			return;
		};
		const entity = new classObj(data.x, data.y);
		for (let i = 0; i < entity.objData.length; i++)
		{
			const dataEl = entity.objData[i];
			const value = data[dataEl.name];
			if (value === undefined)
			{
				console.error(`No such field "${dataEl.name}"`, data);
				dataEl.value = null;
				continue;
			}
			dataEl.value = value;
		}
		return entity;
	}
}

interface DecorObj
{
	className: keyof typeof DecorDict,
	imgUrl: string;
	img: HTMLImageElement | undefined;
	readonly width: number;
	readonly height: number;
}

const DecorDict: { [a: string]: typeof Decor } = {};


function createSimpleDecorClass(name: string, imgUrl: string, width: number, height: number, objData: ObjData)
{
	class Decor_New extends Decor
	{
		public static override readonly imgUrl = imgUrl;
		public static override readonly width = width;
		public static override readonly height = height;
		public static override readonly className = name
		public override objData: ObjData = JSON.parse(JSON.stringify(objData));
	}
	DecorDict[name] = Decor_New;
}
function createSimpleDecorClass_Auto(name: string, folder: string | null, width: number, height: number, objData?: ObjData)
{
	let imgUrl = name + ".png";
	if (folder) imgUrl = folder + "/" + name + ".png";
	createSimpleDecorClass(folder || name, imgUrl, width, height, objData || [])
}