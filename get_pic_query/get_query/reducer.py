#coding=utf-8
import sys

def get_top_query():
    query_dic = dict()
    last_uid = ''
    top_num = 10
    for line in sys.stdin:
        arr = line.strip().split('\t')
        if len(arr) != 5:
            continue
        uid = arr[0]
        if last_uid != uid and last_uid != '':
            sorted_dic = sorted(query_dic.items(), key=lambda d:d[1], reverse = True)
            count = 0
            try:
                output = last_uid + '\t' + uid_company[last_uid]
            except:
                output = last_uid + '\t' + 'unknown\tunknown'
            for key, value in sorted_dic:
                if count < top_num:
                    output += '\t' + key
                    count += 1
                else:
                    break
            print output
            last_uid = ''
            query_dic.clear()
        last_uid = uid
        query_dic[arr[1]] = float(arr[-1])

    sorted_dic = sorted(query_dic.items(), key=lambda d:d[1], reverse = True)
    count = 0
    try:
        output = last_uid + '\t' + uid_company[last_uid]
    except:
        output = last_uid + '\t' + 'unknown\tunknown'
    for key, value in sorted_dic:
        if count < top_num:
            output += '\t' + key
            count += 1
        else:
            break
    print output

def get_company_trade():
    userid_company = dict()
    with open('./uid_trade_company.csv', 'r') as f:
        for line in f:
            arr = line.strip().decode('gbk', 'ignore').encode('utf-8', 'ignore').split(';')
            if len(arr) != 5:
                continue
            userid_company[arr[0]] = arr[1] + '\t' + arr[-1]

    return userid_company
if __name__ == '__main__':
    uid_company = get_company_trade()
    get_top_query()
