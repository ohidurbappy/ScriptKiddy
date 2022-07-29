import time
import random
from decimal import Decimal


def method1():
    common_elements = [x for x in li1_temp if x in li2_temp]
    print(len(common_elements))


def method2():
    common_elements = (x for x in li1_temp if x in li2_temp)
    print(len(list(common_elements)))


def method3():
    common_elements = set(li1_temp) & set(li2_temp)
    print(len(common_elements))


def method4():
    common_elements = set(li1_temp).intersection(li2_temp)
    print(len(common_elements))


if __name__ == "__main__":
    li1 = []
    li2 = []
    for i in range(100000):
        li1.append(random.randint(0, 10000))
        li2.append(random.randint(0, 10000))

    li1_temp = list(set(li1))
    li2_temp = list(set(li2))

    methods = [method1, method2, method3, method4]
    for m in methods:
        start = time.perf_counter()
        m()
        end = time.perf_counter()
        print(Decimal((end - start)))