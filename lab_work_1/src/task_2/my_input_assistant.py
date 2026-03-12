import re


class MyInputAssistant():
    def __init__(self):
        self.bigram: dict[str, dict[str, int]] = {}

    def _text_preprocessing(self, text: str) -> list[str]:
        text_lowercase: str = text.lower()
        word_list: list[str] = re.findall(r'[A-Za-zА-Яа-яЁё]+', text_lowercase)
        return word_list

    def _update_bigram(self, text: str) -> None:
        word_list = self._text_preprocessing(text)
        for i in range(len(word_list) - 1):
            word_bigram = self.bigram.setdefault(word_list[i], {})
            value = word_bigram.setdefault(word_list[i + 1], 0)
            word_bigram[word_list[i + 1]] = value + 1
            self.bigram[word_list[i]] = word_bigram

    def update_bigram_from_file(self, file_path: str) -> None:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        self._update_bigram(text)

    def update_bigram_from_str(self, text: str) -> None:
        self._update_bigram(text)

    def find_bigram_by_word(self, word: str, bigram_sorted: bool = True) -> dict[str, int] | None:
        word = word.lower().replace(' ', '')  
        if word not in self.bigram:
            return
        if not bigram_sorted:
            return self.bigram[word]
        return dict(sorted(self.bigram[word].items(), key=lambda item: item[1], reverse=True))

    def clear_bigram(self):
        self.bigram = {}
