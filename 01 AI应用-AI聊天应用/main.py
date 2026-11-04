# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。


# def print_hi(name):
#     # 在下面的代码行中使用断点来调试脚本。
#     print(f'Hi, {name}')  # 按 ⌘F8 切换断点。
#
#
# # 按装订区域中的绿色按钮以运行脚本。
# if __name__ == '__main__':
#     print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助

# opt = input('opt:')
# num1 = float(input('number1'))
# num2 = float(input('number2'))
# match opt:
#     case '+':
#         print(num1+num2)
#     case '-':
#         print(num1-num2)
#     case '*':
#         print(num1*num2)
#     case '/':
#         print(num1/num2)
#     case _:
#         print('exit')

# i=100
# sum=0
# while i>0:
#     if i % 2==0:
#         sum+=i
#     i-=1
# else:
#     print(sum)
# num=range(0,10,2)
# print(type(num))
# for i in range(0,10,2):
#     print(i)
# l = int(input('length'))
# w = int(input('width'))
# for i in range(w):
#     for j in range(l):
#         print('*', end=' ')
#     print()
# print(1,2, 4,end='*')
# print(2)

# 99乘法表
# i=1
# while i<10:
#     j = 1
#     while j<=i:
#         print(f"{j} x {i} = {j * i}", end = "\t")
#         j+=1
#     print()
#     i+=1

# 猜随机数
# import random
# random_number = random.randint(1, 101)
# while True:
#     input_number = float(input("请输入数字:"))
#     if random_number < input_number:
#         print("大了")
#         continue
#     elif random_number > input_number:
#         print("小了")
#         continue
#     else:
#         print("对了")
#         break
# count = 10
# input_list = []
# print('请输入10个数，回车')
# for i in range(10):
#     input_list.append(float(input()))
# input_list.sort()
# print(f"min={input_list[0]}, max={input_list[-1]}, avg={sum(input_list) / len(input_list)}")


# num = [1,2,3,4,5]
# num2 = [0,1,5,9]
# num3 = [*num,*num2]
# for i in num2:
#     if i not in num3:
#         print("true")

# list = []
# list.
# for i in range(20):
#     list.append((i+1) ** 2)
# print(list)

# str = 'ertyy'
# print('yy' in str)

# d = {}
# d['a'] = 1
# d['b'] = 2
# d['c'] = 3
# d['d'] = 4
# print(type(d.items()))
# print(type(d.keys()))
# d.pop('a')
# del d['d']
# print(d)

"""
#  #
# #
"""
from textwrap import indent

# def fun(a):
#     """
#
#     :param a:
#     :return:
#     """
#     pass

l = "  aaaa    "
# print(l.strip())

import  json
obj = {
    "name": "zhangsan",
    "age": 18
}

with open('json.json', 'w', encoding='utf-8') as f:
    # indent 添加缩进，即格式化
    # ensure_ascii=False 确保中文不被转义，默认会被转义成ascii码
    json.dump(obj, f, ensure_ascii=False, indent=2)