abstract class Entity
{
	public x: number;
	public y: number;
	public static imgUrl: string = "none.png";
	public static img: HTMLImageElement | undefined;
	protected static readonly width: number;
	protected static readonly height: number;
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
		const ctx = getCanvasContext(canvas);
		ctx.imageSmoothingEnabled = false;
		ctx.drawImage(this.img, 0, 0, this.width, this.height, 0, 0, canvas.width, canvas.height);
	};
	public draw()
	{
		if (Entity.img == undefined) return;
		const coef = TileSize / Entity.width;
		const width = Entity.width * coef;
		const height = Entity.height * coef;
		ctx.drawImage(Entity.img, 0, 0, 13, 11, 0, 0, width, height);
	};
}

class Entity_Crab extends Entity
{
	public static override imgUrl: string = "crab.png";
	protected static override readonly width = 13;
	protected static override readonly height = 11;
}