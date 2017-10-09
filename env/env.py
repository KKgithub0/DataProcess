#!/usr/bin/env python
#encoding=gbk
import datetime

# �ж�һ��unicode�Ƿ��Ǻ���
def is_chinese(uchar):
    if u'\u4e00' <= uchar <= u'\u9fff':
        return True
    else:
        return False

# �ж�һ��unicode�Ƿ�������
def is_number(uchar):
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False

# �ж�һ��unicode�Ƿ���Ӣ����ĸ
def is_alphabet(uchar):
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False

# �ж��Ƿ�Ǻ��֣����ֺ�Ӣ���ַ�
def is_other(uchar):
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False

def is_single_gbk_chinese(gbk_str):
    try:
        u = gbk_str.decode('gbk')
        if len(u) == 1 and is_chinese(u[0]):
            return True
        return False
    except:
        return False

# gbkתΪutf-8
def gbk_2_utf(string):
    return string.decode('gbk', 'ignore').encode('utf-8', 'ignore')

# utf-8תΪgbk
def utf_2_gbk(string):
    return string.decode('utf-8', 'ignore').encode('gbk', 'ignore')

# ��ӡʱ��
def get_time():
    return datetime.datetime.now()

if __name__ == "__main__":
    ustring=u' \t�й� �������Ƶ��'
    # �ж��Ƿ��������ַ���
    for item in ustring:
        if (is_other(item)):
            print "%s is other"%(item)

    # ����
    gbk_str = "��"
    print "[%s] is_single_gbk_chinese [%s]"%(gbk_str, is_single_gbk_chinese(gbk_str))
    gbk_str = "��ok"
    print "[%s] is_single_gbk_chinese [%s]"%(gbk_str, is_single_gbk_chinese(gbk_str))
    gbk_str = "����"
    print "[%s] is_single_gbk_chinese [%s]"%(gbk_str, is_single_gbk_chinese(gbk_str))

