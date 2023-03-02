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
        # 有时候会出现 00:00:00 这种情况
        # 判断冒号的个数,如果是2个,则是时分秒,如果是1个,则是分秒
        if t.count(':') == 2:
            h, m, s = t.strip().split(":")
            return int(h) * 3600 + int(m) * 60 + int(s)
        elif t.count(':') == 1:
            m, s = t.strip().split(":")
            return int(m) * 60 + int(s)
    else:
        return ''
