from math_parser.math_parser import MathParser


#-------------------------------------------------------
# Пример №1
#-------------------------------------------------------
exp_example_1 = '1 + (2 + 3)'
mp_1 = MathParser(exp_example_1)
mp_1.construct()
res_1 = mp_1.calculate()
out_str_1 = f'''Пример №1
Выражение: {exp_example_1} = {res_1} (результат)
'''
print(out_str_1)
#-------------------------------------------------------
# Пример №2
#-------------------------------------------------------
exp_example_2 = 'a * b - c + (28 * 100) / 15 - 12'
mp_2 = MathParser(exp_example_2)
mp_2.construct()
mp_2.assign_values(
    **{
        'a': 10,
        'b': 2,
        'c': 15
    }
)
res_2 = mp_2.calculate()
out_str_2 = f'''Пример №2
Выражение: {exp_example_2} = {res_2} (результат)
Переменные: {mp_2.variables}
'''
print(out_str_2)
#-------------------------------------------------------
# Завершение
#-------------------------------------------------------
print('Больше примеров -> task_2_3/test_math_parser.py')
