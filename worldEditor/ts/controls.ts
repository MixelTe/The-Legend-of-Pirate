const controls_popup = new Popup();
controls_popup.cancelBtn = false;
controls_popup.okBtn = false;
getButton("btn-controls").addEventListener("click", () => controls_popup.open());
controls_popup.content.appendChild(Div([], [
	H1([], [], "Управление"),
	Table([], [
		TR([], [
			TD([], [], "Движение экрана:"),
		]),
		TR([], [
			TD([], [], ""),
			TD([], [], "Тянуть с помощь ПКМ"),
		]),
		TR([], [
			TD([], [], "По вертикали"),
			TD([], [], "Колёсико мыши"),
		]),
		TR([], [
			TD([], [], "По горизонтали"),
			TD([], [], "Shift + Колёсико мыши"),
		]),
		TR([], [
			TD([], [], "Отцентрировать"),
			TD([], [], "ЛКМ + ПКМ"),
		]),
		TR([], [
			TD([], [], "Рисование:"),
		]),
		TR([], [
			TD([], [], ""),
			TD([], [], "ЛКМ или тянуть с помощь ЛКМ"),
		]),
		TR([], [
			TD([], [], "Пипетка"),
			TD([], [], "СКМ"),
		]),
	]),
]));
