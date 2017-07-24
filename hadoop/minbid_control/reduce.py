#coding=gbk
import sys
import random
import math

sumday = 7
def calc(sumclick, sumcharge):
    if sumclick != 0:
        click = (float)(sumclick)
        charge = (float)(sumcharge)
        cpc = (float)(charge)/click * 1.4 / 100
        if cpc < 1.5:
            return float('%0.2f' % random.uniform(1.5,2))
        else:
            return float('%0.2f' % cpc)
    else:
        return float('%0.2f' % random.uniform(1.5,2))

jingxiu_dic = {} # old jingxiu query minbid # query province_id wise_minbid  pc_minbid
jingxiu_file = open('./jingxiu_minbid.txt','r')
for line in jingxiu_file:
    arr = line.strip().split('\t')
    if len(arr) != 6:
        continue
    query = arr[0]
    pid = int(arr[1])
    if (float)(arr[2]) <= 2.0 and (float)(arr[4]) <= 2.0:
        continue
    if pid == 998:
        continue
    key = query + str(pid)
    jingxiu_dic.setdefault(key, [0,0])
    jingxiu_dic[key][0] = float(arr[2])
    jingxiu_dic[key][1] = float(arr[4])

jingxiu_file.close()

#print len(jingxiu_dic)


last_query = ''
query_info = [[0 for i in range(9)] for i in range(40)] # wise_pv pc_pv wise_show wise_click wise_charge pc_show pc_click pc_charge contain_flag
for line in sys.stdin:
    line = line.strip()
    if line == "":
        continue
    arr = line.split("\t")
    query = arr[0]
    pid = int(arr[2])
    cmatch = arr[1]

    if last_query != query and last_query != '':
        key = 0
        max_wise_minbid = 0
        max_pc_minbid = 0
        sum_wise_pv = 0
        sum_pc_pv = 0
        while (key < 40):
            if query_info[key][8] == 1:
                wise_minbid = calc(query_info[key][3],query_info[key][4])
                pc_minbid = calc(query_info[key][6],query_info[key][7])
                #make sure new minbid's fluctuation cannot beyond 10 percent of old minbid
                dic_key = last_query + str(key)
                if jingxiu_dic.has_key(dic_key):
                    old_wise_minbid = jingxiu_dic[dic_key][0]
#                    print '+++\t' + str(wise_minbid) + '\t' + str(old_wise_minbid)
                    if wise_minbid > old_wise_minbid:
                        wise_minbid = min(wise_minbid,float('%0.2f' % (old_wise_minbid * 1.05)))
                    else:
                        wise_minbid = max(wise_minbid,float('%0.2f' % (old_wise_minbid * 0.95)))
                    old_pc_minbid = jingxiu_dic[dic_key][1]
#                    print '+++\t' + str(pc_minbid) + '\t' + str(old_pc_minbid)
                    if pc_minbid > old_pc_minbid:
                        pc_minbid = min(pc_minbid,float('%0.2f' % (old_pc_minbid * 1.05)))
                    else:
                        pc_minbid = max(pc_minbid,float('%0.2f' % (old_pc_minbid * 0.95)))

                wise_epv = (float)(query_info[key][0])/sumday
                pc_epv = (float)(query_info[key][1])/sumday
                wise_pv = str(int(math.ceil(wise_epv)))
                pc_pv = str(int(math.ceil(pc_epv)))
                if wise_minbid > max_wise_minbid:
                    max_wise_minbid = wise_minbid
                if pc_minbid > max_pc_minbid:
                    max_pc_minbid = pc_minbid
                sum_wise_pv += query_info[key][0]
                sum_pc_pv += query_info[key][1]
                print last_query + '\t' + str(key) +'\t' + str(wise_minbid) + '\t' + wise_pv + '\t' + str(pc_minbid) + '\t' + pc_pv
            query_info[key] = [0 for i in range(9)]
            key = key + 1
        print last_query + '\t' + '998' + '\t' + str(max_wise_minbid) + '\t' + str(int(math.ceil(float('%0.2f' % (float(sum_wise_pv)/sumday))))) + '\t' + str(max_pc_minbid) + '\t' + str(int(math.ceil(float('%0.2f' % (float(sum_pc_pv)/sumday)))))


    last_query = query
    if len(arr) == 6:
        show = int(arr[3])
        click = int(arr[4])
        charge = int(arr[5])
        query_info[pid][8] = 1
        if cmatch in ['222','223']:
            query_info[pid][2] += show
            query_info[pid][3] += click
            query_info[pid][4] += charge
        if cmatch in ['225','204']:
            query_info[pid][5] += show
            query_info[pid][6] += click
            query_info[pid][7] += charge
    if len(arr) == 4:
        query_info[pid][8] = 1
        if cmatch in ['222','223']:
            query_info[pid][0] += int(arr[3])
        if cmatch in ['225']:
            query_info[pid][1] += int(arr[3])


key = 0
max_wise_minbid = 0
max_pc_minbid = 0
sum_wise_pv = 0
sum_pc_pv = 0
while (key < 40):
    if query_info[key][8] == 1:
        wise_minbid = calc(query_info[key][3],query_info[key][4])
        pc_minbid = calc(query_info[key][6],query_info[key][7])
        #make sure new minbid's fluctuation cannot beyond 10 percent of old minbid
        dic_key = last_query + str(key)
        if jingxiu_dic.has_key(dic_key):
            old_wise_minbid = jingxiu_dic[dic_key][0]
            if wise_minbid > old_wise_minbid:
                wise_minbid = min(wise_minbid,float('%0.2f' % (old_wise_minbid * 1.05)))
            else:
                wise_minbid = min(wise_minbid,float('%0.2f' % (old_wise_minbid * 0.95)))
            old_pc_minbid = jingxiu_dic[dic_key][1]
            if pc_minbid > old_pc_minbid:
                pc_minbid = min(pc_minbid,float('%0.2f' % (old_pc_minbid * 1.05)))
            else:
                pc_minbid = min(pc_minbid,float('%0.2f' % (old_pc_minbid * 0.95)))

        wise_epv = (float)(query_info[key][0])/sumday
        pc_epv = (float)(query_info[key][1])/sumday
        wise_pv = str(int(math.ceil(wise_epv)))
        pc_pv = str(int(math.ceil(pc_epv)))
        if wise_minbid > max_wise_minbid:
            max_wise_minbid = wise_minbid
        if pc_minbid > max_pc_minbid:
            max_pc_minbid = pc_minbid
        sum_wise_pv += query_info[key][0]
        sum_pc_pv += query_info[key][1]
        print last_query + '\t' + str(key) +'\t' + str(wise_minbid) + '\t' + wise_pv + '\t' + str(pc_minbid) + '\t' + pc_pv
    query_info[key] = [0 for i in range(9)]
    key = key + 1
print last_query + '\t' + '998' + '\t' + str(max_wise_minbid) + '\t' + str(int(math.ceil(float('%0.2f' % (float(sum_wise_pv)/sumday))))) + '\t' + str(max_pc_minbid) + '\t' + str(int(math.ceil(float('%0.2f' % (float(sum_pc_pv)/sumday)))))
