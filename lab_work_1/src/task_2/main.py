import subprocess
import os
import time
import tkinter as tk
from tkinter import filedialog

from my_input_assistant import MyInputAssistant


def clear_terminal():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)


def show_dialog_msg(dialog_msg: str, sleep: float = 1.8) -> None:
    clear_terminal()
    msg = f'# {dialog_msg} #'
    print(
f'''{'#'*len(msg)}
{msg}
{'#'*len(msg)}
'''
)
    time.sleep(sleep)


def select_file_txt() -> str:
    root = tk.Tk()
    file_path = filedialog.askopenfilename(
        parent=root,
        title="Выберите текстовый файл",
        filetypes=[("Текстовые файлы", "*.txt")]
    )
    root.destroy()
    return file_path


def user_selection(start: int, end: int, menu_msg: str) -> int:
    msg: str = 'Выберите пункт меню, указанный в скобках [ ]: '
    while True:
        err: bool = False
        clear_terminal()
        print(menu_msg)
        user_input = input(msg).replace(' ', '')
        if not err and user_input.isdigit():
            user_input = int(user_input)
        else:
            err = True           
        if not err and start <= user_input <= end:
            return user_input
        else:
            err = True
        if err:
            msg = f'(Ошибка: {user_input}) Выберите пункт меню, указанный в скобках [ ]: '


def main_menu() -> None:
    menu_msg = f'''
Главное меню: "Интеллектуальный помощник ввода"
{'_'*50}
[1] Обновить словарь биграмм
[2] Ввести текст с использование помощника

[0] Выход
{'‾'*50}'''
    mia = MyInputAssistant()
    menu_status: bool = True
    while menu_status:
        user_input = user_selection(start=0, end=2, menu_msg=menu_msg)
        match user_input:
            case 0:
                menu_status = False
            case 1:
                update_bigram(mia=mia)
            case 2:
                input_text_with_assistant(mia=mia)


def update_bigram(mia: MyInputAssistant) -> None:
    menu_msg = f'''
Обновить словарь биграмм: "Интеллектуальный помощник ввода"
{'_'* 50}
[1] Очистить словарь биграмм
[2] Ввести текст вручную
[3] Прочитать текст из файла (.txt)

[0] Назад
{'‾'*50}'''
    menu_status: bool = True
    while menu_status:
        user_input = user_selection(start=0, end=3, menu_msg=menu_msg)
        match user_input:
            case 0:
                menu_status = False
            case 1:
                mia.clear_bigram()
                show_dialog_msg(dialog_msg='Словарь биграмм успешно очищен!')
            case 2:
                update_bigram_from_str(mia=mia)
            case 3:
                file_path = select_file_txt()
                if file_path:
                    mia.update_bigram_from_file(file_path=file_path)
                    show_dialog_msg(dialog_msg='Словарь биграмм успешно обновлен!')


def update_bigram_from_str(mia: MyInputAssistant):
    clear_terminal()
    input_text = input('Введите текст: ')
    menu_msg = f'''Текст: {input_text}

Обновить биграмму по введенному тексту?
{'_'* 50}
[1] Да
[2] Нет
{'‾'*50}'''
    user_input = user_selection(start=1, end=2, menu_msg=menu_msg)
    if user_input == 1:
        mia.update_bigram_from_str(text=input_text)
        show_dialog_msg(dialog_msg='Словарь биграмм успешно обновлен!')


def input_text_with_assistant(mia: MyInputAssistant):
    text = ''
    last_word = ''
    while True:
        clear_terminal()
        print(f'Текст: {text}\n')
        print(f'{'_'* 50}')
        print('Возомжные продолжения:')
        bigram = mia.find_bigram_by_word(last_word)
        key_bigram = {}
        if not bigram:
            print('Слово не найдено! Продолжайте набор...')
        else:
            for i, (key, value) in enumerate(bigram.items()):
                key_bigram[f'!{i+1}'] = (key, value)
                print(f'[!{i+1}] {key} ({value})')
        print('\n[!finish] Назад')
        print(f'{'‾'*50}')
        last_word = input('Введите слово или ключ [ ]: ').replace(' ', '')
        if last_word == '!finish':
            break
        elif last_word in key_bigram:
            text += key_bigram[last_word][0] + ' '
            last_word = key_bigram[last_word][0]
        else:
            text += last_word + ' '


if __name__ == '__main__':
    main_menu()