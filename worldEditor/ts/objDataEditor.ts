class ObjDataEditor
{
	private readonly objDataCopy: ObjData;
	private readonly popup: Popup;
	constructor(obj: Entity | Decor, vx: number, vy: number)
	{
		this.objDataCopy = this.copyData(obj.objData);
		this.popup = new Popup();
		if (obj instanceof Entity) this.popup.title = "Редактирование сущности";
		else this.popup.title = "Редактирование декорации";
		const table = Table("entity-editor");
		this.popup.content.appendChild(table);
		const titles: { td: HTMLTableCellElement, data: EntityData<any> }[] = [];
		const onChange = (data: EntityData<any>) =>
		{
			for (const el of titles)
			{
				if (!el.data.smartTitle) continue;
				if (data.name == el.data.smartTitle.field)
				{
					const newTitle = el.data.smartTitle.titles[data.value];
					if (newTitle) el.td.innerText = newTitle;
					else el.td.innerText = el.data.title || el.data.name;
				}
			}
		}
		obj.objData.forEach(data =>
		{
			const colorRect = Div("color-rect");
			if (data.displayColor) colorRect.style.background = data.displayColor;
			const nameTD = TD([], [], data.name);
			if (data.title) nameTD.innerText = data.title;
			if (data.smartTitle)
			{
				titles.push({ td: nameTD, data });
				for (const data2 of obj.objData)
				{
					if (data2.name == data.smartTitle.field)
					{
						const newTitle = data.smartTitle.titles[data2.value];
						if (newTitle) nameTD.innerText = newTitle;
						else nameTD.innerText = data.title || data.name;
						break;
					}
				}
			}
			if (data.header)
			{
				const td = initEl("th", [], [], data.header)
				td.colSpan = 2;
				table.appendChild(TR([], [
					TD(),
					td,
				]));
			}
			const td = TD();
			const tr = TR([], [
				TD([], [colorRect]),
				nameTD,
				td
			]);
			table.appendChild(tr);
			if (data.options)
			{
				this.createValueEdit_select(data, td, onChange);
				return;
			}
			switch (data.type) {
				case "bool": this.createValueEdit_bool(<EntityData<"bool">>data, td, onChange); break;
				case "number": this.createValueEdit_number(<EntityData<"number">>data, td, onChange); break;
				case "text": this.createValueEdit_text(<EntityData<"text">>data, td, onChange); break;
				case "textAria": this.createValueEdit_textAria(<EntityData<"textAria">>data, td, onChange); break;
				case "aura": this.createValueEdit_aura(<EntityData<"aura">>data, td, onChange); break;
				case "area": this.createValueEdit_area(<EntityData<"area">>data, td, onChange); break;
				case "tile": this.createValueEdit_tile(<EntityData<"tile">>data, td, vx, vy, onChange); break;
				case "tiles": this.createValueEdit_tiles(<EntityData<"tiles">>data, td, vx, vy, onChange); break;
				case "tilesNumered": this.createValueEdit_tiles(<EntityData<"tilesNumered">>data, td, vx, vy, onChange); break;
				case "coords": this.createValueEdit_coords(<EntityData<"coords">>data, td, onChange); break;
				default: console.error("switch default"); break;
			}
		});
		table.appendChild(TR([], [
			TD(),
			TD([], [], obj instanceof Entity ? "Удалить сущность" : "Удалить декорацию"),
			TD([], [
				Button("delete-button", "Удалить", async () =>
				{
					let popup = new Popup();
					popup.focusOn = "cancel";
					let text = "Вы уверены, что хотите удалить сущность?"
					if (obj instanceof Decor) text = "Вы уверены, что хотите удалить декорацию?";
					popup.content.appendChild(Div([], [], text));
					let r = await popup.openAsync();
					if (!r) return
					const view = world.map[vy][vx];
					if (!view) return;
					if (obj instanceof Decor)
					{
						const i = view.decor.indexOf(obj);
						if (i >= 0)
						{
							view.decor.splice(i, 1);
							this.popup.close(true);
						}
					}
					else
					{
						const i = view.entity.indexOf(obj);
						if (i >= 0)
						{
							view.entity.splice(i, 1);
							this.popup.close(true);
						}
					}
				}),
			]),
		]));
		this.popup.addListener("cancel", () => obj.objData = this.objDataCopy);
		this.popup.addListener("close", () =>
		{
			if (obj instanceof Decor)
			{
				for (const decor of selectedDecors)
				{
					if (decor.constructor == obj.constructor)
					{
						decor.apllyData(obj.objData);
					}
				}
			}
		});
	}
	private copyData(objData: ObjData)
	{
		const newData: ObjData = JSON.parse(JSON.stringify(objData));
		return newData;
	}
	private createValueEdit_bool(data: EntityData<"bool">, td: HTMLTableCellElement, onChange: (data: EntityData<any>) => void)
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
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
		]));
		if (data.value) inpTrue.checked = true;
		else if (data.value == false) inpFalse.checked = true;
		else inpNone.checked = true;
		inpTrue.addEventListener("change", () => {data.value = inpTrue.checked; onChange(data)});
		inpFalse.addEventListener("change", () => {data.value = inpTrue.checked; onChange(data)});
		inpNone.addEventListener("change", () => { if (inpNone.checked) data.value = null; onChange(data) });
	}
	private createValueEdit_number(data: EntityData<"number">, td: HTMLTableCellElement, onChange: (data: EntityData<any>) => void)
	{
		const inpNone = Input([], "checkbox");
		const inp = Input([], "number");
		td.appendChild(Div([], [
			inp,
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
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
		inp.addEventListener("change", () => { data.value = inp.valueAsNumber; onChange(data); });
	}
	private createValueEdit_text(data: EntityData<"text">, td: HTMLTableCellElement, onChange: (data: EntityData<any>) => void)
	{
		const inpNone = Input([], "checkbox");
		const inp = Input([], "text");
		const dataListEl = Span();
		td.appendChild(Div([], [
			inp,
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
			dataListEl,
		]));
		if (data.optionsHint)
		{
			const dataList = document.createElement("datalist");
			dataList.id = "dataList" + data.name.replaceAll(" ", "-");
			dataListEl.appendChild(dataList);
			data.optionsHint.forEach(hint =>
			{
				const option = document.createElement("option");
				dataList.appendChild(option);
				option.innerText = hint;
			});
			inp.setAttribute("list", dataList.id);
		}
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
		inp.addEventListener("change", () => { data.value = inp.value; onChange(data); });

	}
	private createValueEdit_textAria(data: EntityData<"textAria">, td: HTMLTableCellElement, onChange: (data: EntityData<any>) => void)
	{
		const inpNone = Input([], "checkbox");
		const inp = initEl("textarea", undefined, undefined, undefined)
		td.appendChild(Div([], [
			inp,
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
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
		inp.addEventListener("change", () => { data.value = inp.value; onChange(data); });

	}
	private createValueEdit_rect(data: EntityData<"aura" | "area">, td: HTMLTableCellElement, addD: boolean, onChange: (data: EntityData<any>) => void)
	{
		const inpX = Input("inp-short", "number");
		const inpY = Input("inp-short", "number");
		const inpW = Input("inp-short", "number");
		const inpH = Input("inp-short", "number");
		let rect: Rect = [addD ? 0.5 : 0, addD ? 0.5 : 0, 1, 1 ];
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
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
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
		inpX.addEventListener("change", () => { rect[0] = inpX.valueAsNumber; onChange(data);});
		inpY.addEventListener("change", () => { rect[1] = inpY.valueAsNumber; onChange(data);});
		inpW.addEventListener("change", () => { rect[2] = inpW.valueAsNumber; onChange(data);});
		inpH.addEventListener("change", () => { rect[3] = inpH.valueAsNumber; onChange(data);});
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
		inpX.valueAsNumber = rect[0];
		inpY.valueAsNumber = rect[1];
		inpW.valueAsNumber = rect[2];
		inpH.valueAsNumber = rect[3];
	}
	private createValueEdit_aura(data: EntityData<"aura">, td: HTMLTableCellElement, onChange: (data: EntityData<any>) => void)
	{
		this.createValueEdit_rect(data, td, true, onChange);
	}
	private createValueEdit_area(data: EntityData<"area">, td: HTMLTableCellElement, onChange: (data: EntityData<any>) => void)
	{
		this.createValueEdit_rect(data, td, false, onChange);
	}
	private createValueEdit_tile(data: EntityData<"tile">, td: HTMLTableCellElement, vx: number, vy: number, onChange: (data: EntityData<any>) => void)
	{
		const inpNone = Input([], "checkbox");
		const span = Span([], [], "0;0 ");
		const btn = Button([], "Изменить");
		let point: Point = [0, 0];
		td.appendChild(Div([], [
			span,
			btn,
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
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
			span.innerText = `${point[0]}:${point[1]} `;
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
				span.innerText = `${point[0]}:${point[1]} `;
			}
			onChange(data);
		});
		btn.addEventListener("click", async () =>
		{
			const r = await new EntityEditor_TileSeclector(vx, vy, true).get();
			if (r) point = r[0];
			data.value = point;
			span.innerText = `${point[0]}:${point[1]} `;
			onChange(data);
		});
	}
	private createValueEdit_tiles(data: EntityData<"tiles" | "tilesNumered">, td: HTMLTableCellElement, vx: number, vy: number, onChange: (data: EntityData<any>) => void)
	{
		const inpNone = Input([], "checkbox");
		const span = Span([], [], "0шт ");
		const btn = Button([], "Изменить");
		let points: Point[] = [];
		td.appendChild(Div([], [
			span,
			btn,
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
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
			onChange(data);
		});
		btn.addEventListener("click", async () =>
		{
			const r = await new EntityEditor_TileSeclector(vx, vy, false, points, data.type == "tilesNumered").get();
			console.log(r);
			if (r) points = r;
			data.value = points;
			span.innerText = points.length + "шт ";
			onChange(data);
		});

	}
	private createValueEdit_select<T extends keyof EntityDataType>(data: EntityData<T>, td: HTMLTableCellElement, onChange: (data: EntityData<any>) => void)
	{
		if (data.type != "text" && data.type != "number" && data.type != "bool" && data.type != "tile")
		{
			const inp = document.createElement("select");
			const el = document.createElement("option");
			inp.appendChild(el);
			el.innerText = "type not supported!";
			inp.disabled = true
			el.style.color = "tomato";
			inp.style.color = "tomato";
			td.appendChild(Div([], [inp]));
			return;
		}
		const inpNone = Input([], "checkbox");
		const inp = document.createElement("select");
		td.appendChild(Div([], [
			inp,
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
		]));
		if (!data.options) return;
		for (const elData of data.options)
		{
			const el = document.createElement("option");
			inp.appendChild(el);
			el.value = `${elData}`;
			el.innerText = `${elData}`;
		}
		if (data.value == null)
		{
			inp.disabled = true;
			inpNone.checked = true;
		}
		else
		{
			inp.value = `${data.value}`;
		}
		function setValue()
		{
			if (data.type == "number") data.value = <any>parseFloat(inp.value);
			else if (data.type == "bool") data.value = <any>(inp.value == "true");
			else if (data.type == "tile") data.value = <any>(inp.value.split(",").map(v => parseInt(v)));
			else data.value = <any>inp.value;
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
				setValue();
				inp.disabled = false;
			}
			onChange(data);
		});
		inp.addEventListener("change", () => { setValue(); onChange(data); });
	}
	private createValueEdit_coords(data: EntityData<"coords">, td: HTMLTableCellElement, onChange: (data: EntityData<any>) => void)
	{
		const inpX = Input("inp-short", "number");
		const inpY = Input("inp-short", "number");
		let point: Point = [0, 0];
		const inpNone = Input([], "checkbox");
		td.appendChild(Div([], [
			initEl("label", [], [
				Span([], [], "X: "),
				inpX
			], undefined),
			initEl("label", [], [
				Span([], [], "Y: "),
				inpY
			], undefined),
			(data.nullable ? initEl("label", [], [
				inpNone,
				Span([], [], "None")
			], undefined) : Span()),
		]));
		inpNone.addEventListener("change", () =>
		{
			if (inpNone.checked)
			{
				data.value = null;
				inpX.disabled = true;
				inpY.disabled = true;
			}
			else
			{
				data.value = point;
				inpX.disabled = false;
				inpY.disabled = false;
			}
		});
		inpX.addEventListener("change", () => { point[0] = inpX.valueAsNumber; onChange(data);});
		inpY.addEventListener("change", () => { point[1] = inpY.valueAsNumber; onChange(data);});
		if (data.value == null)
		{
			inpX.disabled = true;
			inpY.disabled = true;
			inpNone.checked = true;
		}
		else
		{
			point = data.value;
		}
		inpX.valueAsNumber = point[0];
		inpY.valueAsNumber = point[1];
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
	private numered: boolean;
	constructor(vx: number, vy: number, oneTile: boolean, cur?: Point[], numered?: boolean)
	{
		this.popup = new Popup();
		this.view = world.map[vy][vx];
		this.numered = !!numered;
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
			this.cursor = [x, y];
			if (x < 0 || x >= ViewWidth || y < 0 || y >= ViewHeight)
			{
				this.cursor = undefined;
			}
			const i = this.pointSelected(x, y);
			if (!this.oneTile && drawing != null)
			{
				if (drawing)
				{
					if (i == null) this.selected.push([x, y]);
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
			drawing = i == null
			this.draw();
		});
		canvas.addEventListener("mouseup", e =>
		{
			const x = Math.floor(e.offsetX / this.tileSize);
			const y = Math.floor(e.offsetY / this.tileSize);
			const i = this.pointSelected(x, y);
			if (drawing == true)
			{
				if (i == null) this.selected.push([x, y]);
				if (this.oneTile) this.popup.close(true);
			}
			else if (drawing == false)
			{
				if (i != null) this.selected.splice(i, 1);
			}
			drawing = null;
			this.draw();
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
				const i = this.pointSelected(x, y)
				if (i != null)
				{
					this.ctx.fillStyle = "rgba(0, 255, 0, 0.2)";
					this.ctx.fillRect(0, 0, this.tileSize, this.tileSize);
					if (this.numered)
					{
						this.ctx.fillStyle = "rgba(255, 0, 255, 0.6)";
						this.ctx.font = "20px Aria"
						this.ctx.fillText(`${i}`, 6, 17);
					}
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
		if (this.cursor) drawTile(this.cursor[0], this.cursor[1], true);
	}
	private pointSelected(x: number, y: number, selected?: Point[])
	{
		if (selected == undefined) selected = this.selected;
		for (let i = 0; i < selected.length; i++)
		{
			const point = selected[i];
			if (point[0] == x && point[1] == y) return i;
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
			if (this.pointSelected(el[0], el[1], selected) == null)
			{
				selected.push(el);
			}
		});
		return selected;
	}
}