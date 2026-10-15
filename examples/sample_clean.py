# 一个写得比较规范的示例文件

from typing import Optional


def fibonacci(n):
    """生成前n个斐波那契数列"""
    if n < 0:
        raise ValueError("n不能为负数")
    if n == 0:
        return []
    if n == 1:
        return [0]

    fib = [0, 1]
    for _ in range(2, n):
        fib.append(fib[-1] + fib[-2])
    return fib


def binary_search(arr, target):
    """二分查找，返回索引，没找到返回None"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return None