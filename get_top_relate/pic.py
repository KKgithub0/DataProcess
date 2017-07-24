#coding=utf-8
import sys
import re
def get_top_center():
    userid_center_dict = dict()
    with open('userid_center_charge.csv_new', 'r') as f:
        for line in f:
            arr = line.strip().split(';')
            if len(arr) != 5:
                continue
            try:
                ctr = float(arr[3]) / int(arr[2])
            except:
                continue
            userid_center_dict.setdefault(arr[0], {})
            userid_center_dict[arr[0]][arr[1]] = ctr
    userid_pic = dict()
    for k, v in userid_center_dict.iteritems():
        userid_pic.setdefault(k, [])
        sorted_dic = sorted(v.items(), key = lambda d:d[1], reverse = True)
        top_num = 18
        count = 0
        for key, value in sorted_dic:
            if count < top_num:
                segid = str(int(key) - 1)
                userid_pic[k].append(segid)
                count += 1
            else:
                break
    return userid_pic

desc_pattern = '\"desc\":\"[^\"]+'
picurl_pattern = '\"picUrl\":\"[^\"]+'
def get_json():
    userid_dic = dict()
    for line in sys.stdin:
        arr = line.strip().split('\t')
        if len(arr) != 3:
            continue
        userid = arr[0] + arr[1]
        m = re.search(picurl_pattern, arr[2])
        value = ''
        if m is not None:
            value += m.group().split('\"picUrl\":\"')[1]
        else:
            continue
        m = re.search(desc_pattern, arr[2])
        if m is not None:
            value += '#' + m.group().split('\"desc\":\"')[1]
        else:
            continue
        userid_dic.setdefault(userid, [])
        userid_dic[userid].append(value)
    return userid_dic

if __name__ == '__main__':
    userid_pic = get_top_center()
#    userid_json = get_json()
    for k, v in userid_pic.iteritems():
        print k + '\t' + '\t'.join(v)
        '''
        output = k
        for arr in v:
            key = k + arr
            if userid_json.has_key(key):
                output += '\t' + '\t'.join(userid_json[key])
       # print output
'''
