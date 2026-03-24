import random
import time
import functools

from splay_tree import SplayTree


def banchmark(func):
    functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        res = func(*args, **kwargs)
        end_time = time.perf_counter()
        t = end_time - start_time
        return t, res
    return wrapper


@banchmark
def test_find_in_list(lst: list, search_data: list[int]):
    counter = 0
    for val in search_data:
        if val in lst:
            counter += 1
    return counter


@banchmark
def test_find_in_tree(tree: SplayTree, search_data: list[int]):
    counter = 0
    for val in search_data:
        if tree.find(val):
            counter += 1
    return counter
    

def main():
    N_INSERT = 100_000          # количество вставляемых чисел
    N_SEARCH = 100_000          # количество проверяемых чисел
    RANGE_MIN = -10**6
    RANGE_MAX = 10**6
    random.seed(42)

    print("=== Генерация данных ===")
    # Генерируем числа для заполнения
    insert_data = [random.randint(RANGE_MIN, RANGE_MAX) for _ in range(N_INSERT)]
    # Создаём список и дерево
    lst = []
    tree = SplayTree()
    print("Заполнение списка и дерева...")
    start_fill = time.perf_counter()
    for val in insert_data:
        lst.append(val)
        tree.insert(val)
    end_fill = time.perf_counter()
    print(f"Время заполнения: {end_fill - start_fill:.3f} с")
    # Генерируем числа для поиска
    search_data = [random.randint(RANGE_MIN, RANGE_MAX) for _ in range(N_SEARCH)]
    # --------------------------------------------------------------
    # Тест 1: проверка наличия в списке
    # --------------------------------------------------------------
    print("\n=== Тест 1: проверка нахождения элементов в СПИСКЕ ===")
    time_find_in_list, count_find_in_list = test_find_in_list(lst=lst, search_data=search_data)
    print(f"Элементов найдено в списке: {count_find_in_list}")
    print(f"Время выполнения поиска в списке: {time_find_in_list}")
    # --------------------------------------------------------------
    # Тест 2: проверка наличия в дереве
    # --------------------------------------------------------------
    print("\n=== Тест 2: проверка нахождения элементов в ДЕРЕВЕ ===")
    time_find_in_tree, count_find_in_tree = test_find_in_tree(tree=tree, search_data=search_data)
    print(f"Элементов найдено в дереве: {count_find_in_tree}")
    print(f"Время выполнения поиска в дереве: {time_find_in_tree}")
    # --------------------------------------------------------------
    # Сравнение результатов
    # --------------------------------------------------------------
    assert count_find_in_list == count_find_in_tree
    print("\n=== Сравнение результатов ===")
    print(f"Найдено: (список) {count_find_in_list} = {count_find_in_tree} (дерево)")
    print(f"Время: (список) {time_find_in_list:.3f} - {time_find_in_tree:.3f} (дерево)")
    difference1 = time_find_in_list - time_find_in_tree
    difference2 = time_find_in_list / time_find_in_tree
    print(f"Время (разница):\n\t(список - дерево): {difference1:.3f}\n\t(список / дерево): {difference2:.3f}")


if __name__ == '__main__':
    main()