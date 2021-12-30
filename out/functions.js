"use strict";
function Div(classes, children, innerText) {
    return initEl("div", classes, children, innerText);
}
function Span(classes, children, innerText) {
    return initEl("span", classes, children, innerText);
}
function H1(classes, children, innerText) {
    return initEl("h1", classes, children, innerText);
}
function Input(classes, type, placeholder) {
    const input = initEl("input", classes, undefined, undefined);
    if (type)
        input.type = type;
    if (placeholder)
        input.placeholder = placeholder;
    return input;
}
function Button(classes, innerText, clickListener) {
    const button = initEl("button", classes, undefined, innerText);
    if (clickListener)
        button.addEventListener("click", clickListener.bind(undefined, button));
    return button;
}
function Table(classes, children) {
    return initEl("table", classes, children, undefined);
}
function TR(classes, children) {
    return initEl("tr", classes, children, undefined);
}
function TD(classes, children, innerText) {
    return initEl("td", classes, children, innerText);
}
function initEl(tagName, classes, children, innerText) {
    const el = document.createElement(tagName);
    if (classes) {
        if (typeof classes == "string")
            el.classList.add(classes);
        else
            classes.forEach(cs => el.classList.add(cs));
    }
    if (innerText)
        el.innerText = innerText;
    if (children)
        children.forEach(ch => el.appendChild(ch));
    return el;
}
function getCanvasContext(canvas) {
    const ctx = canvas.getContext("2d");
    if (ctx == null)
        throw new Error(`Context is null`);
    return ctx;
}
function getCanvas(id) {
    const el = document.getElementById(id);
    if (el == null)
        throw new Error(`${id} not found`);
    if (el instanceof HTMLCanvasElement)
        return el;
    throw new Error(`${id} element not Canvas`);
}
function getButton(id) {
    const el = document.getElementById(id);
    if (el == null)
        throw new Error(`${id} not found`);
    if (el instanceof HTMLButtonElement)
        return el;
    throw new Error(`${id} element not Button`);
}
function getInput(id) {
    const el = document.getElementById(id);
    if (el == null)
        throw new Error(`${id} not found`);
    if (el instanceof HTMLInputElement)
        return el;
    throw new Error(`${id} element not Input`);
}
function getTable(id) {
    const el = document.getElementById(id);
    if (el == null)
        throw new Error(`${id} not found`);
    if (el instanceof HTMLTableElement)
        return el;
    throw new Error(`${id} element not Table`);
}
function getDiv(id) {
    const el = document.getElementById(id);
    if (el == null)
        throw new Error(`${id} not found`);
    if (el instanceof HTMLDivElement)
        return el;
    throw new Error(`${id} element not Div`);
}
function rectPointIntersect(rect, point) {
    return (rect.x + rect.w >= point.x &&
        point.x >= rect.x &&
        rect.y + rect.h >= point.y &&
        point.y >= rect.y);
}
