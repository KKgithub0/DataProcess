#coding=utf-8
import sys
import re

desc_pattern = '\"desc\":\"[^\"]+'
picurl_pattern = '\"picUrl\":\"[^\"]+'

#get needed picture first then others followed
def get_json():
    pic_set = set()
    all_pic_set = set()
    last_uid = ''
    for line in sys.stdin:
        arr = line.strip().split('\t')
        if len(arr) != 3:
            continue
        uid = arr[0]
        #get total 18 pictures
        if last_uid != uid and last_uid != '':
            fit_num = 18 - len(pic_set)
            res = last_uid
            res += '\t' + '\t'.join(pic_set)
            count = 0
            for item in all_pic_set:
                if count < fit_num:
                    res += '\t' + item
                else:
                    break
                count += 1
            print res
            pic_set.clear()
            all_pic_set.clear()

        last_uid = uid
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

        if uid_segmentid.has_key(uid):
            if arr[1] in uid_segmentid[uid]:
                pic_set.add(value)
            else:
                all_pic_set.add(value)

#    print last_uid + '\t' + '\t'.join(pic_set)
    fit_num = 18 - len(pic_set)
    res = last_uid
    res += '\t' + '\t'.join(pic_set)
    count = 0
    for item in all_pic_set:
        if count < fit_num:
            res += '\t' + item
        else:
            break
        count += 1
    print res

#key and values to be found
def get_uid_segmentid():
    uid_segmentid = dict()
    with open('filename' ,'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            if len(arr) < 2:
                continue
            uid = arr[0]
            uid_segmentid.setdefault(uid, [])
            for id in arr[1:]:
                uid_segmentid[arr[0]].append(id)
    return uid_segmentid
if __name__ == '__main__':
    uid_segmentid = get_uid_segmentid()
    get_json()
