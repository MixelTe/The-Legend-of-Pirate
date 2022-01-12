const controls_popup = new Popup();
controls_popup.cancelBtn = false;
controls_popup.okBtn = false;
getButton("btn-controls").addEventListener("click", () => controls_popup.open());
controls_popup.content.appendChild(Div([], [
	H1([], [], "Управление"),
	Table("controls-table", [
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
			TD([], [], "Приблизить/отдалить"),
			TD([], [], "Ctrl + Колёсико мыши"),
		]),
		TR([], [
			TD([], [], "Отцентрировать"),
			TD([], [], "ЛКМ + ПКМ\nПКМ на миникарте"),
		]),
		TR([], [
			TD([], [], "Переместить к экрану"),
			TD([], [], "ЛКМ на миникарте"),
		]),
		TR("row-spacer"),
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
		TR([], [
			TD([], [], "Ручка"),
			TD([], [], "S"),
		]),
		TR([], [
			TD([], [], "Заливка"),
			TD([], [], "W"),
		]),
		TR([], [
			TD([], [], "Быстрая палитра"),
			TD([], [], "Q"),
		]),
		TR([], [
			TD([], [], "Открыть текущюю группу"),
			TD([], [], "E"),
		]),
		TR("row-spacer"),
		TR([], [
			TD([], [], "Мир:"),
		]),
		TR([], [
			TD([], [], "Режим экранов"),
			TD([], [], "A"),
		]),
		TR([], [
			TD([], [], "Сдвинуть все экраны"),
			TD([], [], "Стрелки"),
		]),
		TR([], [
			TD([], [], "Подвинуть экран"),
			TD([], [], "Тянуть с помощь ЛКМ"),
		]),
		TR("row-spacer"),
		TR([], [
			TD([], [], "Сущности:"),
		]),
		TR([], [
			TD([], [], "Режим сущностей"),
			TD([], [], "D"),
		]),
		TR([], [
			TD([], [], "Подвинуть сущность"),
			TD([], [], "Тянуть с помощь ЛКМ"),
		]),
		// TR([], [
		// 	TD([], [], "Отцентрировать сущность"),
		// 	TD([], [], "При перемещении нажать C"),
		// ]),
		TR([], [
			TD([], [], "Выделить сущность"),
			TD([], [], "ЛКМ"),
		]),
		TR([], [
			TD([], [], "Редактировать сущность"),
			TD([], [], "Двойное нажатие ЛКМ"),
		]),
	]),
]));
