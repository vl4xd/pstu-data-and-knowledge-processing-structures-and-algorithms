import re


class MyInputAssistant():
    def __init__(self):
        self.bigram: dict[str, dict[str, int]] = {}

    def _preprocessing(self, text: str) -> list[str]:
        text_lowercase: str = text.lower()
        text_list: list[str] = re.findall(r'[A-z]+|[Ё-ё]+', text_lowercase)
        return text_list

    def update_bigram(self, file_path: str):
        text = ''
        with open(file_path, 'r') as file:
            text = file.read()
        text_list = self._preprocessing(text)
        ...
