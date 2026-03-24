from __future__ import annotations
from typing import TYPE_CHECKING

# Для проверки типов
if TYPE_CHECKING:
    from tree_objects.factor_node import FactorNode


class NumberNode:
    """Класс "Число"
    """
    def __init__(self, result: float, parent: 'FactorNode'):
        self.result: float = result
        self.parent: 'FactorNode' = parent

    def construct(self):
        pass

    def _collect_variables(self, vars_dict):
        pass

    def calculate(self, variables: dict[str, float]) -> float:
        return self.result
