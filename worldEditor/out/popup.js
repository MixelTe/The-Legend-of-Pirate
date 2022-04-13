"use strict";
class Popup {
    static Opened = 0;
    content = Div();
    set title(v) { this.titleEl.innerText = v; }
    get title() { return this.titleEl.innerText; }
    set cancelText(v) { this.cancelBtnEl.innerText = v; }
    get cancelText() { return this.cancelBtnEl.innerText; }
    set okText(v) { this.okBtnEl.innerText = v; }
    get okText() { return this.okBtnEl.innerText; }
    set okBtn(v) { this.okBtnEl.style.display = v ? "" : "none"; }
    get okBtn() { return this.okBtnEl.style.display != "none"; }
    set cancelBtn(v) { this.cancelBtnEl.style.display = v ? "" : "none"; }
    get cancelBtn() { return this.cancelBtnEl.style.display != "none"; }
    set focusOn(v) { this.focusEl = v; this.setFocus(); }
    ;
    get focusOn() { return this.focusEl; }
    ;
    set reverse(v) { this.footer.classList.toggle("popup-footer-reverse", v); }
    get reverse() { return this.footer.classList.contains("popup-footer-reverse"); }
    closeOnBackClick = true;
    closeEscape = true;
    onClose = [];
    onOk = [];
    onCancel = [];
    body = Div("popup");
    titleEl = Div("popup-title");
    cancelBtnEl = Button([], "Отмена", this.close.bind(this, false));
    okBtnEl = Button([], "ОК", this.close.bind(this, true));
    closeBtnEl = Button("popup-close", "x", this.close.bind(this, false));
    footer = Div("popup-footer", [this.cancelBtnEl, this.okBtnEl]);
    focusEl = "ok";
    resolve = null;
    onKeyUp = () => { };
    openPopup() {
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
        this.body.addEventListener("click", e => {
            if (this.closeOnBackClick && e.target == this.body)
                this.close(false);
        });
        this.onKeyUp = (e) => {
            if (e.code == "Escape")
                this.close(false);
        };
        window.addEventListener("keyup", this.onKeyUp);
        document.body.appendChild(this.body);
        this.setFocus();
    }
    close(confirmed) {
        Popup.Opened -= 1;
        document.body.removeChild(this.body);
        window.removeEventListener("keyup", this.onKeyUp);
        this.fireEvent(confirmed ? "ok" : "cancel");
        this.fireEvent("close", confirmed);
        if (this.resolve)
            this.resolve(confirmed);
    }
    fireEvent(type, confirmed = false) {
        switch (type) {
            case "close":
                this.onClose.forEach(f => f(confirmed, this));
                break;
            case "ok":
                this.onOk.forEach(f => f(this));
                break;
            case "cancel":
                this.onCancel.forEach(f => f(this));
                break;
            default: throw new Error(`Listener can be: "close", "ok" or "cancel". Input: ${type}`);
        }
    }
    setFocus() {
        switch (this.focusEl) {
            case "cancel":
                this.cancelBtnEl.focus();
                break;
            case "close":
                this.closeBtnEl.focus();
                break;
            case "ok":
                this.okBtnEl.focus();
                break;
        }
    }
    open() {
        this.openPopup();
    }
    openAsync() {
        return new Promise((resolve) => {
            this.resolve = resolve;
            this.openPopup();
        });
    }
    addListener(type, f) {
        const fn = f;
        switch (type) {
            case "close":
                this.onClose.push(fn);
                break;
            case "ok":
                this.onOk.push(fn);
                break;
            case "cancel":
                this.onCancel.push(fn);
                break;
            default: throw new Error(`Listener can be: "close", "ok" or "cancel". Input: ${type}`);
        }
    }
    removeListener(type, f) {
        const fn = f;
        switch (type) {
            case "close": return removeFromArray(this.onClose, fn);
            case "ok": return removeFromArray(this.onOk, fn);
            case "cancel": return removeFromArray(this.onCancel, fn);
            default: throw new Error(`Listener can be: "close", "ok" or "cancel". Input: ${type}`);
        }
    }
}
function removeFromArray(array, item) {
    const i = array.indexOf(item);
    if (i >= 0)
        array.splice(i, 1);
    return i >= 0;
}
async function contextMenu(title, items) {
    return new Promise((resolve) => {
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
function contextMenu_create(items, popup, resolve) {
    const menu = initEl("ul", "popup-contextMenu", undefined, undefined);
    let firstOption = null;
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const { el, line } = contextMenu_item(item, popup, resolve);
        if (i == 0)
            firstOption = line;
        menu.appendChild(el);
    }
    return { menu, firstOption };
}
function contextMenu_item(item, popup, resolve) {
    const el = document.createElement("li");
    const line = document.createElement("button");
    el.appendChild(line);
    const text = document.createElement("span");
    text.innerText = item.text;
    line.appendChild(text);
    if (item.subItems != undefined) {
        line.appendChild(Div("popup-contextMenu-arrow"));
        el.appendChild(contextMenu_create(item.subItems, popup, resolve).menu);
        line.addEventListener("click", () => {
            el.classList.toggle("popup-contextMenu-open");
        });
    }
    else if (item.id != undefined) {
        el.addEventListener("click", () => {
            popup.close(true);
            resolve(item.id ?? null);
        });
    }
    return { el, line };
}
