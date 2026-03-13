from collections import Counter


def my_multisets_intersection(a: list[int], b: list[int]) -> list[int]:
    """Вернуть пересечение множеств

    Args:
        a (list[int]): первое множество
        b (list[int]): второй множество

    Returns:
        list[int]: пересечение множеств
    """
    counter_a, counter_b = Counter(a), Counter(b)
    c: list[int] = []
    for k, v in counter_a.items():
        if k not in counter_b:
            continue
        if v < counter_b[k]:
            c += [k] * v
        else:
            c += [k] * counter_b[k]
    return c


if __name__ == '__main__':
    res = f'''
Пример работы функции (my_multisets_intersection):
a = [1, 2, 3, 4, 4]
b = [3, 3, 4, 5, 6]
c = {my_multisets_intersection([1, 2, 3, 4, 4], [3, 3, 4, 5, 6])}

Запустите тесты (test_my_func.py) для рассмотрения множества примеров
'''
    print(res)
