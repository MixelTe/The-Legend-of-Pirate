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
			TD([], [], "R"),
		]),
		TR([], [
			TD([], [], "Заливка"),
			TD([], [], "F"),
		]),
		TR([], [
			TD([], [], "Быстрая палитра"),
			TD([], [], "Q"),
		]),
		TR([], [
			TD([], [], "Открыть текущюю группу"),
			TD([], [], "W"),
		]),
		TR([], [
			TD([], [], "Подсвечивать тайл под курсором"),
			TD([], [], "H"),
		]),
		TR([], [
			TD([], [], "Скрыть декорции"),
			TD([], [], "J"),
		]),
		TR("row-spacer"),
		TR([], [
			TD([], [], "Мир:"),
		]),
		TR([], [
			TD([], [], "Режим экранов"),
			TD([], [], "S"),
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
			TD([], [], "Объекты:"),
		]),
		TR([], [
			TD([], [], "Режим сущностей"),
			TD([], [], "E"),
		]),
		TR([], [
			TD([], [], "Режим декораций"),
			TD([], [], "D"),
		]),
		TR([], [
			TD([], [], "Подвинуть объект"),
			TD([], [], "Тянуть с помощь ЛКМ"),
		]),
		TR([], [
			TD([], [], "Подвинуть объект без привязки к клеткам"),
			TD([], [], "Зажать shift при перемещении"),
		]),
		// TR([], [
		// 	TD([], [], "Отцентрировать сущность"),
		// 	TD([], [], "При перемещении нажать C"),
		// ]),
		TR([], [
			TD([], [], "Выделить объект"),
			TD([], [], "ЛКМ"),
		]),
		TR([], [
			TD([], [], "Редактировать объект"),
			TD([], [], "Двойное нажатие ЛКМ"),
		]),
		TR([], [
			TD([], [], "Удалить объект"),
			TD([], [], "Delete"),
		]),
		TR("row-spacer"),
		TR([], [
			TD([], [], "Выделение:"),
		]),
		TR([], [
			TD([], [], ""),
			TD([], [], "Тянуть с помощь ЛКМ с зажатым ctrl"),
		]),
		TR([], [
			TD([], [], "Добавить/удалить из выделения"),
			TD([], [], "ПКМ по объекту с зажатым ctrl"),
		]),
		TR([], [
			TD([], [], "очистить выделение"),
			TD([], [], "ПКМ по пустому месту с зажатым ctrl"),
		]),
		TR("row-spacer"),
		TR([], [
			TD([], [], "При выделении:"),
			TD([], [], ""),
		]),
		TR([], [
			TD([], [], "Delete"),
			TD([], [], "Удаляет все выделенные объекты"),
		]),
		TR([], [
			TD([], [], "Перемещение объекта"),
			TD([], [], "Двигаются все выделенные объекты"),
		]),
		TR([], [
			TD([], [], "Изменение свойств декорации"),
			TD([], [], "Изменения применяются ко всем \nвыделенным декорациям, того же типа"),
		]),
		TR([], [
			TD([], [], "Ctrl + C"),
			TD([], [], "Скопировать выделенные объекты"),
		]),
		TR([], [
			TD([], [], "Ctrl + X"),
			TD([], [], "Вырезать выделенные объекты"),
		]),
		TR([], [
			TD([], [], "Ctrl + V"),
			TD([], [], "Вставить выделенные объекты"),
		]),
	]),
]));
