const inp_width = getInput("inp-width")
const inp_height = getInput("inp-height")
const inp_tilesize = getInput("inp-tilesize")
const btn_up = getButton("btn-up")
const btn_right = getButton("btn-right")
const btn_down = getButton("btn-down")
const btn_left = getButton("btn-left")
const btn_save = getButton("btn-save")
const btn_load = getButton("btn-load")
const btn_new = getButton("btn-new")
const inp_cameraSpeed = getInput("inp_cameraSpeed");
const world_map = getTable("world-map")
const div_viewport = getDiv("viewport")
const canvas = getCanvas("canvas");
const ctx = getCanvasContext(canvas);

const ViewWidth = 15;
const ViewHeight = 7;
let TileSize = 16 * 2;
const tileIds = {
	none: "none.png",
	ice: "ice.png",
	sand: "sand.png",
	wall: "wall.png",
}
const tileImages: TileImages = {};

inp_tilesize.valueAsNumber = TileSize;
let camera_x = 0;
let camera_y = 0;
let camera_speed = () =>
{
	return Math.round(TileSize * inp_cameraSpeed.valueAsNumber / 2);
};


class World
{
	map: (View | undefined)[][] = [];
	width: number;
	height: number;
	constructor(width: number, height: number, world?: World)
	{
		this.width = width;
		this.height = height;
		this.map = []
		if (world)
		{
			if (world.width > width)
			{
				for (let y = 0; y < world.height; y++)
				{
					for (let x = width; x < world.width; x++)
					{
						if (world.map[y][x])
						{
							const popup = new Popup();
							popup.content.appendChild(Div([], [], "Уменьшение мира нельзя провести без потерь!"));
							popup.open();
							this.width = world.width
							this.height = world.height
							this.map = world.map
							return
						}
					}
				}
			}
			if (world.height > height)
			{
				for (let y = height; y < world.height; y++)
				{
					for (let x = 0; x < world.width; x++)
					{
						if (world.map[y][x])
						{
							const popup = new Popup();
							popup.content.appendChild(Div([], [], "Уменьшение мира нельзя провести без потерь!"));
							popup.open();
							this.width = world.width
							this.height = world.height
							this.map = world.map
							return
						}
					}
				}
			}
			for (let y = 0; y < height; y++)
			{
				const line = []
				for (let x = 0; x < width; x++)
				{
					if (y < world.height && x < world.width)
					{
						line.push(world.map[y][x])
					}
					else
					{
						line.push(undefined)
					}
				}
				this.map.push(line)
			}
		}
		else
		{
			for (let y = 0; y < height; y++)
			{
				const line = []
				for (let x = 0; x < width; x++)
				{
					line.push(undefined)
				}
				this.map.push(line)
			}
		}
		if (this.map[0]) this.map[0][0] = new View();
		this.createTable();
	}
	public up()
	{
		if (this.height == 0) return;
		const line = this.map.splice(0, 1)
		this.map.push(line[0])
		this.createTable();
	}
	public right()
	{
		if (this.width == 0) return;
		for (let y = 0; y < this.height; y++)
		{
			this.map[y].unshift(this.map[y].pop())
		}
		this.createTable();
	}
	public down()
	{
		if (this.height == 0) return;
		const line = this.map.splice(this.height - 1, 1)
		this.map.unshift(line[0])
		this.createTable();
	}
	public left()
	{
		if (this.width == 0) return;
		for (let y = 0; y < this.height; y++)
		{
			this.map[y].push(this.map[y].shift())
		}
		this.createTable();
	}
	private createTable()
	{
		world_map.innerHTML = "";
		for (let y = 0; y < this.height; y++)
		{
			const row = document.createElement("tr")
			world_map.appendChild(row);
			for (let x = 0; x < this.width; x++)
			{
				const cell = document.createElement("td");
				row.appendChild(cell);
				const btn = document.createElement("button");
				if (this.map[y][x]) btn.classList.add("active");
				cell.appendChild(btn);
				btn.addEventListener("click", async () =>
				{
					if (this.map[y][x])
					{
						const popup = new Popup();
						popup.content.appendChild(Div([], [], "Вы уверены, что хотите удалить экран?"));
						const r = await popup.openAsync();
						if (r)
						{
							const popup = new Popup();
							popup.content.appendChild(Div([], [], "Вы точно уверены, что хотите удалить экран?"));
							popup.reverse = true;
							const r = await popup.openAsync();
							if (!r) return;
						}
						if (!r) return;
						this.map[y][x] = undefined
						btn.classList.remove("active")
					}
					else
					{
						this.map[y][x] = new View()
						btn.classList.add("active")
					}
				});
			}
		}
	}

	public draw()
	{
		const viewWidth = ViewWidth * TileSize;
		const viewHeight = ViewHeight * TileSize;
		for (let y = 0; y < this.height; y++)
		{
			for (let x = 0; x < this.width; x++)
			{
				let view = this.map[y][x];
				if (view)
				{
					ctx.save();
					ctx.translate(x * viewWidth, y * viewHeight);
					view.draw();
					ctx.restore();
				}
				else
				{
					ctx.save();
					ctx.fillStyle = "lightblue";
					ctx.translate(x * viewWidth, y * viewHeight);
					ctx.fillRect(0, 0, viewWidth, viewHeight);
					ctx.restore();
				}
			}
		}
	}
}
class View
{
	tiles: Tile[][] = [];
	constructor()
	{
		for (let y = 0; y < ViewHeight; y++)
		{
			const line = []
			for (let x = 0; x < ViewWidth; x++)
			{
				if (x == 0 || x == ViewWidth - 1 || y == 0 || y == ViewHeight - 1)
				{
					line.push(new Tile("wall"))
				}
				else
				{
					line.push(new Tile())
				}
			}
			this.tiles.push(line)
		}
	}
	public draw()
	{
		for (let y = 0; y < ViewHeight; y++)
		{
			for (let x = 0; x < ViewWidth; x++)
			{
				let view = this.tiles[y][x];
				if (view)
				{
					ctx.save();
					ctx.translate(x * TileSize, y * TileSize);
					view.draw();
					ctx.restore();
				}
			}
		}
		ctx.strokeStyle = "black";
		ctx.lineWidth = 1;
		ctx.strokeRect(0, 0, ViewWidth * TileSize, ViewHeight * TileSize)
	}
}
class Tile
{
	id: keyof typeof tileIds = "sand";
	constructor(id?: keyof typeof tileIds)
	{
		if (id) this.id = id;
	}
	public draw()
	{
		const img = tileImages[this.id];
		if (img)
		{
			ctx.drawImage(img, 0, 0, TileSize, TileSize);
		}
	}
}

let world = new World(0, 0)

inp_width.addEventListener("change", () =>
{
	world = new World(inp_width.valueAsNumber, inp_height.valueAsNumber, world)
	inp_width.valueAsNumber = world.width;
	inp_height.valueAsNumber = world.height;
})
inp_height.addEventListener("change", () =>
{
	world = new World(inp_width.valueAsNumber, inp_height.valueAsNumber, world)
	inp_width.valueAsNumber = world.width;
	inp_height.valueAsNumber = world.height;
})
btn_up.addEventListener("click", () => world.up());
btn_right.addEventListener("click", () => world.right());
btn_down.addEventListener("click", () => world.down());
btn_left.addEventListener("click", () => world.left());

btn_save.addEventListener("click", () => {

});
btn_load.addEventListener("click", () => {

});
btn_new.addEventListener("click", async () =>
{
	if (world.height != 0 || world.width != 0)
	{
		let popup = new Popup();
		popup.content.appendChild(Div([], [], "Вы уверены, что хотите создать пустой мир?"));
		let r = await popup.openAsync();
		if (!r) return
		popup = new Popup();
		popup.content.appendChild(Div([], [], "Вы точно уверены, что хотите создать пустой мир?"));
		popup.reverse = true
		r = await popup.openAsync();
		if (!r) return
		popup = new Popup();
		popup.content.appendChild(Div([], [], "Вы уверены, что хотите создать пустой мир? Все несохранённые данные будут потеряны!"));
		r = await popup.openAsync();
		if (!r) return
	}
	world = new World(inp_width.valueAsNumber, inp_height.valueAsNumber)
});
inp_tilesize.addEventListener("change", () => TileSize = inp_tilesize.valueAsNumber);
canvas.addEventListener("wheel", e =>
{
	const moveSpeed = camera_speed();
	if (e.ctrlKey)
	{
		e.preventDefault();
		const v = 1.4
		if (e.deltaY > 0) TileSize /= v
		else TileSize *= v
		TileSize = Math.max(Math.round(TileSize), 2);
		inp_tilesize.valueAsNumber = TileSize;
	}
	else if (e.shiftKey)
	{
		if (e.deltaY > 0) camera_x += moveSpeed;
		else camera_x -= moveSpeed;
		const width = world.width * ViewWidth * TileSize;
		if (width > canvas.width)
		{
			camera_x = Math.max(Math.min(camera_x, 0), -width + canvas.width);
		}
		else camera_x = 0;
	}
	else
	{
		if (e.deltaY > 0) camera_y -= moveSpeed;
		else camera_y += moveSpeed;
		const height = world.height * ViewHeight * TileSize
		if (height > canvas.height)
		{
			camera_y = Math.max(Math.min(camera_y, 0), -height + canvas.height);
		}
		else camera_y = 0;
	}
});

function loadImages()
{
	for (const k in tileIds)
	{
		const key = <keyof typeof tileIds>k;
		const path = tileIds[key];
		// const img = document.createElement("img");
		const img = new Image()
		img.src = "../../src/data/images/" + path;
		img.addEventListener("load", () => tileImages[key] = img);
	}
}

loadImages();
loop();
function loop()
{
	const rect = div_viewport.getBoundingClientRect();
	canvas.width = rect.width;
	canvas.height = rect.height;
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.imageSmoothingEnabled = false;
	ctx.save();
	ctx.translate(camera_x, camera_y);
	world.draw();
	ctx.restore();
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

	requestAnimationFrame(loop);
}

type TileImages =
{
	[Property in keyof(typeof tileIds)]?: HTMLImageElement;
}