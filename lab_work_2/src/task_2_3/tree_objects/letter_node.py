from __future__ import annotations
from typing import TYPE_CHECKING

# Для проверки типов
if TYPE_CHECKING:
    from tree_objects.factor_node import FactorNode   


class LetterNode:
    """Класс "Переменная"
    """
    def __init__(self, value: str, parent: 'FactorNode'):
        self.value: str = value
        self.parent: 'FactorNode' = parent
        self.result: float = None

    def construct(self):
        # Ничего не строим, просто лист
        pass

    def _collect_variables(self, vars_dict):
        # Добавляем имя переменной в словарь, если её ещё нет
        if self.value not in vars_dict:
            vars_dict[self.value] = None

    def calculate(self, variables: dict[str, float]) -> float:
        return variables[self.value]
