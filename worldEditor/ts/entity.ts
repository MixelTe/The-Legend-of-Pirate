class Entity
{
	public x: number;
	public y: number;
	public objData: ObjData = [];
	public static img: HTMLImageElement | undefined;
	public static readonly imgUrl: string = "/none.png";
	public static readonly className: string = "Entity"
	protected static readonly width: number = 1;
	protected static readonly height: number = 1;
	protected static readonly widthImg: number = 1;
	protected static readonly heightImg: number = 1;
	protected static readonly xImg: number = 0;
	protected static readonly yImg: number = 0;
	protected static readonly widthHitbox: number = 1;
	protected static readonly heightHitbox: number = 1;
	public getWidth = () => (<EntityObj><any>this.constructor).widthHitbox;
	public getHeight = () => (<EntityObj><any>this.constructor).heightHitbox;

	public static customDraw = (self: Entity, ctx: CanvasRenderingContext2D) => {};
	constructor(x: number, y: number)
	{
		this.x = x;
		this.y = y;
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
	public draw(ctx: CanvasRenderingContext2D)
	{
		const obj = <EntityObj><any>this.constructor;
		if (obj.img == undefined) return;
		if (selectedEntity == this)
		{
			const fontSize = TileSize / 5;
			ctx.save();
			ctx.font = `${fontSize}px Arial`;
			let line = 0;
			const drawLine = (text: string) =>
			{
				ctx.fillText(text, this.x * TileSize + 2, this.y * TileSize + line * fontSize);
				line -= 1;
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
					ctx.strokeRect(rect[0] * TileSize, rect[1] * TileSize, rect[2] * TileSize, rect[3] * TileSize);
				}
				else if (data.type == "aura")
				{
					const rect = <Rect>data.value;
					if (rect == null) continue;
					ctx.strokeRect(
						this.x * TileSize + obj.widthHitbox * TileSize / 2 - rect[0] * TileSize,
						this.y * TileSize + obj.heightHitbox * TileSize / 2 - rect[1] * TileSize,
						rect[2] * TileSize, rect[3] * TileSize);
				}
				else if (data.type == 'tile')
				{
					const point = <Point>data.value;
					if (point == null) continue;
					ctx.save();
					ctx.globalAlpha = 0.6;
					ctx.fillRect(point[0] * TileSize, point[1] * TileSize, TileSize, TileSize);
					ctx.restore();
				}
				else if (data.type == 'tiles' || data.type == 'tilesNumered')
				{
					const points = <Point[]>data.value;
					if (points == null) continue;
					ctx.save();
					ctx.globalAlpha = 0.6;
					for (let j = 0; j < points.length; j++)
					{
						const point = points[j];
						ctx.fillRect(point[0] * TileSize, point[1] * TileSize, TileSize, TileSize);
						if (data.type == 'tilesNumered')
						{
							ctx.save();
							ctx.fillStyle = "rgb(255, 0, 255)";
							ctx.font = `${TileSize}px Aria`
							ctx.fillText(`${j}`, point[0] * TileSize + TileSize * 0.2, point[1] * TileSize + TileSize * 0.8);
							ctx.restore();
						}
					}
					ctx.restore();
				}
			}
			ctx.restore();
		}
		const width = obj.widthImg * TileSize;
		const height = obj.heightImg * TileSize;
		const selected = selectedEntities.includes(this);
		ctx.save();
		if (entity_moving && (entity_moving.entity == this || selected)) ctx.translate(entity_moving.dx, entity_moving.dy);
		ctx.drawImage(obj.img, 0, 0, obj.width, obj.height, (this.x + obj.xImg) * TileSize, (this.y + obj.yImg) * TileSize, width, height);
		if (inp_mode_entity.checked)
		{
			if (selectedEntity == this) ctx.strokeStyle = "rgba(255, 0, 0, 0.5)";
			else ctx.strokeStyle = "rgba(0, 0, 0, 0.5)";
			ctx.strokeRect(this.x * TileSize, this.y * TileSize, obj.widthHitbox * TileSize, obj.heightHitbox * TileSize);
			if (selected)
			{
				ctx.strokeStyle = "rgba(255, 0, 0, 1)";
				if (selectedEntity == this) ctx.lineWidth = 4;
				else ctx.lineWidth = 2;
				ctx.strokeRect(this.x * TileSize - 2, this.y * TileSize - 2, obj.widthHitbox * TileSize + 4, obj.heightHitbox * TileSize + 4);
			}
		}
		ctx.restore();
		obj.customDraw(this, ctx);
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
	public snapToPixels()
	{
		this.x = Math.floor(this.x * 16) / 16;
		this.y = Math.floor(this.y * 16) / 16;
	}
	public openMenu(vx: number, vy: number)
	{
		new ObjDataEditor(this, vx, vy).show();
	}
	public getData(): EntitySaveData
	{
		const obj = <EntityObj><any>this.constructor;
		const data: EntitySaveData = {
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
				continue;
			}
			dataEl.value = value;
		}
		return entity;
	}
}
interface EntityObj
{
	className: keyof typeof EntityDict,
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
	customDraw: (self: Entity, ctx: CanvasRenderingContext2D) => {};
}
interface EntityDataType
{
	"bool": boolean | null,
	"number": number | null,
	"text": string | null,
	"textAria": string | null,
	"aura": Rect | null,
	"area": Rect | null,
	"tile": Point | null,
	"tiles": Point[] | null,
	"tilesNumered": Point[] | null,
	"coords": Point | null,
	"any": any | null,
};
type Rect = [number, number, number, number]
type Point = [number, number]
interface EntityData<T extends keyof EntityDataType>
{
	type: T;
	name: string;
	value: EntityDataType[T];
	displayColor?: string,
	options?: EntityDataType[T][],
	optionsHint?: string[],
	nullable?: boolean,
	title?: string,
	smartTitle?: SmartTitle,
	header?: string,
}
interface SmartTitle
{
	field: string,
	titles: {
		[_: string]: string,
	}
}
type ObjData = EntityData<keyof EntityDataType>[];


const EntityDict: { [a: string]: typeof Entity } = {};

function createNewEntityClass(name: string, imgUrl: string, width: number, height: number, widthHitbox: number, heightHitbox: number,
	xImg: number, yImg: number, widthImg: number, heightImg: number, objData: ObjData)
{
	class Entity_New extends Entity
	{
		public static override readonly imgUrl = imgUrl;
		protected static override readonly width = width;
		protected static override readonly height = height;
		protected static override readonly widthHitbox = widthHitbox;
		protected static override readonly heightHitbox = heightHitbox;
		protected static override readonly xImg = xImg;
		protected static override readonly yImg = yImg;
		protected static override readonly widthImg = widthImg;
		protected static override readonly heightImg = heightImg;
		public static override readonly className = name
		public override objData: ObjData = JSON.parse(JSON.stringify(objData));
	}
	EntityDict[name] = Entity_New;
	return Entity_New;
}
function createNewEntityClass_Auto(name: string, hasFolder: boolean | null, width: number, height: number, widthHitbox: number, heightHitbox: number, xImg?: number, yImg?: number, widthImg?: number, heightImg?: number, objData?: ObjData)
{
	let imgUrl = name + ".png"
	if (hasFolder == null) imgUrl = "/" + name + ".png"
	if (hasFolder) imgUrl = name + "/stay.png"
	return createNewEntityClass(name, imgUrl, width, height, widthHitbox, heightHitbox, xImg || 0, yImg || 0, widthImg || widthHitbox, heightImg || heightHitbox, objData || [])
}