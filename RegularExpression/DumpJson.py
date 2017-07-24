# -*- encoding:utf-8 -*-
import sys
import re

if len(sys.argv) != 3:
    print "argument is not completed!"
    exit(1)

query_file = open(sys.argv[1],'r')
json_file = open(sys.argv[2],'r')

query_uniq_map = {}
image_uniq_map = {}

query_map = []
for line in query_file.xreadlines():
    line = line.strip()
    if line == '':
        continue
    arr = line.split(';')
    if arr[0] == 'user_id':
        continue
    query = arr[4]
    winfo = arr[:3]
    winfo.append(arr[5])
    winfo = ','.join(str(i) for i in winfo)
    query_map.append([winfo,query])

query_file.close()

json_map = {}
title_pattern = "\"title\":\"[^\"]+"
desc_pattern = "\"desc\":\"[^\"]+"
desc1_pattern = "\"imageDesc\":\"[^\"]+"
title_url_pattern = "https?://[^(bj)][^\"]+"
url_pattern = "http://bj.+?\""
for line in json_file.xreadlines():
    line = line.strip()
    if line == '':
        continue
    arr = line.split('\t')
    winfo = arr[:4]
    winfo.reverse()
    winfo = ','.join(str(i) for i in winfo)
    json = arr[6].strip('{}')
    new_json = []
    m = re.match(title_pattern, json)
    if m is not None:
        title = m.group()
    else:
        continue
    title = title.strip("\"title\":")
    new_json.append(title)
    m = re.search(desc_pattern, json)
    if m is not None:
        desc = m.group()
        desc = desc.strip("\"desc\":")
        new_json.append(desc)
    else:
        m = re.search(desc1_pattern, json)
        if m is not None:
            desc = m.group()
            desc = desc.strip("\"imageDesc\":")
            new_json.append(desc)
        else:
            continue


    m = re.search(title_url_pattern, json)
    if m is not None:
        new_json.insert(1,m.group())
    else:
        continue
    m = re.findall(url_pattern, json)
    try:
        for url in m:
            url = url.strip("\"")
            new_json.append(url)
        json_map[winfo] = new_json
    except:
        pass

json_file.close()

count = 0
TITLE = "query,title,title_url,desc,img_url1,img_url2,img_url3,img_url4,img_url5".split(',')
print '\t'.join(str(i) for i in TITLE)
for ele in query_map:
    if ele[0] in json_map:
        if ele[1] in query_uniq_map.keys() or json_map[ele[0]][3] in image_uniq_map:
            continue
        if count < 300:
            query_uniq_map[ele[1]] = ''
            image_uniq_map[json_map[ele[0]][3]] = ''
            print str(ele[1]).decode('gbk').encode('utf-8') + '\t' + '\t'.join(str(i) for i in json_map[ele[0]])
            count += 1
        else :
            break
