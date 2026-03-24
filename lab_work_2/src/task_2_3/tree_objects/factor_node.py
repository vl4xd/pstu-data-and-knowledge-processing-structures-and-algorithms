from __future__ import annotations
from typing import TYPE_CHECKING

# Для проверки типов
if TYPE_CHECKING:
    from tree_objects.addend_node import AddendNode
    from tree_objects.letter_node import LetterNode
    from tree_objects.number_node import NumberNode
    from tree_objects.expression_node import ExpressionNode


class FactorNode:
    """Класс "Множетель"
    """
    def __init__(self, value: str, parent: 'AddendNode'):
        self.value: str = value
        self.parent: 'AddendNode' = parent
        self.left_node: 'LetterNode | NumberNode | ExpressionNode' = None
        self.right_node: 'LetterNode | NumberNode | ExpressionNode' = None
        self.result: float = None

    def construct(self):
        # Локальный импорт
        from tree_objects.expression_node import ExpressionNode 
        from tree_objects.letter_node import LetterNode
        from tree_objects.number_node import NumberNode

        expr = self.value.replace(' ', '')
        if not expr:
            return
        # Унарный минус: преобразуем в 0 - (остаток)
        if expr[0] == '-':
            rest = expr[1:]  # всё после минуса
            if not rest:
                raise ValueError("Invalid factor: expected expression after '-'")
            # Создаём выражение "0 - rest"
            self.left_node = ExpressionNode(f"0 - {rest}", parent=self)
            self.left_node.construct()
            return
        if expr[0] == '(' and expr[-1] == ')':
            # Подвыражение в скобках
            inner = expr[1:-1]
            self.left_node = ExpressionNode(inner, parent=self)
            self.left_node.construct()
        elif len(expr) == 1 and expr.isalpha() and expr.islower():
            # Переменная (одна буква)
            self.left_node = LetterNode(expr, parent=self)
            self.left_node.construct()
        elif expr.isdigit():
            # Целое число
            self.left_node = NumberNode(int(expr), parent=self)
        else:
            raise ValueError(f"Invalid factor: {expr}")

    def _collect_variables(self, vars_dict):
        if self.left_node:
            self.left_node._collect_variables(vars_dict)
        if self.right_node:
            self.right_node._collect_variables(vars_dict)

    def calculate(self, variables: dict[str, float]) -> float:
        return self.left_node.calculate(variables)