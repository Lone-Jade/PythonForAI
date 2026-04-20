# x1 = chr(ord("D") + 2)
# print(x1)
# print(type(x1))

# print(1 == 1 is not True)
# print((1 == 1) is not True)

# print(-13 // 4)
# print(-10 % 4)
# print(10 % -3)

# print(bool(range(8, 5)))
# eval("3*2" + "22")
# print(eval("3*2" + "22"))
# print(max(["121", "34"]))
# print([1, 2, 3] * 2)
# print({1, 2, 3, 4} - {2, 4, 5})

# print(bin(int("11", 16)))
# print(type(bin(int("11", 16))))

# dict1 = {"1": 345, "2": "0b10001", "3": [1, 2, 3], "4": {3}}
# print(dict1)
# for key, value in dict1.items():
#     try:
#         print(key, value)
#         print(hash(value))
#     except:
#         print("Error, cannot hash this value")

# print(max([1, 2, 3], [2, 1, 3, 0], [3, 2, 1]))

# x2 = ["aaaa", "bc", "d", "b", "ba"]
# print(sorted(x2, key=len))
# try:
#     print(len(zip([1, 2, 3], "abcdefg")))
# except:
#     print("Error, cannot zip this list")

# # x=input(3)

# x3 = "[1,2,3,4]"
# print(list(x3))

# dict2 = {"a": 1, "b": 2, "c": 3}
# # print(dict1 + dict2)
# try:
#     print(dict1 + dict2)
# except:
#     print("Error, cannot add these two dictionaries")

# list1 = [1, 2, 3, 4, 5]
# list2 = [6, 7, 8, 9, 10]
# list3 = list1 + list2
# print(list3)


# from decimal import Decimal, getcontext
# import time


# def Leibniz_cal_pi(n):
#     """返回圆周率π的前n位数字（不含小数点）"""
#     # 设置精度：多留10位以避免舍入误差
#     getcontext().prec = n + 10

#     start_time = time.time()
#     # 初始值
#     pi = Decimal(0)
#     sign = Decimal(1)
#     term = Decimal(1)

#     # 迭代
#     for i in range(n**2):
#         pi += sign / term
#         sign *= -1
#         term = 2 * i + 3
#         if time.time() - start_time > 60:
#             print("超时，停止计算")
#             break

#     pi *= 4  # 最后乘以4

#     # 返回前n位（去掉小数点）
#     pi_str = str(pi)
#     if "." in pi_str:
#         pi_str = pi_str.replace(".", "")
#     return pi_str[:n]


# def Wallis_cal_pi(n):
#     """返回圆周率π的前n位数字（不含小数点）"""
#     # 设置精度：多留10位以避免舍入误差
#     getcontext().prec = n + 10

#     start_time = time.time()
#     pi = Decimal(1)
#     for i in range(1, n**2):
#         pi *= (
#             Decimal(4) * Decimal(i) ** 2 / (Decimal(4) * (Decimal(i)) ** 2 - Decimal(1))
#         )
#         if time.time() - start_time > 60:
#             print("超时，停止计算")
#             break

#     pi *= 2  # 最后乘以2
#     # 返回前n位（去掉小数点）
#     pi_str = str(pi)
#     if "." in pi_str:
#         pi_str = pi_str.replace(".", "")
#     return pi_str[:n]


# def arctan_cal_pi(n):
#     """返回圆周率π的前n位数字（不含小数点）"""
#     # 设置精度：多留10位以避免舍入误差
#     getcontext().prec = n + 10

#     start_time = time.time()
#     pi = Decimal(0)
#     sign = Decimal(1)
#     term = Decimal(1)

#     # 迭代
#     for i in range(n**2):
#         pi += sign * term / (2 * i + 1)
#         sign *= -1

#         if time.time() - start_time > 60:
#             print("超时，停止计算")
#             break

#     pi *= 4  # 最后乘以4

#     # 返回前n位（去掉小数点）
#     pi_str = str(pi)
#     if "." in pi_str:
#         pi_str = pi_str.replace(".", "")
#     return pi_str[:n]


# def arctan(x: Decimal, terms: int) -> Decimal:
#     """
#     计算arctan(x)的第n项
#     :param x: 数值
#     :param terms: 项数
#     :return: 第n项
#     """
#     x2 = x * x
#     res = x
#     denom = Decimal(1)
#     sign = Decimal(-1)
#     power = x  # x^(2n+1)
#     for _ in range(terms):
#         power *= x2
#         denom += 2
#         res += sign * power / denom
#         sign = -sign
#     return res


# def Machin_cal_pi(n):
#     """返回圆周率π的前n位数字（不含小数点）"""
#     # 设置精度：多留10位以避免舍入误差
#     getcontext().prec = n + 10

#     start_time = time.time()
#     pi = 4 * arctan(Decimal(1) / 5, 30) - arctan(Decimal(1) / 239, 20)
#     pi *= 4
#     pi_str = str(pi)
#     if "." in pi_str:
#         pi_str = pi_str.replace(".", "")
#     return pi_str[:n]


# def quick_cal_pi(n):
#     start_time = time.time()
#     """返回圆周率π的前n位数字（不含小数点）"""
#     # 设置精度：多留10位以避免舍入误差
#     getcontext().prec = n + 10

#     # 高斯-勒让德算法初始值
#     a = Decimal(1)
#     b = Decimal(1) / Decimal(2).sqrt()
#     t = Decimal(1) / Decimal(4)
#     p = Decimal(1)

#     # 迭代直到精度足够
#     for _ in range(20):  # 20次迭代足够5000位
#         a_next = (a + b) / 2
#         b = (a * b).sqrt()
#         t = t - p * (a - a_next) ** 2
#         p = 2 * p
#         a = a_next
#         if time.time() - start_time > 60:
#             print("超时，停止计算")
#             break

#     # 计算圆周率
#     pi = (a + b) ** 2 / (4 * t)

#     # 返回前n位（去掉小数点）
#     pi_str = str(pi)
#     # 注意：Decimal转字符串可能是 '3.14159...'，去掉小数点
#     if "." in pi_str:
#         pi_str = pi_str.replace(".", "")
#     # 截取前n位
#     return pi_str[:n]


# if __name__ == "__main__":
#     # print(Leibniz_cal_pi(1000))
#     print()
#     # print(Wallis_cal_pi(1000))
#     print()
#     print(arctan_cal_pi(1000))
#     print()
#     print(Machin_cal_pi(1000))
#     print()
#     print(quick_cal_pi(1000))

# from random import randint


# def factors(num, fac=[]):
#     for i in range(2, int(num**0.5) + 1):
#         if num % i == 0:
#             fac.append(i)
#             factors(num // i, fac)
#             # break
#     else:
#         fac.append(num)


# a = []
# factors(12, a)
# print(a)


# import numpy as np

# x = np.array([1, 2, 3, 4, 5])
# y = np.array([6, 7, 8, 9, 10])
# one = np.ones(len(x))
# print(x + y)
# print(x - y)
# print(x * y)
# print(x / y)
# print(x**y)
# print(x // y)
# print(x @ y)
# print(y @ x)
# print(np.sum(x, axis=0))
# print(np.dot(x, one))
# print(np.dot(one, x))

# import math

# sum_ = 0
# for i in range(0, 4):
#     sum_ += math.exp(-5) * 5**i / math.factorial(i)
# print(sum_)

# print(5 * math.exp(-5))
# print(math.exp(-9) * 18)

# x = 1 - math.exp(-3) * 4
# x = x / (1 - math.exp(-3))
# print(x)

# y = math.exp(3) - 4
# y = y / (math.exp(3) - 1)
# print(y)

# lambda_ = 220
# # 初始化累积和
# sum_ = 0.0
# # 计算第0项概率：P(0) = e^(-λ)
# p = math.exp(-lambda_)
# sum_ += p

# # 递推计算 1~220 项并累加
# for i in range(1, 221):
#     # 核心递推公式，无大数、无阶乘、无幂次
#     p = p * lambda_ / i
#     sum_ += p

# print(sum_)

import math

rho = (3 - math.sqrt(5)) / 2
print(rho, 1 - rho)
print((1 - rho) / rho, rho / (1 - rho))
print((1-rho)**2, rho**2)