class EntityEditor
{
	private readonly objDataCopy: ObjData;
	private readonly popup: Popup;
	constructor(entity: Entity, vx: number, vy: number)
	{
		this.objDataCopy = this.copyData(entity.objData);
		this.popup = new Popup();
		this.popup.title = "Редактирование сущности";
		const table = Table("entity-editor");
		this.popup.content.appendChild(table);
		entity.objData.forEach(data =>
		{
			const colorRect = Div("color-rect");
			if (data.displayColor) colorRect.style.background = data.displayColor;
			const td = TD();
			const tr = TR([], [
				TD([], [colorRect]),
				TD([], [], data.name),
				td
			]);
			table.appendChild(tr);
			switch (data.type) {
				case "bool": this.createValueEdit_bool(<EntityData<"bool">>data, td); break;
				case "number": this.createValueEdit_number(<EntityData<"number">>data, td); break;
				case "text": this.createValueEdit_text(<EntityData<"text">>data, td); break;
				case "aura": this.createValueEdit_aura(<EntityData<"aura">>data, td); break;
				case "area": this.createValueEdit_area(<EntityData<"area">>data, td); break;
				case "tile": this.createValueEdit_tile(<EntityData<"tile">>data, td, vx, vy); break;
				case "tiles": this.createValueEdit_tiles(<EntityData<"tiles">>data, td, vx, vy); break;
				default: console.error("switch default"); break;
			}
		});
		table.appendChild(TR([], [
			TD(),
			TD([], [], "Удалить сущность"),
			TD([], [
				Button("delete-button", "Удалить", async () =>
				{
					let popup = new Popup();
					popup.focusOn = "cancel";
					popup.content.appendChild(Div([], [], "Вы уверены, что хотите удалить сущность?"));
					let r = await popup.openAsync();
					if (!r) return
					const view = world.map[vy][vx];
					if (!view) return;
					const i = view.entity.indexOf(entity);
					if (i >= 0)
					{
						view.entity.splice(i, 1);
						this.popup.close(true);
					}
				}),
			]),
		]));
		this.popup.addListener("cancel", () => entity.objData = this.objDataCopy);
	}
	private copyData(objData: ObjData)
	{
		const newData: ObjData = JSON.parse(JSON.stringify(objData));
		return newData;
	}
	private createValueEdit_bool(data: EntityData<"bool">, td: HTMLTableCellElement)
	{
		const inpTrue = Input([], "radio");
		inpTrue.name = "entityEditor-bool" + Math.random();
		const inpFalse = Input([], "radio");
		inpFalse.name = inpTrue.name;
		const inpNone = Input([], "radio");
		inpNone.name = inpTrue.name;
		td.appendChild(Div([], [
			initEl("label", [], [
				inpTrue,
				Span([], [], "True")
			], undefined),
			initEl("label", [], [
				inpFalse,
				Span([], [], "False")
			], undefined),
			initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined),
		]));
		if (data.value) inpTrue.checked = true;
		else if (data.value == false) inpFalse.checked = true;
		else inpNone.checked = true;
		inpTrue.addEventListener("change", () => data.value = inpTrue.checked);
		inpFalse.addEventListener("change", () => data.value = inpTrue.checked);
		inpNone.addEventListener("change", () => { if (inpNone.checked) data.value = null });
	}
	private createValueEdit_number(data: EntityData<"number">, td: HTMLTableCellElement)
	{
		const inpNone = Input([], "checkbox");
		const inp = Input([], "number");
		td.appendChild(Div([], [
			inp,
			initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined),
		]));
		if (data.value == null)
		{
			inp.disabled = true;
			inpNone.checked = true;
		}
		else
		{
			inp.valueAsNumber = data.value;
		}
		inpNone.addEventListener("change", () =>
		{
			if (inpNone.checked)
			{
				data.value = null;
				inp.disabled = true;
			}
			else
			{
				data.value = inp.valueAsNumber;
				inp.disabled = false;
			}
		});
		inp.addEventListener("change", () => data.value = inp.valueAsNumber);
	}
	private createValueEdit_text(data: EntityData<"text">, td: HTMLTableCellElement)
	{
		const inpNone = Input([], "checkbox");
		const inp = Input([], "text");
		td.appendChild(Div([], [
			inp,
			initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined),
		]));
		if (data.value == null)
		{
			inp.disabled = true;
			inpNone.checked = true;
		}
		else
		{
			inp.value = data.value;
		}
		inpNone.addEventListener("change", () =>
		{
			if (inpNone.checked)
			{
				data.value = null;
				inp.disabled = true;
			}
			else
			{
				data.value = inp.value;
				inp.disabled = false;
			}
		});
		inp.addEventListener("change", () => data.value = inp.value);

	}
	private createValueEdit_rect(data: EntityData<"aura" | "area">, td: HTMLTableCellElement, addD = false)
	{
		const inpX = Input("inp-short", "number");
		const inpY = Input("inp-short", "number");
		const inpW = Input("inp-short", "number");
		const inpH = Input("inp-short", "number");
		let rect = { x: addD ? 0.5 : 0, y: addD ? 0.5 : 0, w: 1, h: 1 };
		const inpNone = Input([], "checkbox");
		td.appendChild(Div([], [
			initEl("label", [], [
				Span([], [], addD ? "dX: " : "X: "),
				inpX
			], undefined),
			initEl("label", [], [
				Span([], [], addD ? "dY: " : "Y: "),
				inpY
			], undefined),
			initEl("label", [], [
				Span([], [], "W: "),
				inpW
			], undefined),
			initEl("label", [], [
				Span([], [], "H: "),
				inpH
			], undefined),
			initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined),
		]));
		inpNone.addEventListener("change", () =>
		{
			if (inpNone.checked)
			{
				data.value = null;
				inpX.disabled = true;
				inpY.disabled = true;
				inpW.disabled = true;
				inpH.disabled = true;
			}
			else
			{
				data.value = rect;
				inpX.disabled = false;
				inpY.disabled = false;
				inpW.disabled = false;
				inpH.disabled = false;
			}
		});
		inpX.addEventListener("change", () => rect.x = inpX.valueAsNumber);
		inpY.addEventListener("change", () => rect.y = inpY.valueAsNumber);
		inpW.addEventListener("change", () => rect.w = inpW.valueAsNumber);
		inpH.addEventListener("change", () => rect.h = inpH.valueAsNumber);
		if (data.value == null)
		{
			inpX.disabled = true;
			inpY.disabled = true;
			inpW.disabled = true;
			inpH.disabled = true;
			inpNone.checked = true;
		}
		else
		{
			rect = data.value;
		}
		inpX.valueAsNumber = rect.x;
		inpY.valueAsNumber = rect.y;
		inpW.valueAsNumber = rect.w;
		inpH.valueAsNumber = rect.h;
	}
	private createValueEdit_aura(data: EntityData<"aura">, td: HTMLTableCellElement)
	{
		this.createValueEdit_rect(data, td, true);
	}
	private createValueEdit_area(data: EntityData<"area">, td: HTMLTableCellElement)
	{
		this.createValueEdit_rect(data, td);
	}
	private createValueEdit_tile(data: EntityData<"tile">, td: HTMLTableCellElement, vx: number, vy: number)
	{
		const inpNone = Input([], "checkbox");
		const span = Span([], [], "0;0 ");
		const btn = Button([], "Изменить");
		let point = { x: 0, y: 0 };
		td.appendChild(Div([], [
			span,
			btn,
			initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined),
		]));
		if (data.value == null)
		{
			btn.disabled = true;
			inpNone.checked = true;
			span.innerText = "";
		}
		else
		{
			point = data.value;
			span.innerText = `${point.x}:${point.y} `;
		}
		inpNone.addEventListener("change", () =>
		{
			if (inpNone.checked)
			{
				data.value = null;
				btn.disabled = true;
				span.innerText = "";
			}
			else
			{
				data.value = point;
				btn.disabled = false;
				span.innerText = `${point.x}:${point.y} `;
			}
		});
		btn.addEventListener("click", async () =>
		{
			const r = await new EntityEditor_TileSeclector(vx, vy, true).get();
			if (r) point = r[0];
			data.value = point;
			span.innerText = `${point.x}:${point.y} `;
		});
	}
	private createValueEdit_tiles(data: EntityData<"tiles">, td: HTMLTableCellElement, vx: number, vy: number)
	{
		const inpNone = Input([], "checkbox");
		const span = Span([], [], "0шт ");
		const btn = Button([], "Изменить");
		let points: Point[] = [];
		td.appendChild(Div([], [
			span,
			btn,
			initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined),
		]));
		if (data.value == null)
		{
			btn.disabled = true;
			inpNone.checked = true;
			span.innerText = "";
		}
		else
		{
			points = data.value;
			span.innerText = points.length + "шт ";
		}
		inpNone.addEventListener("change", () =>
		{
			if (inpNone.checked)
			{
				data.value = null;
				btn.disabled = true;
				span.innerText = "";
			}
			else
			{
				data.value = points;
				btn.disabled = false;
				span.innerText = points.length + "шт ";
			}
		});
		btn.addEventListener("click", async () =>
		{
			const r = await new EntityEditor_TileSeclector(vx, vy, false, points).get();
			console.log(r);
			if (r) points = r;
			data.value = points;
			span.innerText = points.length + "шт ";
		});

	}

	public show()
	{
		this.popup.open();
	}
}

class EntityEditor_TileSeclector
{
	private popup: Popup;
	private tileSize = 24;
	private view: View | undefined;
	private oneTile: boolean;
	private selected: Point[] = [];
	private ctx: CanvasRenderingContext2D;
	private cursor: Point | undefined;
	constructor(vx: number, vy: number, oneTile: boolean, cur?: Point[])
	{
		this.popup = new Popup();
		this.view = world.map[vy][vx];
		this.oneTile = oneTile;
		if (cur) this.selected = JSON.parse(JSON.stringify(cur));
		if (oneTile) this.popup.title = "Выбор клетки";
		else this.popup.title = "Выбор клеток";
		const canvas = document.createElement("canvas");
		this.popup.content.appendChild(canvas);
		this.popup.content.style.display = "flex";
		this.popup.content.style.justifyContent = "center";
		canvas.width = this.tileSize * ViewWidth;
		canvas.height = this.tileSize * ViewHeight;
		this.ctx = getCanvasContext(canvas);
		this.ctx.imageSmoothingEnabled = false;
		this.draw();
		let drawing: null | boolean = null;
		canvas.addEventListener("mousemove", e =>
		{
			const x = Math.floor(e.offsetX / this.tileSize);
			const y = Math.floor(e.offsetY / this.tileSize);
			this.cursor = { x, y };
			if (x < 0 || x >= ViewWidth || y < 0 || y >= ViewHeight)
			{
				this.cursor = undefined;
			}
			const i = this.pointSelected(x, y);
			if (!this.oneTile && drawing != null)
			{
				if (drawing)
				{
					if (i == null) this.selected.push({ x, y });
				}
				else
				{
					if (i != null) this.selected.splice(i, 1);
				};
			}
			this.draw();
		});
		canvas.addEventListener("mouseover", () => this.cursor = undefined);
		canvas.addEventListener("mousedown", e =>
		{
			const x = Math.floor(e.offsetX / this.tileSize);
			const y = Math.floor(e.offsetY / this.tileSize);
			const i = this.pointSelected(x, y);
			if (i == null) drawing = true;
			else drawing = false;
			this.draw();

		});
		canvas.addEventListener("mouseup", e =>
		{
			const x = Math.floor(e.offsetX / this.tileSize);
			const y = Math.floor(e.offsetY / this.tileSize);
			const i = this.pointSelected(x, y);
			if (drawing == true)
			{
				this.selected.push({ x, y });
				if (this.oneTile) this.popup.close(true);
			}
			else if (drawing == false)
			{
				if (i != null) this.selected.splice(i, 1);
			}
			drawing = null;
		});
	}
	private draw()
	{
		if (this.view == undefined) return;
		const drawTile = (x: number, y: number, shadow = false) =>
		{
			if (this.view == undefined) return;
			const tile = this.view.tiles[y][x];
			this.ctx.save();
			this.ctx.translate(x * this.tileSize, y * this.tileSize);
			if (shadow)
			{
				this.ctx.fillStyle = "rgba(0, 0, 0, 0.3)";
				this.ctx.fillRect(0, 0, this.tileSize, this.tileSize);
			}
			else
			{
				const img = tileImages[tile.id];
				if (img) this.ctx.drawImage(img, 0, 0, this.tileSize, this.tileSize);
				if (this.pointSelected(x, y) != null)
				{
					this.ctx.fillStyle = "rgba(0, 255, 0, 0.2)";
					this.ctx.fillRect(0, 0, this.tileSize, this.tileSize);
					this.ctx.strokeStyle = "lime";
					this.ctx.lineWidth = 1;
					const shift = 2;
					this.ctx.strokeRect(shift, shift, this.tileSize - shift * 2, this.tileSize - shift * 2);
				}
			}
			this.ctx.restore();
		}
		for (let y = 0; y < ViewHeight; y++)
		{
			for (let x = 0; x < ViewWidth; x++)
			{
				drawTile(x, y);
			}
		}
		if (this.cursor) drawTile(this.cursor.x, this.cursor.y, true);
	}
	private pointSelected(x: number, y: number, selected?: Point[])
	{
		if (selected == undefined) selected = this.selected;
		for (let i = 0; i < selected.length; i++)
		{
			const point = selected[i];
			if (point.x == x && point.y == y) return i;
		}
		return null;
	}
	public async get()
	{
		const r = await this.popup.openAsync();
		const selected: Point[] = [];
		if (!r || this.selected.length == 0) return null;
		this.selected.forEach(el =>
		{
			if (!this.pointSelected(el.x, el.y, selected))
			{
				selected.push(el);
			}
		});
		return selected;
	}
}