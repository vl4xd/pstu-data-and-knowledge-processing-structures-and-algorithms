from math_parser.math_parser import MathParser


mp = MathParser('((((-4 * 20) + 3 + c))) + 174')
mp.construct()
print(f'{mp.value=}\n{mp.variables=}\n{mp.is_calculated=}')
mp.assign_values(**{'c': 3})
res = mp.calculate()
print(f'{res=}\n{mp.is_calculated=}')
mp.assign_values(**{'c': 4})
print(f'{mp.is_calculated=}')
res = mp.calculate()
print(f'{res=}\n{mp.is_calculated=}')
