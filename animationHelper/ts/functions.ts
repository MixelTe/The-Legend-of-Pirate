function getCanvasContext(canvas: HTMLCanvasElement)
{
	const ctx = canvas.getContext("2d");
	if (ctx == null) throw new Error(`Context is null`);
	return ctx;
}
function getCanvas(id: string)
{
	const el = <unknown | null>document.getElementById(id);
	if (el == null) throw new Error(`${id} not found`);
	if (el instanceof HTMLCanvasElement) return el;
	throw new Error(`${id} element not Canvas`);
}
function getButton(id: string)
{
	const el = <unknown | null>document.getElementById(id);
	if (el == null) throw new Error(`${id} not found`);
	if (el instanceof HTMLButtonElement) return el;
	throw new Error(`${id} element not Button`);
}
function getInput(id: string)
{
	const el = <unknown | null>document.getElementById(id);
	if (el == null) throw new Error(`${id} not found`);
	if (el instanceof HTMLInputElement) return el;
	throw new Error(`${id} element not Input`);
}
function getSelect(id: string)
{
	const el = <unknown | null>document.getElementById(id);
	if (el == null) throw new Error(`${id} not found`);
	if (el instanceof HTMLSelectElement) return el;
	throw new Error(`${id} element not Select`);
}
