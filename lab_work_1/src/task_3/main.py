import sys
import re
import random

from close_hash_table import CloseHashTable


def interactive_mode():
    ht = CloseHashTable()
    print("Введите команды (add <слово> / check <слово>). Для завершения Ctrl+D/Ctrl+Z.")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            continue
        cmd, word = parts[0].lower(), parts[1].lower()
        if cmd == "add":
            print('successful' if ht.add(word) else 'unsuccessful')
        elif cmd == "check":
            print("yes" if ht.check(word) else "no")
        else:
            print("Неизвестная команда")


def file_mode(filename):
    # чтение текста и выделение слов
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    words = re.findall(r'\w+', text.lower())
    unique_words = list(set(words))  # работаем с уникальными
    print(f"Всего уникальных слов: {len(unique_words)}")
    # параметры хеш-таблицы
    m = 20011  # размер таблицы (простое число)
    ht = CloseHashTable(m)
    # добавление слов и подсчёт коллизий
    for w in unique_words:
        ht.add(w)
    real_collisions = ht.collision_count()
    print(f"Число коллизий для собственной хэш-функции: {real_collisions}")
    # симуляция идеальной равномерной функции
    trials = 100 # количество экспериментов
    ideal_collisions_total = 0 # сумма коллизий по всем экспериментам
    for _ in range(trials):
        # случайное распределение индексов
        indices = [random.randint(0, m-1) for _ in range(len(unique_words))]
        # подсчёт коллизий (имитация цепочек)
        # для каждого индекса считаем, сколько раз он встретился
        from collections import Counter
        cnt = Counter(indices)
        ideal_collisions = sum(v - 1 for v in cnt.values() if v > 1)
        ideal_collisions_total += ideal_collisions
    avg_ideal_collisions = ideal_collisions_total / trials
    print(f"Среднее число коллизий для идеальной (равномерной) хэш-функции: {avg_ideal_collisions:.2f}")
    print(f"Отношение собственной к идеальной хэш-функции: {real_collisions / avg_ideal_collisions:.10f}")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--file":
        if len(sys.argv) > 2:
            file_mode(sys.argv[2])
        else:
            print("Укажите имя файла после --file")
    else:
        interactive_mode()
