import re


class MyInputAssistant():
    def __init__(self):
        self.bigram: dict[str, dict[str, int]] = {}

    def _text_preprocessing(self, text: str) -> list[str]:
        """Подготовка текста

        Args:
            text (str): входной текст

        Returns:
            list[str]: список слов
        """
        text_lowercase: str = text.lower()
        word_list: list[str] = re.findall(r'[A-Za-zА-Яа-яЁё]+', text_lowercase)
        return word_list

    def _update_bigram(self, text: str) -> None:
        """Обновление словаря биграмм

        Args:
            text (str): входной текст
        """
        word_list = self._text_preprocessing(text)
        for i in range(len(word_list) - 1):
            # биграммы слова - возвращаем значение, иначе пустой словарь
            word_bigram = self.bigram.setdefault(word_list[i], {})
            # конкретное значение биграммы слова - возращает частоту, иначе 0
            value = word_bigram.setdefault(word_list[i + 1], 0)
            # обновляем частоту слова
            word_bigram[word_list[i + 1]] = value + 1
            # обновляем биграмму слова
            self.bigram[word_list[i]] = word_bigram

    def update_bigram_from_file(self, file_path: str) -> None:
        """Обновление словаря биграмм из файла

        Args:
            file_path (str): путь к файлу
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        self._update_bigram(text)

    def update_bigram_from_str(self, text: str) -> None:
        """Обновление словаря биграмм из текста

        Args:
            text (str): входной текст
        """
        self._update_bigram(text)

    def find_bigram_by_word(self, word: str, bigram_sorted: bool = True) -> dict[str, int] | None:
        """Поиск словаря биграмм по слову

        Args:
            word (str): слово
            bigram_sorted (bool, optional): сортировка словаря биграмм по по убыванию частоты. Defaults to True.

        Returns:
            dict[str, int] | None: _description_
        """
        word = word.lower().replace(' ', '')  
        if word not in self.bigram:
            return
        if not bigram_sorted:
            return self.bigram[word]
        return dict(sorted(self.bigram[word].items(), key=lambda item: item[1], reverse=True))

    def clear_bigram(self):
        """Очистить словарь биграмм
        """
        self.bigram = {}
