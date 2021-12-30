class Entity
{
	public x: number;
	public y: number;
	public objData: ObjData = [];
	public static img: HTMLImageElement | undefined;
	public static readonly imgUrl: string = "none.png";
	protected static readonly width: number = 1;
	protected static readonly height: number = 1;
	protected static readonly widthImg: number = 1;
	protected static readonly heightImg: number = 1;
	protected static readonly xImg: number = 0;
	protected static readonly yImg: number = 0;
	protected static readonly widthHitbox: number = 1;
	protected static readonly heightHitbox: number = 1;
	constructor(x: number, y: number)
	{
		this.x = x;
		this.y = y;
		this.center();
	}
	public static draw(canvas: HTMLCanvasElement, size: number)
	{
		if (this.img == undefined) return;
		const coef = size / this.width;
		canvas.width = this.width * coef;
		canvas.height = this.height * coef;
		canvas.style.width = `${canvas.width}px`;
		canvas.style.height = `${canvas.height}px`;
		const ctx = getCanvasContext(canvas);
		ctx.imageSmoothingEnabled = false;
		ctx.drawImage(this.img, 0, 0, this.width, this.height, 0, 0, canvas.width, canvas.height);
	};
	public draw()
	{
		const obj = <EntityObj><any>this.constructor;
		if (obj.img == undefined) return;
		const width = obj.widthImg * TileSize;
		const height = obj.heightImg * TileSize;
		ctx.save();
		if (entity_moving && entity_moving.entity == this) ctx.translate(entity_moving.dx, entity_moving.dy);
		ctx.drawImage(obj.img, 0, 0, obj.width, obj.height, (this.x + obj.xImg) * TileSize, (this.y + obj.yImg) * TileSize, width, height);
		ctx.strokeStyle = "rgba(0, 0, 0, 0.5)";
		ctx.strokeRect(this.x * TileSize, this.y * TileSize, obj.widthHitbox * TileSize, obj.heightHitbox * TileSize);
		ctx.restore();
		if (selectedEntity == this)
		{
			const fontSize = TileSize / 5;
			ctx.save();
			ctx.font = `${fontSize}px Arial`;
			let line = 0;
			const drawLine = (text: string) =>
			{
				ctx.fillText(text, this.x * TileSize + 2, this.y * TileSize + line * fontSize);
				line += 1;
			}
			for (let i = 0; i < this.objData.length; i++)
			{
				const data = this.objData[i];
				if (!data.displayColor) continue;
				ctx.fillStyle = data.displayColor;
				ctx.strokeStyle = data.displayColor;
				ctx.lineWidth = 2;
				if (data.type == "bool" || data.type == "number" || data.type == "text")
				{
					drawLine(`${data.name}: ${data.value}`);
				}
				else if (data.type == "area")
				{
					const rect = <Rect>data.value;
					if (rect == null) continue;
					ctx.strokeRect(rect.x * TileSize, rect.y * TileSize, rect.w * TileSize, rect.h * TileSize);
				}
				else if (data.type == "aura")
				{
					const rect = <Rect>data.value;
					if (rect == null) continue;
					ctx.strokeRect(
						this.x * TileSize + obj.widthHitbox * TileSize / 2 - rect.x * TileSize,
						this.y * TileSize + obj.heightHitbox * TileSize / 2 - rect.y * TileSize,
						rect.w * TileSize, rect.h * TileSize);
				}
				else if (data.type == 'tile')
				{
					const point = <Point>data.value;
					if (point == null) continue;
					ctx.save();
					ctx.globalAlpha = 0.6;
					ctx.fillRect(point.x * TileSize, point.y * TileSize, TileSize, TileSize);
					ctx.restore();
				}
				else if (data.type == 'tiles')
				{
					const points = <Point[]>data.value;
					if (points == null) continue;
					ctx.save();
					ctx.globalAlpha = 0.6;
					for (let j = 0; j < points.length; j++)
					{
						const point = points[j];
						ctx.fillRect(point.x * TileSize, point.y * TileSize, TileSize, TileSize);
					}
					ctx.restore();
				}
			}
			ctx.restore();
		}
	};
	public intersect(x: number, y: number)
	{
		const obj = <EntityObj><any>this.constructor;
		const X = x / TileSize;
		const Y = y / TileSize;
		return X >= this.x && X <= this.x + obj.widthHitbox && Y >= this.y && Y <= this.y + obj.heightHitbox;
	}
	public center()
	{
		const obj = <EntityObj><any>this.constructor;
		this.x = Math.floor(this.x + obj.widthHitbox / 2) + (1 - obj.widthHitbox) / 2;
		this.y = Math.floor(this.y + obj.heightHitbox / 2) + (1 - obj.heightHitbox) / 2;
	}
	public openMenu(vx: number, vy: number)
	{
		new EntityEditor(this, vx, vy).show();
	}
	public getData(): EntitySaveData
	{
		const obj = <EntityObj><any>this.constructor;
		const data: EntitySaveData = {
			className: obj.name,
			x: this.x,
			y: this.y,
		}
		this.objData.forEach(dataEl =>
		{
			data[dataEl.name] = dataEl.value;
		});
		return data;
	}
	public static fromData(data: EntitySaveData)
	{
		const classObj = EntityDict[data.className];
		if (!classObj)
		{
			console.error(`Cant create entity: No such class name "${data.className}"`);
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
interface EntityObj
{
	name: keyof typeof EntityDict,
	imgUrl: string;
	img: HTMLImageElement | undefined;
	readonly width: number;
	readonly height: number;
	readonly widthHitbox: number;
	readonly heightHitbox: number;
	readonly xImg: number;
	readonly yImg: number;
	readonly widthImg: number;
	readonly heightImg: number;
}
interface EntityDataType
{
	"bool": boolean | null,
	"number": number | null,
	"text": string | null,
	"aura": Rect | null,
	"area": Rect | null,
	"tile": Point | null,
	"tiles": Point[] | null,
};
interface Rect
{
	x: number,
	y: number,
	w: number,
	h: number
}
interface Point
{
	x: number,
	y: number,
}
interface EntityData<T extends keyof EntityDataType>
{
	type: T;
	name: string;
	value: EntityDataType[T];
	displayColor?: string,
}
type ObjData = EntityData<keyof EntityDataType>[];

class Entity_Crab extends Entity
{
	public static override img: HTMLImageElement | undefined;
	public static override readonly imgUrl: string = "crab.png";
	protected static override readonly width = 13;
	protected static override readonly height = 11;
	protected static override readonly widthHitbox = 0.8;
	protected static override readonly heightHitbox = 0.677;
	protected static override readonly xImg = 0;
	protected static override readonly yImg = 0;
	protected static override readonly widthImg = 0.8;
	protected static override readonly heightImg = 0.677;
	public override objData: ObjData = [
		{ type: "bool", name: "sleeping", value: true },
		{ type: "number", name: "hp", value: 1, displayColor: "black" },
		{ type: "text", name: "tag", value: null, displayColor: "black" },
		{ type: "aura", name: "atackArea", value: { x: 0.5, y: 0.5, w: 1, h: 1 }, displayColor: "orange" },
		{ type: "area", name: "sleepArea", value: { x: 6, y: 2, w: 5, h: 3 }, displayColor: "azure" },
		{ type: "tile", name: "favoriteTile", value: { x: 1, y: 4 }, displayColor: "pink" },
		{ type: "tiles", name: "killingTiles", value: [{ x: 13, y: 2 }, { x: 13, y: 3 }], displayColor: "tomato" },
	];
}

const EntityDict = {
	"Entity_Crab": Entity_Crab,
}