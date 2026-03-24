from __future__ import annotations
from typing import Callable
from typing import TYPE_CHECKING

from math_parser.tree_objects.utils import find_last_operator, multiplication, division

# Для проверки типов
if TYPE_CHECKING:
    from math_parser.tree_objects.expression_node import ExpressionNode
    from math_parser.tree_objects.factor_node import FactorNode


class AddendNode:
    """Класс "Слагаемое"
    """
    def __init__(self, value: str, parent: 'ExpressionNode'):
        self.value: str = value
        self.parent: 'ExpressionNode' = parent
        self.left_node: 'FactorNode | AddendNode' = None
        self.right_node: 'FactorNode' = None
        self.operation: Callable[[float, float], float] = None
        self.result: float = None
    
    def construct(self):
        # Локальный импорт
        from math_parser.tree_objects.addend_node import AddendNode
        from math_parser.tree_objects.factor_node import FactorNode

        expr = self.value.replace(' ', '').lower()
        if not expr:
            return
        pos = find_last_operator(expr, '*/')
        if pos != -1:
            op = expr[pos]
            left_str = expr[:pos]
            right_str = expr[pos+1:]
            if find_last_operator(left_str, '*/') != -1:
                self.left_node = AddendNode(left_str, parent=self)
                self.left_node.construct()
            else:
                self.left_node = FactorNode(left_str, parent=self)
                self.left_node.construct()
            self.right_node = FactorNode(right_str, parent=self)
            self.right_node.construct()
            self.operation = multiplication if op == '*' else division
        else:
            # Нет * или / — это множитель
            self.left_node = FactorNode(expr, parent=self)
            self.left_node.construct()
        
    def _collect_variables(self, vars_dict):
        if self.left_node:
            self.left_node._collect_variables(vars_dict)
        if self.right_node:
            self.right_node._collect_variables(vars_dict)

    def calculate(self, variables: dict[str, float]) -> float:
        left_val = self.left_node.calculate(variables)
        if self.right_node is not None:
            right_val = self.right_node.calculate(variables)
            self.result = self.operation(left_val, right_val)
        else:
            self.result = left_val
        return self.result

        