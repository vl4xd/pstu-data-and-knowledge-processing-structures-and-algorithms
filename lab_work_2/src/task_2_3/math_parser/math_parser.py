from math_parser.tree_objects.expression_node import ExpressionNode


class MathParser:

    def __init__(self, value: str):
        self.value: str = value
        self.root: ExpressionNode = None
        self.variables: dict[str, float] = None
        self.is_calculated: bool = False

    def assign_values(self, **kwargs) -> None:
        for var_name, value in kwargs.items():
            if var_name not in self.variables:
                raise ValueError(f"Unknown variable '{var_name}'")
            self.variables[var_name] = value

        # После присвоения всех переменных флаг вычисления сбрасываем,
        # чтобы следующий вызов calculate() использовал новые значения.
        self.is_calculated = False

    def construct(self) -> None:
        self.root = ExpressionNode(value=self.value)
        self.variables = self.root.construct()

    def calculate(self) -> float:
        if self.root is None:
            raise RuntimeError("Expression not constructed yet")
        # Проверяем, что все переменные имеют значения
        missing = [var for var, val in self.variables.items() if val is None]
        if missing:
            raise ValueError(f"Missing values for variables: {', '.join(missing)}")
        # Вычисляем
        if self.is_calculated:
            return self.root.result
        result = self.root.calculate(self.variables)
        self.is_calculated = True
        return result 
