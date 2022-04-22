#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 4/22/22 10:56
# @Author  : StevenL
# @Email   : stevenl365404@gmail.com
# @File    : utils.py


def t2s(t):
    """

    Args:
        t: mm:ss

    Returns: 秒数

    """
    if ':' in t:
        m, s = t.strip().split(":")
        return int(m) * 60 + int(s)
    else:
        return ''
