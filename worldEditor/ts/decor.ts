class Decor
{
	public x: number;
	public y: number;
	public objData: ObjData = [];
	protected canvas: HTMLCanvasElement | undefined;
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
	public draw(ctx: CanvasRenderingContext2D)
	{
		const obj = <DecorObj><any>this.constructor;
		if (obj.img == undefined) return;
		const selected = selectedDecors.includes(this)
		ctx.save();
		if (decor_moving && (decor_moving.decor == this || selected)) ctx.translate(decor_moving.dx, decor_moving.dy);
		if (this.canvas)
		{
			ctx.drawImage(this.canvas, this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
		}
		else
		{
			ctx.drawImage(obj.img, this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
		}
		if (inp_mode_decor.checked)
		{
			if (selectedDecor == this) ctx.strokeStyle = "rgba(255, 0, 0, 0.5)";
			else ctx.strokeStyle = "rgba(0, 0, 0, 0.5)";
			ctx.strokeRect(this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
			if (selected)
			{
				ctx.strokeStyle = "rgba(255, 0, 0, 1)";
				if (selectedDecor == this) ctx.lineWidth = 4;
				else ctx.lineWidth = 2;
				ctx.strokeRect(this.x * TileSize, this.y * TileSize, obj.width * TileSize, obj.height * TileSize);
			}
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
		this.x = Math.floor(this.x) + (1 - obj.width) / 2;
		this.y = Math.floor(this.y) + (1 - obj.height) / 2;
	}
	public snapToPixels()
	{
		this.x = Math.floor(this.x * 16) / 16;
		this.y = Math.floor(this.y * 16) / 16;
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
		const decor = new classObj(data.x, data.y);
		for (let i = 0; i < decor.objData.length; i++)
		{
			const dataEl = decor.objData[i];
			const value = data[dataEl.name];
			if (value === undefined)
			{
				console.error(`No such field "${dataEl.name}"`, data);
				continue;
			}
			dataEl.value = value;
		}
		decor.afterDataSet();
		return decor;
	}
	public apllyData(data: ObjData)
	{
		for (let i = 0; i < this.objData.length; i++)
		{
			const dataEl = this.objData[i];
			for (let j = 0; j < data.length; j++)
			{
				const el = data[j];
				if (el.name == dataEl.name)
				{
					dataEl.value = JSON.parse(JSON.stringify(el.value));
				}
			}
		}
		this.afterDataSet();
	}
	public afterDataSet()
	{

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