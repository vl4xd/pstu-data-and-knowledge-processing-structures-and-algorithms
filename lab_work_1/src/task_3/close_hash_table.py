

class CloseHashTable:
    def __init__(self, size: int = 1000) -> None:
        self.size: int = size
        self.table: list[list] = [[] for _ in range(size)]

    def _hash(self, obj: object) -> int:
        """Хэш объекта

        Args:
            obj (object): объект хэширования

        Raises:
            TypeError: возникает, когда данный класс не поддерживает тип объекта хэширования 

        Returns:
            int: хэш обхекта
        """
        if isinstance(obj, str):
            # полиномиальный хеш с основанием 31
            h = 0
            for ch in str(obj):
                h = (h * 31 + ord(ch)) % self.size
            return h
        raise TypeError(f'Ошибка: тип {type(obj)} не поддерживается данным класом.')
                
    def add(self, obj: object) -> bool:
        """Добавить объект в хэш-таблицу

        Args:
            obj (object): объект

        Returns:
            bool: True - объект добавлен, иначе - False
        """
        idx = self._hash(obj=obj)
        chain = self.table[idx]
        if obj in chain:
            return False
        chain.append(obj)
        return True
    
    def check(self, obj: object) -> bool:
        """Проверить объект в хэш-таблице

        Args:
            obj (object): объект

        Returns:
            bool: True - объект содерживаться в хэш-таблице, иначе - False
        """
        idx = self._hash(obj=obj)
        if obj in self.table[idx]:
            return True
        return False
    
    def collision_count(self) -> int:
        """Вернуть общее число коллизий (сумма (len-1) для цепочек длиной >1)

        Returns:
            int: количество коллизий
        """
        return sum(len(chain) - 1 for chain in self.table if len(chain) > 1)

    def __str__(self):
        for hash, chain in enumerate(self.table):
            if chain:
                print(f'({hash}) {chain}')
