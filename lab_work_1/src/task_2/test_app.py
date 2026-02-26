import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QCompleter
from PyQt5.QtGui import QTextCursor, QKeyEvent
from PyQt5.QtCore import Qt, QStringListModel

class PredictiveTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabChangesFocus(False)  # Tab будет использоваться для выбора, а не для переключения фокуса

        # Модель биграмм: ключ - последнее слово, значение - список следующих слов
        # В реальном проекте загружайте из файла или базы данных
        self.bigram_model = {
            "": ["привет", "здравствуйте", "добрый"],          # начало предложения
            "я": ["хочу", "могу", "есть", "спать"],
            "хочу": ["есть", "пить", "спать", "гулять"],
            "ты": ["хочешь", "можешь", "идешь"],
            "он": ["сказал", "пошёл", "сделал"],
            "она": ["сказала", "пошла", "сделала"],
        }

        # Текущий контекст (последнее слово)
        self.context = ""

        # Настройка Completer
        self.completer = QCompleter()
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.activated.connect(self.insertCompletion)

        # Модель для списка подсказок (будет обновляться)
        self.list_model = QStringListModel()
        self.completer.setModel(self.list_model)

        # Инициализация контекста
        self.update_completer_model("")

    def update_completer_model(self, last_word):
        """Обновляет список подсказок на основе последнего слова."""
        suggestions = self.bigram_model.get(last_word, [])
        self.list_model.setStringList(suggestions)
        self.context = last_word

    def insertCompletion(self, completion):
        """Вставляет выбранное слово и пробел."""
        if self.completer.widget() != self:
            return

        tc = self.textCursor()
        tc.insertText(completion + " ")   # вставляем слово с пробелом
        self.setTextCursor(tc)

        # После вставки обновляем контекст (последним словом стало вставленное)
        self.update_completer_model(completion)

    def get_last_word(self):
        """Возвращает последнее слово перед курсором (без учёта текущего неоконченного)."""
        tc = self.textCursor()
        # Перемещаемся к началу предыдущего слова, затем выделяем его
        tc.movePosition(QTextCursor.PreviousWord, QTextCursor.MoveAnchor)
        tc.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)
        word = tc.selectedText().strip()
        return word

    def text_under_cursor(self):
        """Возвращает текущее слово (под курсором) для фильтрации."""
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def keyPressEvent(self, event: QKeyEvent):
        if self.completer and self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return

        was_space = (event.text() == " ")

        super().keyPressEvent(event)

        if was_space or event.key() == Qt.Key_Space:
            last_word = self.get_last_word()
            self.update_completer_model(last_word)
            self.completer.setCompletionPrefix("")   # <-- сброс фильтра
            self.show_completer()
            return

        prefix = self.text_under_cursor()
        self.completer.setCompletionPrefix(prefix)

        if len(prefix) >= 1 and self.completer.completionCount() > 0:
            self.show_completer()
        else:
            self.completer.popup().hide()

    def show_completer(self):
        """Отображает выпадающий список в позиции курсора."""
        if self.completer.completionCount() == 0:
            return
        cr = self.cursorRect()
        # Устанавливаем ширину попапа под самую длинную подсказку
        cr.setWidth(self.completer.popup().sizeHintForColumn(0) +
                    self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr)

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self)
        super().focusInEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Предиктивный ввод (как в телефоне)")
        self.setGeometry(100, 100, 600, 400)

        self.text_edit = PredictiveTextEdit()
        self.text_edit.setPlaceholderText("Введите 'я' и пробел, затем увидите подсказки...")
        self.setCentralWidget(self.text_edit)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())