#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Author  : minglei.guo
    @Contact : minglei@skyplatanus.com
    @Version : 1.0
    @Time    : 2020-03-27
'''
from typing import List


class Num2Hans(object):

    # 分组内的进位
    LG_DICT = {
        1: u'',
        2: u'拾',
        3: u'佰',
        4: u'仟'
    }
    # 分组间的单位
    HG_DICT = {
        #1: u'元',
        1: '',
        2: u'万',
        3: u'亿',
        4: u'兆'
    }
    # 数值对汉字
    NUMBER_DICT = {
        '0': u'零',
        '1': u'壹',
        '2': u'贰',
        '3': u'叁',
        '4': u'肆',
        '5': u'伍',
        '6': u'陆',
        '7': u'柒',
        '8': u'捌',
        '9': u'玖'
    }

    @staticmethod
    def split_integer(integer_str: str) -> List[str]:
        # 拆分函数，将整数字符串拆分成[亿，万，仟]的list
        group = []

        g = len(integer_str) % 4

        lx = len(integer_str) - 1
        if g > 0:
            group.append(integer_str[0:g])
        k = g
        while k <= lx:
            group.append(integer_str[k:k + 4])
            k += 4
        return group

    @classmethod
    def sub_change(cls, integer: str) -> List[str]:
        # 对[亿，万，仟]的list中每个字符串分组进行大写化再合并
        # 由高位到低位遍历
        hans_arr = []

        if integer == '0000':
            return hans_arr

        length = len(integer)
        lgrade = length

        for i, number in enumerate(integer):
            if number == '0':
                # 避免有 零 重复
                if i < length - 1:
                    if integer[i + 1] != '0':
                        # 没有连续的零
                        # 只留最后的那个零
                        hans_arr.append(cls.NUMBER_DICT[number])
            else:
                # 转换大写和进位
                hans_arr.extend([cls.NUMBER_DICT[number], cls.LG_DICT[lgrade]])
            lgrade -= 1

        return hans_arr

    @classmethod
    def transform(cls, data: str) -> str:

        hans = ''
        tmp_arr = []

        if "." in data:
            integer, decimal = data.split('.')
        else:
            integer = data
            decimal = ''

        if integer:
            integer_list = cls.split_integer(integer)  # 分解字符数组[亿，万，仟]三组List:['0000','0000','0000']
            group_lenght = len(integer_list)  # 获取拆分后的List长度
            # 大写合并
            for group in range(group_lenght):
                group_n2c = cls.sub_change(integer_list[group])
                if group_n2c:
                    # 过滤一个字符串全是0的情况
                    # 合并：前字符串大写+当前字符串大写+标识符
                    tmp_arr.extend(group_n2c)
                    tmp_arr.extend([cls.HG_DICT[group_lenght - group]])  # 合并：前字符串大写+当前字符串大写+标识符
        if decimal:
            # 处理小数部分
            d_lenght = len(decimal)
            if d_lenght == 1:  # 若小数只有1位
                if decimal[0] == '0':
                    tmp_arr.append(u'整')
                else:
                    tmp_arr.extend([cls.NUMBER_DICT[decimal[0]], u'角整'])
            else:  # 若小数有两位的四种情况
                if decimal[0] == '0' and decimal[1] != '0':
                    tmp_arr.extend([u'零', cls.NUMBER_DICT[decimal[1]], u'分'])
                elif decimal[0] == '0' and decimal[1] == '0':
                    tmp_arr.append(u'整')
                elif decimal[0] != '0' and decimal[1] != '0':
                    tmp_arr.extend([cls.NUMBER_DICT[decimal[0]], u'角', cls.NUMBER_DICT[decimal[1]], u'分'])
                else:
                    tmp_arr.extend([cls.NUMBER_DICT[decimal[0]], u'角整'])
        hans = ''.join(tmp_arr)
        return hans


if __name__ == '__main__':
    print(Num2Hans.transform('12345000789.456'))

