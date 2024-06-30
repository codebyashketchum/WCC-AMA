import re

from sympy import latex, sympify


class MathProcessor:
    def __init__(self):
        self.math_pattern = r"\$(.+?)\$"

    def contains_math(self, text: str) -> bool:
        return bool(re.search(self.math_pattern, text))

    def extract_math(self, text: str) -> list:
        return re.findall(self.math_pattern, text)

    def process_math(self, math_expr: str) -> str:
        try:
            expr = sympify(math_expr)
            return latex(expr)
        except:
            return math_expr

    def explain_math(self, text: str) -> str:
        math_expressions = self.extract_math(text)
        explanations = []

        for expr in math_expressions:
            latex_expr = self.process_math(expr)
            explanations.append(f"${latex_expr}$")

        return "\n".join(explanations)
