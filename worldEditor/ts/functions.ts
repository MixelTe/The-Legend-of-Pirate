function Div(classes?: string[] | string, children?: HTMLElement[], innerText?: string)
{
	return initEl("div", classes, children, innerText);
}
function Span(classes?: string[] | string, children?: HTMLElement[], innerText?: string)
{
	return initEl("span", classes, children, innerText);
}
function H1(classes?: string[] | string, children?: HTMLElement[], innerText?: string)
{
	return initEl("h1", classes, children, innerText);
}
function Input(classes?: string[] | string, type?: string, placeholder?: string)
{
	const input = initEl("input", classes, undefined, undefined);
	if (type) input.type = type;
	if (placeholder) input.placeholder = placeholder;
	return input;
}
function Button(classes?: string[] | string, innerText?: string, clickListener?: (btn: HTMLButtonElement) => void)
{
	const button = initEl("button", classes, undefined, innerText);
	if (clickListener) button.addEventListener("click", clickListener.bind(undefined, button));
	return button;
}
function Table(classes?: string[] | string, children?: HTMLElement[])
{
	return initEl("table", classes, children, undefined);
}
function TR(classes?: string[] | string, children?: HTMLElement[])
{
	return initEl("tr", classes, children, undefined);
}
function TD(classes?: string[] | string, children?: HTMLElement[], innerText?: string)
{
	return initEl("td", classes, children, innerText);
}

function initEl<K extends keyof HTMLElementTagNameMap>(tagName: K, classes: string[] | string | undefined, children: HTMLElement[] | undefined, innerText: string | undefined)
{
	const el = document.createElement(tagName);
	if (classes)
	{
		if (typeof classes == "string") el.classList.add(classes);
		else classes.forEach(cs => el.classList.add(cs));
	}
	if (innerText) el.innerText = innerText;
	if (children) children.forEach(ch => el.appendChild(ch));

	return el;
}

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
function getTable(id: string)
{
	const el = <unknown | null>document.getElementById(id);
	if (el == null) throw new Error(`${id} not found`);
	if (el instanceof HTMLTableElement) return el;
	throw new Error(`${id} element not Table`);
}
function getDiv(id: string)
{
	const el = <unknown | null>document.getElementById(id);
	if (el == null) throw new Error(`${id} not found`);
	if (el instanceof HTMLDivElement) return el;
	throw new Error(`${id} element not Div`);
}

function rectPointIntersect(rect: {x: number, y: number, w: number, h: number}, point: {x: number, y: number})
{
	return (
		rect.x + rect.w >= point.x &&
		point.x >= rect.x &&
		rect.y + rect.h >= point.y &&
		point.y >= rect.y
	);
}
