from __future__ import annotations
from typing import Callable
from typing import TYPE_CHECKING

from tree_objects.utils import find_last_operator, addition, subtraction

# Для проверки типов
if TYPE_CHECKING:
    from tree_objects.addend_node import AddendNode
    from tree_objects.factor_node import FactorNode


class ExpressionNode:
    """Класс "Выражение"
    """
    def __init__(self, value: str, parent: 'FactorNode' = None):
        self.value: str = value
        self.parent: 'FactorNode' = parent
        self.left_node: 'AddendNode | ExpressionNode'= None
        self.right_node: 'AddendNode' = None
        self.operation: Callable[[float, float], float] = None
        self.result: float = None

    def construct(self) -> dict[str, float]:
        # Локальный импорт
        from tree_objects.addend_node import AddendNode

        expr = self.value.replace(' ', '').lower()
        if not expr:
            return {}
        pos = find_last_operator(expr, '+-')
        if pos != -1:
            op = expr[pos]
            left_str = expr[:pos]
            right_str = expr[pos+1:]

            # Обработка унарного минуса/плюса (левая часть пуста)
            if left_str == "":
                if op == '-':
                    # Унарный минус: 0 - rest
                    self.left_node = AddendNode("0", parent=self)
                    self.left_node.construct()
                    self.right_node = AddendNode(right_str, parent=self)
                    self.right_node.construct()
                    self.operation = subtraction
                else:  # op == '+'
                    # Унарный плюс игнорируем, просто берём правую часть
                    self.left_node = AddendNode(right_str, parent=self)
                    self.left_node.construct()
                    self.right_node = None
                    self.operation = None
                # Собираем переменные и возвращаем
                variables = {}
                self._collect_variables(variables)
                return variables

            # Обычная обработка бинарного оператора
            if find_last_operator(left_str, '+-') != -1:
                self.left_node = ExpressionNode(left_str, parent=self)
                self.left_node.construct()
            else:
                self.left_node = AddendNode(left_str, parent=self)
                self.left_node.construct()

            self.right_node = AddendNode(right_str, parent=self)
            self.right_node.construct()
            self.operation = addition if op == '+' else subtraction
        else:
            self.left_node = AddendNode(expr, parent=self)
            self.left_node.construct()

        variables = {}
        self._collect_variables(variables)
        return variables
    
    def _collect_variables(self, vars_dict: dict[str, float]):
        # Локальный импорт
        from tree_objects.expression_node import ExpressionNode
        from tree_objects.addend_node import AddendNode

        """Рекурсивно собирает имена переменных в словарь (значения пока None)."""
        if isinstance(self.left_node, (ExpressionNode, AddendNode)):
            self.left_node._collect_variables(vars_dict)
        if isinstance(self.right_node, (AddendNode)):
            self.right_node._collect_variables(vars_dict)

    def calculate(self, variables: dict[str, float]) -> float:
        left_val = self.left_node.calculate(variables)
        if self.right_node is not None:
            right_val = self.right_node.calculate(variables)
            self.result = self.operation(left_val, right_val)
        else:
            self.result = left_val
        return self.result

        