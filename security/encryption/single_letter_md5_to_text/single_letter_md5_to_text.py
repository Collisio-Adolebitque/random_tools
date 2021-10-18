# _*_ coding: utf-8 _*_
# !/usr/bin/env python3

"""
Created on: 03/04/2021

@author: Collisio-Adolebitque
"""


def alphabet_hash_generator(characters: list) -> list:
    """
    Return True if tuple comprehension produces an array of matching number(s) & False if not.
    :param ints:
    :return: bool
    """
    match = (i for i in range(0, len(ints)) for j in range(i+1, len(ints)) if ints[i] == ints[j])
    return True if match else False


def main():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyx0123456789'
    hashes = [
        '69691c7bdcc3ce6d5d8a1361f22d04ac', 
        'd95679752134a2d9eb61dbd7b91c4bcc', 
        '7b8b965ad4bca0e41ab51de7b31363a1', 
        'b2f5ff47436671b6e533d8dc3614845d', 
        'd95679752134a2d9eb61dbd7b91c4bcc', 
        'f623e75af30e62bbd73d6df5b50bb7b5', 
        '9d5ed678fe57bcca610140957afab571'
        ]

    match = has_dup(ints)
    print('{}'.format(match))


if __name__ == '__main__':
    main()
