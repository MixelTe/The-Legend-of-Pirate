abstract class Entity
{
	public imgUrl: string = "none.png";
	public img: HTMLImageElement | undefined;
	public abstract draw(ctx: CanvasRenderingContext2D, size: number): void;
	public abstract drawCanvas(canvas: HTMLCanvasElement, size: number): void;
}

class Entity_Crab extends Entity
{
	public override imgUrl: string = "crab.png";
	private readonly width = 13;
	private readonly height = 11;
	public draw(ctx: CanvasRenderingContext2D, size: number)
	{
		if (this.img == undefined) return;
		const coef = this.img.height / this.img.width;
		ctx.drawImage(this.img, 0, 0, 13, 11, 0, 0, size, size * coef);
	};
	public drawCanvas(canvas: HTMLCanvasElement, size: number)
	{
		if (this.img == undefined) return;
		const coef = size / this.width;
		canvas.width = this.width * coef;
		canvas.height = this.height * coef;
		const ctx = getCanvasContext(canvas);
		ctx.imageSmoothingEnabled = false;
		ctx.drawImage(this.img, 0, 0, this.width, this.height, 0, 0, canvas.width, canvas.height);
	};
}