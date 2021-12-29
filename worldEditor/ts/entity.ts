class Entity
{
	public x: number;
	public y: number;
	protected readonly objData: ObjData = [];
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
	public openMenu()
	{
		new EntityEditor(this.objData).show();
	}
}
interface EntityObj
{
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
interface EntityData<T extends (keyof EntityDataType)>
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
	protected override readonly objData: ObjData = [
		{ type: "bool", name: "sleeping", value: true, displayColor: "black" },
		{ type: "number", name: "hp", value: 1, displayColor: "black" },
		{ type: "text", name: "tag", value: null, displayColor: "black" },
		{ type: "aura", name: "atackArea", value: { x: 0, y: 0, w: 1, h: 1 }, displayColor: "black" },
		{ type: "area", name: "sleepArea", value: null, displayColor: "azure" },
		{ type: "tile", name: "favoriteTile", value: null, displayColor: "pink" },
		{ type: "tiles", name: "killingTiles", value: null, displayColor: "tomato" },
	];
}