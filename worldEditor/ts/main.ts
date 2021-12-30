const inp_width = getInput("inp-width")
const inp_height = getInput("inp-height")
const inp_tilesize = getInput("inp-tilesize")
const btn_up = getButton("btn-up")
const btn_right = getButton("btn-right")
const btn_down = getButton("btn-down")
const btn_left = getButton("btn-left")
const btn_save = getButton("btn-save")
const inp_load = getInput("inp-load")
const btn_new = getButton("btn-new")
const inp_cameraSpeed = getInput("inp_cameraSpeed");
const inp_mode_pen = getInput("inp-mode-pen");
const inp_mode_fill = getInput("inp-mode-fill");
const inp_mode_view = getInput("inp-mode-view");
const inp_mode_entity = getInput("inp-mode-entity");
// const world_map = getTable("world-map")
const div_viewport = getDiv("viewport");
const div_palette = getDiv("palette");
const div_fast_palette = getDiv("fast-palette");
const canvas = getCanvas("canvas");
const ctx = getCanvasContext(canvas);

const localStorageKey = "WorldEditor-world-data";
const ViewWidth = 15;
const ViewHeight = 7;
let TileSize = 16 * 2;
// let TileSize = 16 * 4; // Temp
const tileIds = {
	sand1: "sand1.png",
	sand2: "sand2.png",
	sand3: "sand3.png",
	grass1: "grass1.png",
	grass2: "grass2.png",
	grass3: "grass3.png",
	water_deep: "water_deep.png",
	water_low: "water_low.png",
	water_sand: "water_sand.png",
}
const entity: (typeof Entity)[] = [
	Entity_Crab,
];
const tileImages: TileImages = {};
let icon_move: null | HTMLImageElement = null;
let icon_plus: null | HTMLImageElement = null;
const icon_center_rect = () => { const size = TileSize * 2; return { x: (ViewWidth * TileSize - size) / 2, y: (ViewHeight * TileSize - size) / 2, w: size, h: size } };
let icon_trash: null | HTMLImageElement = null;
const icon_trash_rect = () => { const size = TileSize * 0.9; return { x: (ViewWidth - 0.5) * TileSize - size, y: TileSize / 2, w: size, h: size * 1.5 } };

inp_tilesize.valueAsNumber = TileSize;
let camera_x = 0;
let camera_y = 0;
const camera_speed = () =>
{
	return Math.round(TileSize * inp_cameraSpeed.valueAsNumber / 2);
};
let pen: keyof (typeof tileIds) = "sand1";
let penEntity: typeof Entity | null = null;
let selectedEntity: Entity | null = null;
let worldFileName = "worldData.json";
let mousePos = { x: 0, y: 0 };


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
		// this.createTable();
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
		// world_map.innerHTML = "";
		for (let y = 0; y < this.height; y++)
		{
			const row = document.createElement("tr")
			// world_map.appendChild(row);
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
						popup.focusOn = "cancel";
						popup.content.appendChild(Div([], [], "Вы уверены, что хотите удалить экран?"));
						const r = await popup.openAsync();
						if (r)
						{
							const popup = new Popup();
							popup.focusOn = "cancel";
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
				if (x * viewWidth + camera_x > canvas.width ||
					y * viewHeight + camera_y > canvas.height ||
					(x + 1) * viewWidth + camera_x < 0 ||
					(y + 1) * viewHeight + camera_y < 0)
				{
					continue;
				}
				const view = this.map[y][x];
				ctx.save();
				ctx.fillStyle = "lightblue";
				ctx.translate(x * viewWidth, y * viewHeight);
				ctx.fillRect(0, 0, viewWidth, viewHeight);
				if (view)
				{
					ctx.save();
					if (view_moving && view_moving.vx == x && view_moving.vy == y) ctx.translate(view_moving.dx, view_moving.dy);
					view.draw();
					ctx.restore();
				}
				else
				{
					if (inp_mode_view.checked && icon_plus)
					{
						const rect = icon_center_rect();
						ctx.drawImage(icon_plus, rect.x, rect.y, rect.w, rect.h);
					}
				}
				ctx.restore();
			}
		}
		if (view_moving)
		{
			ctx.save();
			ctx.translate(view_moving.vx * viewWidth, view_moving.vy * viewHeight);
			ctx.translate(view_moving.dx, view_moving.dy);
			const view = this.map[view_moving.vy][view_moving.vx];
			if (view) view.draw();
			ctx.restore();
		}
	}

	private getView(x: number, y: number)
	{
		const width = TileSize * ViewWidth;
		const height = TileSize * ViewHeight;
		const X = Math.floor(x / width);
		const Y = Math.floor(y / height);
		if (X >= this.width || Y >= this.height) return { view: null, X, Y, vx: X, vy: Y };
		return { view: this.map[Y][X] || null, X: x - X * width, Y: y - Y * height, vx: X, vy: Y };
	}
	public fill(x: number, y: number)
	{
		const { view, X, Y } = this.getView(x, y);
		if (view) view.fill(X, Y);
	}
	public pen(x: number, y: number)
	{
		const { view, X, Y } = this.getView(x, y);
		if (view) view.pen(X, Y);
	}
	public pick(x: number, y: number)
	{
		const { view, X, Y } = this.getView(x, y);
		if (view) view.pick(X, Y);
	}
	public setCursor(x: number, y: number)
	{
		const { view, X, Y } = this.getView(x, y);
		if (view) view.setCursor(X, Y);
		else setCursor("pointer");
	}
	public mousedown(x: number, y: number)
	{
		const {view, X, Y, vx, vy } = this.getView(x - camera_x, y - camera_y);
		if (!view) return;
		view.mousedown(X, Y, x, y, vx, vy);
	}
	public mouseup(x: number, y: number)
	{
		const {view, X, Y, vx, vy } = this.getView(x - camera_x, y - camera_y);
		if (view_moving)
		{
			if (view) return;
			if (vx >= this.width || vy >= this.height || vx < 0 || vy < 0) return;
			this.map[vy][vx] = this.map[view_moving.vy][view_moving.vx];
			this.map[view_moving.vy][view_moving.vx] = undefined;
			return;
		}
		if (view) view.mouseup(X, Y, vx, vy);
		else
		{
			this.map[vy][vx] = new View();
		}
	}
	public getEntity(x: number, y: number)
	{
		const { view, X, Y, vx, vy } = this.getView(x, y);
		return { entity: view && view.getEntity(X, Y) || null, vx, vy };
	}
	public entity(x: number, y: number)
	{
		const { view, X, Y } = this.getView(x, y);
		if (view) view.setEntity(X, Y);
	}
	public saveToLocalStarage()
	{
		const data = this.getData();
		const json = JSON.stringify(data);
		localStorage.setItem(localStorageKey, json);
	}
	public getData()
	{
		const data: WorldData = {
			width: this.width,
			height: this.height,
			map: [],
		}
		for (let y = 0; y < this.width; y++)
		{
			const row: (ViewData | undefined)[] = [];
			for (let x = 0; x < this.height; x++)
			{
				const view = this.map[y][x];
				if (view) row.push(view.getData());
				else row.push(undefined);
			}
			data.map.push(row);
		}

		return data;
	}
	public static fromData(data: WorldData)
	{
		const world = new World(data.width, data.height);

		for (let y = 0; y < data.height; y++)
		{
			for (let x = 0; x < data.width; x++)
			{
				const vData = data.map[y][x];
				if (vData) world.map[y][x] = View.fromData(vData);
			}
		}
		return world;
	}
	public static loadFromLocalStorage()
	{
		const json = localStorage.getItem(localStorageKey);
		if (!json) return;
		World.loadData(json);
	}
	public static loadData(json: string)
	{
		try
		{
			const data = <WorldData>JSON.parse(json);
			const newWorld = World.fromData(data);
			world = newWorld;
		}
		catch (error)
		{
			console.error(error);
			const popup = new Popup();
			popup.cancelBtn = false;
			popup.content.appendChild(Div([], [], "Произошла ошибка при загрузке данных"));
			popup.open();
		}
	}
}
class View
{
	tiles: Tile[][] = [];
	entity: Entity[] = [];
	constructor()
	{
		for (let y = 0; y < ViewHeight; y++)
		{
			const line = []
			for (let x = 0; x < ViewWidth; x++)
			{
				if (x == 0 || x == ViewWidth - 1 || y == 0 || y == ViewHeight - 1)
				{
					line.push(new Tile("water_deep"))
				}
				else
				{
					const random = Math.floor(Math.random() * 3);
					if (random == 0) line.push(new Tile("sand1"));
					else if (random == 1) line.push(new Tile("sand2"));
					else line.push(new Tile("sand3"));
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
				let tile = this.tiles[y][x];
				ctx.save();
				ctx.translate(x * TileSize, y * TileSize);
				tile.draw();
				ctx.restore();
			}
		}
		ctx.save();
		if (!inp_mode_entity.checked) ctx.globalAlpha = 0.5;
		this.entity.forEach(e => e.draw());
		ctx.restore();
		ctx.strokeStyle = "black";
		ctx.lineWidth = 1;
		ctx.strokeRect(0, 0, ViewWidth * TileSize, ViewHeight * TileSize);
		if (inp_mode_view.checked)
		{
			ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
			ctx.fillRect(0, 0, ViewWidth * TileSize, ViewHeight * TileSize);
			if (icon_move)
			{
				const rect = icon_center_rect();
				ctx.drawImage(icon_move, rect.x, rect.y, rect.w, rect.h);
			}
			if (icon_trash)
			{
				const rect = icon_trash_rect();
				ctx.drawImage(icon_trash, rect.x, rect.y, rect.w, rect.h);
			}
		}
	}
	public fill(x: number, y: number)
	{
		const X = Math.floor(x / TileSize);
		const Y = Math.floor(y / TileSize);
		const tile = this.tiles[Y][X].id;
		this.fillR(X, Y, tile, []);
	}
	private fillR(x: number, y: number, tile: Tiles, path: number[])
	{
		if (x < 0 || y < 0 || x >= ViewWidth || y >= ViewHeight) return;
		if (this.tiles[y][x].id != tile) return;

		this.tiles[y][x].id = pen;
		const key = (x: number, y: number) => y * ViewWidth + x;
		path.push(key(x, y));
		if (path.indexOf(key(x + 1, y)) == -1) this.fillR(x + 1, y, tile, path);
		if (path.indexOf(key(x - 1, y)) == -1) this.fillR(x - 1, y, tile, path);
		if (path.indexOf(key(x, y + 1)) == -1) this.fillR(x, y + 1, tile, path);
		if (path.indexOf(key(x, y - 1)) == -1) this.fillR(x, y - 1, tile, path);
	}
	public pen(x: number, y: number)
	{
		const X = Math.floor(x / TileSize);
		const Y = Math.floor(y / TileSize);
		this.tiles[Y][X].id = pen;
	}
	public pick(x: number, y: number)
	{
		const X = Math.floor(x / TileSize);
		const Y = Math.floor(y / TileSize);
		pen = this.tiles[Y][X].id;
		fastPalette.addTile(pen);
	}
	public setCursor(x: number, y: number)
	{
		if (rectPointIntersect(icon_trash_rect(), { x, y }))
		{
			setCursor("pointer");
		}
		else
		{
			setCursor("move");
		}
	}
	public mousedown(x: number, y: number, rx: number, ry: number, vx: number, vy: number)
	{
		if (rectPointIntersect(icon_trash_rect(), { x, y }))
		{ }
		else
		{
			view_moving = { x: rx, y: ry, dx: 0, dy: 0, vx, vy };
		}
	}
	public async mouseup(x: number, y: number, vx: number, vy: number)
	{
		if (rectPointIntersect(icon_trash_rect(), { x, y }))
		{
			const popup = new Popup();
			popup.focusOn = "cancel";
			popup.content.appendChild(Div([], [], "Вы уверены, что хотите удалить экран?"));
			const r = await popup.openAsync();
			if (r)
			{
				const popup = new Popup();
				popup.focusOn = "cancel";
				popup.content.appendChild(Div([], [], "Вы точно уверены, что хотите удалить экран?"));
				popup.reverse = true;
				const r = await popup.openAsync();
				if (!r) return;
			}
			if (!r) return;
			world.map[vy][vx] = undefined;
		}
	}
	public getEntity(x: number, y: number)
	{
		for (let i = 0; i < this.entity.length; i++)
		{
			const e = this.entity[i];
			if (e.intersect(x, y)) return e;
		}
		return null;
	}
	public setEntity(x: number, y: number)
	{
		// const X = x / TileSize;
		// const Y = y / TileSize;
		const X = Math.floor(x / TileSize);
		const Y = Math.floor(y / TileSize);
		if (penEntity) this.entity.push(new penEntity(X, Y));
	}
	public getData()
	{
		const data: ViewData = {
			tiles: [],
			entity: [],
		}
		for (let y = 0; y < ViewHeight; y++)
		{
			const row: Tiles[] = [];
			for (let x = 0; x < ViewWidth; x++)
			{
				row.push(this.tiles[y][x].id);
			}
			data.tiles.push(row);
		}
		this.entity.forEach(e => data.entity.push(e.getData()));
		return data;
	}
	public static fromData(data: ViewData)
	{
		const view = new View();

		for (let y = 0; y < ViewHeight; y++)
		{
			for (let x = 0; x < ViewWidth; x++)
			{
				view.tiles[y][x] = new Tile(data.tiles[y][x]);
			}
		}
		data.entity.forEach(eData =>
		{
			const entity = Entity.fromData(eData);
			if (entity) view.entity.push(entity);
		});
		return view;
	}
}
class Tile
{
	id: Tiles = "sand1";
	constructor(id?: Tiles)
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

class MiniMap
{
	private canvas = getCanvas("minimap");
	private ctx = getCanvasContext(this.canvas);
	private size = 20;

	constructor()
	{
		this.canvas.addEventListener("contextmenu", e => e.preventDefault());
		this.canvas.addEventListener("mousedown", e =>
		{
			const x = Math.min(Math.floor(e.offsetX / this.size), world.width);
			const y = Math.min(Math.floor(e.offsetY / this.size), world.height);
			const X = x * TileSize * ViewWidth;
			const Y = y * TileSize * ViewHeight;
			if (e.button == 0)
			{
				camera_x = -(X - Math.round((canvas.width - ViewWidth * TileSize) / 2));
				camera_y = -(Y - Math.round((canvas.height - ViewHeight * TileSize) / 2));
				normalizeCamera();
			}
			else
			{
				centerView(X, Y);
			}
		});
	}

	public draw()
	{
		this.canvas.width = (this.size + 1) * world.width + 2;
		this.canvas.height = (this.size + 1) * world.height + 2;

		for (let y = 0; y < world.height; y++)
		{
			for (let x = 0; x < world.width; x++)
			{
				if (world.map[y] && world.map[y][x]) this.ctx.fillStyle = "rgb(243, 200, 81)";
				else this.ctx.fillStyle = "rgb(177, 225, 255)";
				this.ctx.fillRect(x * (this.size + 1) + 1, y * (this.size + 1) + 1, this.size, this.size);
			}
		}

		const coefX = (this.canvas.width - 2) / (world.width * ViewWidth * TileSize);
		const coefY = (this.canvas.height - 2) / (world.height * ViewHeight * TileSize);
		this.ctx.strokeStyle = "blue";
		this.ctx.strokeRect(-camera_x * coefX + 1, -camera_y * coefY + 1, canvas.width * coefX, canvas.height * coefY);
	}
}
class FastPalette
{
	private opened = false;
	private closedByClick = false;
	private imgs: HTMLDivElement[] = [];
	private tiles: Tiles[] = [pen];
	private entity: (typeof Entity | null)[] = [penEntity];
	private hovered: number | null = null;
	private addtileI = 1;
	private addentityI = 1;
	constructor()
	{
		const imgs = div_fast_palette.querySelectorAll(".fast-palette-part");
		for (let i = 0; i < imgs.length; i++)
		{
			const el = imgs[i];
			if (el instanceof HTMLDivElement)
			{
				this.imgs.push(el);
				el.addEventListener("mouseover", () => this.hovered = i);
				el.addEventListener("click", () =>
				{
					this.hovered = i;
					this.close(true);
				});
			}
		}
	}
	public open()
	{
		if (this.opened) return;
		this.hovered = null;
		this.opened = true;
		this.closedByClick = false;
		if (inp_mode_entity.checked) this.setPaletteEntity();
		else this.setPaletteTiles();
		div_fast_palette.style.left = `${mousePos.x}px`;
		div_fast_palette.style.top = `${mousePos.y}px`;
		div_fast_palette.classList.add("fast-palette-visible");
	}
	private setPaletteTiles()
	{
		for (let i = 0; i < this.imgs.length; i++)
		{
			const imgDiv = this.imgs[i];
			imgDiv.innerHTML = "";
			const imgTile = this.tiles.length > i ? tileImages[this.tiles[i]] : tileImages[this.tiles[0]];
			if (!imgTile) continue;
			const img = document.createElement("img");
			img.src = imgTile?.src;
			imgDiv.appendChild(img);
		}
	}
	private setPaletteEntity()
	{
		for (let i = 0; i < this.imgs.length; i++)
		{
			const imgDiv = this.imgs[i];
			imgDiv.innerHTML = "";
			const e = this.entity.length > i ? this.entity[i] : this.entity[0];
			if (!e)
			{
				const img = document.createElement("img");
				img.src = "imgs/none.png";
				imgDiv.appendChild(img);
				continue;
			}
			const img = document.createElement("canvas");
			e.draw(img, 65);
			imgDiv.appendChild(img);
		}
	}
	public close(closedByClick = false)
	{
		this.opened = false || this.closedByClick;
		div_fast_palette.classList.remove("fast-palette-visible");
		if (this.closedByClick || this.hovered == null) return;
		this.closedByClick = closedByClick;
		if (inp_mode_entity.checked) penEntity = this.entity.length > this.hovered ? this.entity[this.hovered] : this.entity[0];
		else pen = this.tiles.length > this.hovered ? this.tiles[this.hovered] : this.tiles[0];
	}
	public addTile(tileid: Tiles)
	{
		if (this.tiles.indexOf(tileid) != -1) return;
		this.tiles[this.addtileI] = tileid;
		this.addtileI = (this.addtileI + 1) % this.imgs.length;
	}
	public addEntity(entity: null | typeof Entity)
	{
		if (this.entity.indexOf(entity) != -1) return;
		this.entity[this.addentityI] = entity;
		this.addentityI = (this.addentityI + 1) % this.imgs.length;
	}
}

let world = new World(0, 0);
const minimap = new MiniMap();
const fastPalette = new FastPalette();

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
	const text = JSON.stringify(world.getData());
	var el = document.createElement('a');
	el.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
	el.setAttribute('download', worldFileName);

	el.style.display = 'none';
	document.body.appendChild(el);
	el.click();
	document.body.removeChild(el);
});
inp_load.addEventListener("input", async () =>
{
	const curFiles = inp_load.files;
	if (!curFiles) return;
	if (curFiles.length == 0) return;
	if (world.height != 0 && world.width != 0)
	{
		if (!await askForSure("заменить текущий мир")) return;
	}
	const file = curFiles[0];
	worldFileName = file.name;
	const data = await file.text();
	World.loadData(data);
});
btn_new.addEventListener("click", async () =>
{
	if (world.height != 0 && world.width != 0)
	{
		if (!await askForSure("создать пустой мир")) return;
	}
	world = new World(inp_width.valueAsNumber, inp_height.valueAsNumber)
});
inp_tilesize.addEventListener("change", () => TileSize = inp_tilesize.valueAsNumber);
inp_mode_entity.addEventListener("change", () => setPalete());
canvas.addEventListener("wheel", e =>
{
	const moveSpeed = camera_speed();
	if (e.ctrlKey)
	{
		e.preventDefault();
		const v = 1.4
		if (e.deltaY > 0)
		{
			TileSize /= v;
			camera_x /= v;
			camera_y /= v;
		}
		else
		{
			TileSize *= v;
			camera_x *= v;
			camera_y *= v;
		}
		TileSize = Math.max(Math.round(TileSize), 2);
		inp_tilesize.valueAsNumber = TileSize;
		normalizeCamera();
	}
	else if (e.shiftKey)
	{
		if (e.deltaY > 0) camera_x -= moveSpeed;
		else camera_x += moveSpeed;
		normalizeCamera();
	}
	else
	{
		if (e.deltaY > 0) camera_y -= moveSpeed;
		else camera_y += moveSpeed;
		normalizeCamera();
	}
});

let camera_moving: null | { x: number, y: number, cx: number, cy: number } = null;
let view_moving: null | { x: number, y: number, dx: number, dy: number, vx: number, vy: number } = null;
let entity_moving: null | { x: number, y: number, dx: number, dy: number, entity: Entity } = null;
let drawing: null | "pen" | "fill" | "entity" = null;
canvas.addEventListener("mousedown", e =>
{
	e.preventDefault();
	if (e.button == 0)
	{
		if (camera_moving)
		{
			centerView(e.offsetX - camera_x, e.offsetY - camera_y);
			camera_moving = null;
			return;
		}
		if (inp_mode_view.checked)
		{
			world.mousedown(e.offsetX, e.offsetY);
		}
		else if (inp_mode_entity.checked)
		{
			const { entity } = world.getEntity(e.offsetX - camera_x, e.offsetY - camera_y);
			if (entity)
			{
				entity_moving = { x: e.offsetX, y: e.offsetY, dx: 0, dy: 0, entity };
				if (selectedEntity == entity) selectedEntity = null;
				else selectedEntity = entity;
			}
			else
			{
				drawing = "entity";
				selectedEntity = null;
			}
		}
		else
		{
			if (inp_mode_pen.checked)
			{
				drawing = "pen";
			}
			else
			{
				drawing = "fill"
			}
		}
	}
	if (e.button == 2)
	{
		if (drawing)
		{
			centerView(e.offsetX - camera_x, e.offsetY - camera_y);
			drawing = null;
			return;
		}
		camera_moving = { x: e.offsetX, y: e.offsetY, cx: camera_x, cy: camera_y };
		setCursor("move");
	}
	if (e.button == 1)
	{
		if (inp_mode_entity.checked)
		{
			const { entity } = world.getEntity(e.offsetX - camera_x, e.offsetY - camera_y);
			if (entity)
			{
				penEntity = <typeof Entity>entity.constructor;
				fastPalette.addEntity(penEntity);
			}
		}
		else
		{
			world.pick(e.offsetX - camera_x, e.offsetY - camera_y);
		}
	}
});
canvas.addEventListener("mousemove", e =>
{
	setCursor("none")
	if (inp_mode_view.checked)
	{
		world.setCursor(e.offsetX - camera_x, e.offsetY - camera_y)
	}
	if (drawing)
	{
		if (drawing == "pen") world.pen(e.offsetX - camera_x, e.offsetY - camera_y);
		else drawing = null;
	}
	else if (entity_moving)
	{
		// entity_moving.dx = e.offsetX - entity_moving.x;
		// entity_moving.dy = e.offsetY - entity_moving.y;
		entity_moving.dx = Math.floor((e.offsetX - entity_moving.x + TileSize / 2) / TileSize) * TileSize;
		entity_moving.dy = Math.floor((e.offsetY - entity_moving.y + TileSize / 2) / TileSize) * TileSize;
		setCursor("move");
	}
	else if (camera_moving)
	{
		camera_x = camera_moving.cx + e.offsetX - camera_moving.x;
		camera_y = camera_moving.cy + e.offsetY - camera_moving.y;
		setCursor("move");
		normalizeCamera();
	}
	else if (view_moving)
	{
		view_moving.dx = e.offsetX - view_moving.x;
		view_moving.dy = e.offsetY - view_moving.y;
		setCursor("move");
		normalizeCamera();
	}
});
canvas.addEventListener("mouseup", e =>
{
	setCursor("none");
	if (inp_mode_view.checked)
	{
		if (e.button == 0) world.mouseup(e.offsetX, e.offsetY);
		world.setCursor(e.offsetX - camera_x, e.offsetY - camera_y)
	}
	if (drawing == "pen") world.pen(e.offsetX - camera_x, e.offsetY - camera_y);
	if (drawing == "fill") world.fill(e.offsetX - camera_x, e.offsetY - camera_y);
	if (drawing == "entity") world.entity(e.offsetX - camera_x, e.offsetY - camera_y);
	if (entity_moving) endEntityMove();
	drawing = null;
	camera_moving = null;
	view_moving = null;
	entity_moving = null;
});
canvas.addEventListener("mouseleave", () =>
{
	drawing = null;
	camera_moving = null;
	view_moving = null;
	entity_moving = null;
	setCursor("none");
});
canvas.addEventListener("contextmenu", e => e.preventDefault());
canvas.addEventListener("dblclick", e =>
{
	if (inp_mode_entity.checked && e.button == 0)
	{
		const { entity, vx, vy } = world.getEntity(e.offsetX - camera_x, e.offsetY - camera_y);
		if (entity) entity.openMenu(vx, vy);
	}
});
window.addEventListener("keypress", e =>
{
	if (Popup.Opened) return;
	switch (e.code) {
		case "KeyW": inp_mode_fill.checked = true; break;
		case "KeyS": inp_mode_pen.checked = true; break;
		case "KeyA": inp_mode_view.checked = !inp_mode_view.checked; break;
		case "KeyD": inp_mode_entity.checked = !inp_mode_entity.checked; setPalete(); break;
		// case "KeyC": endEntityMove()?.center(); break;
	}
});
window.addEventListener("keydown", e =>
{
	switch (e.code) {
		case "ArrowUp": world.up(); break;
		case "ArrowRight": world.right(); break;
		case "ArrowDown": world.down(); break;
		case "ArrowLeft": world.left(); break;
		case "KeyQ": fastPalette.open(); break;
	}
});
window.addEventListener("keyup", e =>
{
	switch (e.code) {
		case "KeyQ": fastPalette.close(); break;
	}
});
window.addEventListener("mousemove", e =>
{
	mousePos.x = e.pageX;
	mousePos.y = e.pageY;
});


function loadImages()
{
	function loadImage(url: string, onload: (img: HTMLImageElement) => void)
	{
		const img = new Image()
		img.src = url;
		img.addEventListener("load", () => onload(img));
	}
	for (const k in tileIds)
	{
		const key = <Tiles>k;
		const path = tileIds[key];
		tileImages[key] = undefined;
		loadImage("../../src/data/images/" + path, img => tileImages[key] = img);
	}
	loadImage("./imgs/icon-move.png", img => icon_move = img);
	loadImage("./imgs/icon-trash.png", img => icon_trash = img);
	loadImage("./imgs/icon-plus.png", img => icon_plus = img);
	entity.forEach(e => {
		loadImage("../../src/data/images/" + e.imgUrl, img => e.img = img);
	});
}
function centerView(x: number, y: number)
{
	let width = TileSize * ViewWidth;
	let height = TileSize * ViewHeight;
	const X = Math.floor(x / width);
	const Y = Math.floor(y / height);
	if (X >= world.width || Y >= world.height) return;
	TileSize = Math.min(canvas.width / ViewWidth, canvas.height / ViewHeight);
	TileSize = Math.floor(TileSize);
	inp_tilesize.valueAsNumber = TileSize;
	width = TileSize * ViewWidth;
	height = TileSize * ViewHeight;
	camera_x = - X * width + Math.floor((canvas.width - width) / 2);
	camera_y = - Y * height + Math.floor((canvas.height - height) / 2);
	normalizeCamera();
}
function normalizeCamera()
{
	const width = world.width * ViewWidth * TileSize;
	const height = world.height * ViewHeight * TileSize
	if (width > canvas.width)
	{
		camera_x = Math.max(Math.min(camera_x, 0), -width + canvas.width);
	}
	else camera_x = 0;
	if (height > canvas.height)
	{
		camera_y = Math.max(Math.min(camera_y, 0), -height + canvas.height);
	}
	else camera_y = 0;
}
function setCursor(cursor: "none" | "pointer" | "move")
{
	switch (cursor)
	{
		case "none":
			canvas.classList.remove("cursor-move");
			canvas.classList.remove("cursor-pointer");
			break;
		case "pointer":
			canvas.classList.remove("cursor-move");
			canvas.classList.add("cursor-pointer");
			break;
		case "move":
			canvas.classList.add("cursor-move");
			canvas.classList.remove("cursor-pointer");
			break;
	}
}
function setPalete()
{
	div_palette.innerHTML = "";
	if (inp_mode_entity.checked)
	{
		const img = document.createElement("img");
		img.title = "Отключить добавление";
		img.src = "./imgs/none.png";
		img.addEventListener("click", () => penEntity = null);
		div_palette.appendChild(img);
		entity.forEach(e =>
		{
			const img = document.createElement("canvas");
			img.title = e.name;
			div_palette.appendChild(img);
			function addImg()
			{
				if (!inp_mode_entity.checked) return;
				if (e.img)
				{
					e.draw(img, 48);
					img.addEventListener("click", () =>
					{
						penEntity = e;
						fastPalette.addEntity(penEntity);
					});
				}
				else setTimeout(addImg, 100);
			}
			addImg();
		});
	}
	else
	{
		selectedEntity = null;
		for (const k in tileImages)
		{
			const key = <keyof TileImages>k;
			function addImg()
			{
				if (inp_mode_entity.checked) return;
				const img = tileImages[key];
				if (img)
				{
					img.title = key;
					div_palette.appendChild(img);
					img.addEventListener("click", () =>
					{
						pen = key;
						fastPalette.addTile(pen);
					});
				}
				else setTimeout(addImg, 100);
			}
			addImg();
		}
	}
}
function endEntityMove()
{
	if (entity_moving)
	{
		entity_moving.entity.x += entity_moving.dx / TileSize;
		entity_moving.entity.y += entity_moving.dy / TileSize;
		entity_moving.entity.x = Math.min(Math.max(entity_moving.entity.x, 0), ViewWidth);
		entity_moving.entity.y = Math.min(Math.max(entity_moving.entity.y, 0), ViewHeight);
		entity_moving.entity.center();
		const entity = entity_moving.entity;
		entity_moving = null;
		return entity;
	}
}
async function askForSure(action: string)
{
	let popup = new Popup();
	popup.focusOn = "cancel";
	popup.content.appendChild(Div([], [], `Вы уверены, что хотите ${action}?`));
	let r = await popup.openAsync();
	if (!r) return false;
	popup = new Popup();
	popup.focusOn = "cancel";
	popup.content.appendChild(Div([], [], `Вы точно уверены, что хотите ${action}?`));
	popup.reverse = true
	r = await popup.openAsync();
	if (!r) return false;
	popup = new Popup();
	popup.focusOn = "cancel";
	popup.content.appendChild(Div([], [], `Вы уверены, что хотите ${action}? Все несохранённые данные будут потеряны!`));
	r = await popup.openAsync();
	if (!r) return false;
	return true;
}


loadImages();
setPalete();
World.loadFromLocalStorage();
loop();
setInterval(() => world.saveToLocalStarage(), 1000);
// btn_new.click() // Temp
// world.map[0][0] = new View(); // Temp
// penEntity = Entity_Crab; // Temp
// world.map[0][0]?.setEntity(100, 100); // Temp
// inp_mode_entity.checked = !inp_mode_entity.checked; // Temp
// setPalete(); // Temp
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

	minimap.draw();

	requestAnimationFrame(loop);
}

type TileImages =
{
	[Property in Tiles]?: HTMLImageElement;
}
type Tiles = keyof typeof tileIds;

interface WorldData
{
	map: (ViewData | undefined)[][];
	width: number;
	height: number;
}
interface ViewData
{
	tiles: Tiles[][];
	entity: EntitySaveData[];
}
interface EntitySaveData
{
	className: keyof typeof EntityDict;
	x: number;
	y: number;
	[a: string]: any;
}