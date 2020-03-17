# _*_ coding: utf-8 _*_
# !/usr/bin/env python3

"""
Created on: 12/03/2020

@author: Collisio-Adolebitque
"""


def has_dup(ints: list) -> bool:
    """
    Return True if tuple comprehension produces an array of matching number(s) & False if not.
    :param ints:
    :return: bool
    """
    match = (i for i in range(0, len(ints)) for j in range(i+1, len(ints)) if ints[i] == ints[j])
    return True if match else False


def main():
    ints = [1, 2, 3, 4, 5, 4, 3, 7]
    # ints = [1, 2, 3, 4, 5, 6, 7]
    match = has_dup(ints)
    print('{}'.format(match))


if __name__ == '__main__':
    main()
