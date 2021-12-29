class EntityEditor
{
	private readonly objData: ObjData;
	private readonly popup: Popup;
	constructor(objData: ObjData)
	{
		this.objData = this.copyData(objData);
		this.popup = new Popup();
		this.popup.title = "Редактирование сущности";
		const table = Table("entity-editor");
		this.popup.content.appendChild(table);
		this.objData.forEach(data =>
		{
			const td = TD();
			const tr = TR([], [
				TD([], [], data.name),
				td
			]);
			table.appendChild(tr);
			switch (data.type) {
				case "bool": this.createValueEdit_bool(<any>data, td); break;
				case "number": this.createValueEdit_number(<any>data, td); break;
				case "text": this.createValueEdit_text(<any>data, td); break;
				case "aura": this.createValueEdit_aura(<any>data, td); break;
				case "area": this.createValueEdit_area(<any>data, td); break;
				case "tile": this.createValueEdit_tile(<any>data, td); break;
				case "tiles": this.createValueEdit_tiles(<any>data, td); break;
				default: console.error("switch default"); break;
			}
		});
	}
	private copyData(objData: ObjData)
	{
		const newData: ObjData = JSON.parse(JSON.stringify(objData));
		return newData;
	}
	private createValueEdit_bool(data: EntityData<"bool">, td: HTMLTableCellElement)
	{

	}
	private createValueEdit_number(data: EntityData<"number">, td: HTMLTableCellElement)
	{

	}
	private createValueEdit_text(data: EntityData<"text">, td: HTMLTableCellElement)
	{

	}
	private createValueEdit_aura(data: EntityData<"aura">, td: HTMLTableCellElement)
	{

	}
	private createValueEdit_area(data: EntityData<"area">, td: HTMLTableCellElement)
	{

	}
	private createValueEdit_tile(data: EntityData<"tile">, td: HTMLTableCellElement)
	{

	}
	private createValueEdit_tiles(data: EntityData<"tiles">, td: HTMLTableCellElement)
	{

	}

	public show()
	{
		this.popup.open();
	}
}