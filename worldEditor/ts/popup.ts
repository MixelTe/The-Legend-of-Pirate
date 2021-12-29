interface PopupEvenListener {
	"close": (confirmed: boolean, popup: Popup) => void;
	"ok": (popup: Popup) => void;
	"cancel": (popup: Popup) => void;
}
type FocusEls = "ok" | "cancel" | "close" | "none";
class Popup
{
	public static Opened = 0;
	public content = Div();
	public set title(v: string) { this.titleEl.innerText = v; }
	public get title(): string { return this.titleEl.innerText }
	public set cancelText(v: string) { this.cancelBtnEl.innerText = v; }
	public get cancelText(): string { return this.cancelBtnEl.innerText }
	public set okText(v: string) { this.okBtnEl.innerText = v; }
	public get okText(): string { return this.okBtnEl.innerText }
	public set okBtn(v: boolean) { this.okBtnEl.style.display = v ? "" : "none"; }
	public get okBtn(): boolean { return this.okBtnEl.style.display != "none" }
	public set cancelBtn(v: boolean) { this.cancelBtnEl.style.display = v ? "" : "none"; }
	public get cancelBtn(): boolean { return this.cancelBtnEl.style.display != "none" }
	public set focusOn(v: FocusEls) { this.focusEl = v; this.setFocus(); };
	public get focusOn() { return this.focusEl; };
	public set reverse(v: boolean) { this.footer.classList.toggle("popup-footer-reverse", v); }
	public get reverse(): boolean { return this.footer.classList.contains("popup-footer-reverse"); }
	public closeOnBackClick = true;
	public closeEscape = true;

	private onClose: ((confirmed: boolean, popup: Popup) => void)[] = [];
	private onOk: ((popup: Popup) => void)[] = [];
	private onCancel: ((popup: Popup) => void)[] = [];
	private body = Div("popup");
	private titleEl = Div("popup-title");
	private cancelBtnEl = Button([], "Отмена", this.close.bind(this, false));
	private okBtnEl = Button([], "ОК", this.close.bind(this, true));
	private closeBtnEl = Button("popup-close", "x", this.close.bind(this, false));
	private footer = Div("popup-footer", [this.cancelBtnEl, this.okBtnEl]);
	private focusEl: FocusEls = "ok";
	private resolve: ((value: boolean) => void) | null = null;
	private onKeyUp: (e: KeyboardEvent) => void = () => {};
	protected openPopup()
	{
		Popup.Opened += 1;
		this.body = Div("popup");
		this.body.appendChild(Div("popup-block", [
			Div("popup-header", [
				this.titleEl,
				this.closeBtnEl,
			]),
			Div("popup-content", [this.content]),
			this.footer,
		]));
		this.body.addEventListener("click", e =>
		{
			if (this.closeOnBackClick && e.target == this.body) this.close(false);
		});
		this.onKeyUp = (e: KeyboardEvent) =>
		{
			if (e.code == "Escape") this.close(false);
		}
		window.addEventListener("keyup", this.onKeyUp);
		document.body.appendChild(this.body);
		this.setFocus();
	}
	public close(confirmed: boolean)
	{
		Popup.Opened -= 1;
		document.body.removeChild(this.body);
		window.removeEventListener("keyup", this.onKeyUp);
		this.fireEvent(confirmed ? "ok" : "cancel");
		this.fireEvent("close", confirmed);
		if (this.resolve) this.resolve(confirmed);
	}
	private fireEvent(type: keyof PopupEvenListener, confirmed = false)
	{
		switch (type) {
			case "close": this.onClose.forEach(f => f(confirmed, this)); break;
			case "ok": this.onOk.forEach(f => f(this)); break;
			case "cancel": this.onCancel.forEach(f => f(this)); break;
			default: throw new Error(`Listener can be: "close", "ok" or "cancel". Input: ${type}`);
		}
	}
	private setFocus()
	{
		switch (this.focusEl) {
			case "cancel": this.cancelBtnEl.focus(); break;
			case "close": this.closeBtnEl.focus(); break;
			case "ok": this.okBtnEl.focus(); break;
		}
	}


	public open()
	{
		this.openPopup();
	}
	public openAsync()
	{
		return new Promise<boolean>((resolve: (value: boolean) => void) =>
		{
			this.resolve = resolve;
			this.openPopup();
		});
	}
	public addListener<T extends keyof PopupEvenListener>(type: T, f: PopupEvenListener[T])
	{
		const fn = <any>f;
		switch (type) {
			case "close": this.onClose.push(fn); break;
			case "ok": this.onOk.push(fn); break;
			case "cancel": this.onCancel.push(fn); break;
			default: throw new Error(`Listener can be: "close", "ok" or "cancel". Input: ${type}`);
		}
	}
	public removeListener<T extends keyof PopupEvenListener>(type: T, f: PopupEvenListener[T])
	{
		const fn = <any>f;
		switch (type) {
			case "close": return removeFromArray(this.onClose, fn);
			case "ok": return removeFromArray(this.onOk, fn);
			case "cancel": return removeFromArray(this.onCancel, fn);
			default: throw new Error(`Listener can be: "close", "ok" or "cancel". Input: ${type}`);
		}
	}
}
function removeFromArray<T>(array: T[], item: T)
{
	const i = array.indexOf(item);
	if (i >= 0) array.splice(i, 1);
	return i >= 0;
}

interface contextMenuItem
{
	text: string;
	id?: string;
	subItems?: contextMenuItem[];
}
async function contextMenu(title: string, items: contextMenuItem[])
{
	return new Promise<string | null>((resolve) =>
	{
		const popup = new Popup();
		popup.title = title;
		popup.cancelBtn = false;
		popup.okBtn = false;
		const { menu, firstOption } = contextMenu_create(items, popup, resolve);
		popup.content.appendChild(menu);
		popup.addListener("cancel", () => resolve(null));
		popup.open();
		firstOption?.focus();
	});
}
function contextMenu_create(items: contextMenuItem[], popup: Popup, resolve: (value: string | null) => void)
{
	const menu = initEl("ul", "popup-contextMenu", undefined, undefined);
	let firstOption: HTMLButtonElement | null = null;
	for (let i = 0; i < items.length; i++) {
		const item = items[i];
		const { el, line } = contextMenu_item(item, popup, resolve);
		if (i == 0) firstOption = line;
		menu.appendChild(el);
	}
	return { menu, firstOption };
}
function contextMenu_item(item: contextMenuItem, popup: Popup, resolve: (value: string | null) => void)
{
	const el = document.createElement("li");
	const line = document.createElement("button");
	el.appendChild(line);
	const text = document.createElement("span");
	text.innerText = item.text;
	line.appendChild(text);
	if (item.subItems != undefined)
	{
		line.appendChild(Div("popup-contextMenu-arrow"));
		el.appendChild(contextMenu_create(item.subItems, popup, resolve).menu);
		line.addEventListener("click", () =>
		{
			el.classList.toggle("popup-contextMenu-open");
		});
	}
	else if (item.id != undefined)
	{
		el.addEventListener("click", () =>
		{
			popup.close(true);
			resolve(item.id ?? null);
		});
	}
	return { el, line };
}