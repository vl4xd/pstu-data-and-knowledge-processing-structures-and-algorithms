from splay_node import SplayNode


class SplayTree:

    def __init__(self):
        self.root: SplayNode = None

    def _rotate_right(self, y: SplayNode):
        x = y.left
        if x is None:
            return
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    def _rotate_left(self, x: SplayNode):
        """Левый поворот вокруг узла x."""
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _splay(self, node: SplayNode):
        """Поднимает узел node в корень дерева с помощью серии поворотов."""
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if grandparent is None:
                # Zig – один поворот
                if node == parent.left:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
            else:
                if node == parent.left and parent == grandparent.left:
                    # Zig‑zig (левый‑левый)
                    self._rotate_right(grandparent)
                    self._rotate_right(parent)
                elif node == parent.right and parent == grandparent.right:
                    # Zig‑zig (правый‑правый)
                    self._rotate_left(grandparent)
                    self._rotate_left(parent)
                elif node == parent.left and parent == grandparent.right:
                    # Zig‑zag (левый‑правый)
                    self._rotate_right(parent)
                    self._rotate_left(grandparent)
                else:  # node == parent.right and parent == grandparent.left
                    # Zig‑zag (правый‑левый)
                    self._rotate_left(parent)
                    self._rotate_right(grandparent)

    def insert(self, key):
        """Вставка ключа в дерево. Дубликаты игнорируются."""
        if self.root is None:
            self.root = SplayNode(key)
            return

        # Обычный поиск места для вставки
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Ключ уже есть – поднимаем его и выходим
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Создаём новый узел
        new_node = SplayNode(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Поднимаем новый узел в корень
        self._splay(new_node)

    def find(self, key):
        """
        Поиск ключа в дереве.
        Возвращает True, если ключ присутствует, иначе False.
        Выполняет splay последнего посещённого узла.
        """
        if self.root is None:
            return False

        node = self.root
        last = None
        while node:
            last = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Ключ не найден, поднимаем последний посещённый узел
        if last:
            self._splay(last)
        return False