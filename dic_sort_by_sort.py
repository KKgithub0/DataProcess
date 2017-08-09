# encoding = gbk
import sys
import csv

TOP_NUM = 1000

wise_show = {}
wise_charge = {}
pc_show = {}
pc_charge = {}

mt_file = open(sys.argv[1],'r')
pv_file = open(sys.argv[2],'r')
wise_output_file = open(sys.argv[3],'w')
pc_output_file = open(sys.argv[4],'w')

wise_writer = csv.writer(wise_output_file)
pc_writer = csv.writer(pc_output_file)

for line in mt_file.xreadlines():
    arr = line.strip().split('\001')
    if len(arr) != 5:
        continue
    query = arr[1]
    show = arr[2]
    click = arr[3]
    charge = arr[4]
    mtlist = arr[0].split('\002')
    for mt in mtlist:
        if mt in ['1', '2']:
            wise_show.setdefault(query,[0,0,0])
#            wise_charge.setdefault(query,0)
            wise_show[query][0] += int(show)
            wise_show[query][1] += int(click)
            wise_show[query][2] += int(charge)
#            wise_charge[query] += int(charge)
            break
        elif mt in ['3', '4']:
            pc_show.setdefault(query,[0,0,0])
#            pc_charge.setdefault(query,0)
            pc_show[query][0] += int(show)
            pc_show[query][1] += int(click)
            pc_show[query][2] += int(charge)
 #           pc_charge[query] += int(charge)
            break
#print 'len :%d' % (len(wise_show) + len(pc_show))
wise_sum_pv = 0
wise_sum_epv = 0
pc_sum_pv = 0
pc_sum_epv = 0

for line in pv_file:
    item = line.strip().split('\t')
    if len(item) != 5:
        continue
    query = item[0]
    wise_pv = int(item[1])
    wise_epv = int(item[2])
    pc_pv = int(item[3])
    pc_epv = int(item[4])
    if wise_show.has_key(query):
        charge = wise_show[query][2]
        show = wise_show[query][0]
#        cpm1 = float('%0.3f' % (float(charge)/float(pv)))*1000
        cpm2 = float('%0.3f' % (float(charge)/float(show)))*1000
        if wise_pv != 0:
            wise_pvr = float('%0.2f' % (float(wise_epv)/wise_pv))
        else:
            wise_pvr = 0
        wise_show[query].append(wise_pv)
        wise_show[query].append(wise_epv)
        wise_show[query].append(wise_pvr)
#            wise_show[query].append(cpm1)
        wise_show[query].append(int(cpm2))
    if query in pc_show:
        charge = pc_show[query][2]
        show = pc_show[query][0]
#       cpm1 = float('%0.3f' % (float(charge)/float(pv)))*1000
        cpm2 = float('%0.3f' % (float(charge)/float(show)))*1000
        if pc_pv != 0.0:
            pc_pvr = float('%0.2f' % (float(pc_epv)/pc_pv))
        else:
            pc_pvr = 0
        pc_show[query].append(pc_pv)
        pc_show[query].append(pc_epv)
        pc_show[query].append(pc_pvr)
#           pc_show[query].append(cpm1)
        pc_show[query].append(int(cpm2))


sort_wise_show = sorted(wise_show.items(), key=lambda d:d[1], reverse = True)
#sort_wise_charge = sorted(wise_charge.items(), key=lambda d:d[1], reverse = True)
sort_pc_show = sorted(pc_show.items(), key=lambda d:d[1], reverse = True)
#sort_pc_charge = sorted(pc_charge.items(), key=lambda d:d[1], reverse = True)

wise_output = [[] for i in range(TOP_NUM)]
pc_output = [[] for i in range(TOP_NUM)]
i = 0
for k,v in sort_wise_show:
    if i < TOP_NUM:
        wise_sum_pv += int(v[3])
        wise_sum_epv += int(v[4])
#        wise_output[i].append(k + ':' + ','.join(str(i) for i in v[3:6]) + ',' + ','.join(str(i) for i in v[:3]) + ',' + ','.join(str(i) for i in v[6:]))
        wise_output[i].append(k)
        for j in range(3,6):
            wise_output[i].append(str(v[j]))
        for j in range(0,3):
            wise_output[i].append(str(v[j]))
        wise_output[i].append(str(v[6]))
        i += 1
    else:
        break
i = 0
for k,v in sort_pc_show:
    if i < TOP_NUM:
        pc_sum_pv += int(v[3])
        pc_sum_epv += int(v[4])
#        pc_output[i].append(k + ':' + ','.join(str(i) for i in v[3:6]) + ',' + ','.join(str(i) for i in v[:3]) + ',' + ','.join(str(i) for i in v[6:]))
#        pc_output[i].append(k + ':' + ','.join(str(i) for i in v))
        pc_output[i].append(k)
        for j in range(3,6):
            pc_output[i].append(str(v[j]))
        for j in range(0,3):
            pc_output[i].append(str(v[j]))
        pc_output[i].append(str(v[6]))
        i += 1
    else:
        break
HEADER = ['query','pv','epv','pvr','show','click','charge','cpm2']
WISE_HEADER = ['total_pv : %s' % str(wise_sum_pv),' total_epv : %s' % str(wise_sum_epv)]
PC_HEADER = ['total_pv : %s' % str(pc_sum_pv),'total_epv : %s' % str(pc_sum_epv)]
#PC_HEADER = ['total_pv : %s','total_epv : %s'] % (str(pc_sum_pv), str(pc_sum_epv))
wise_writer.writerow(WISE_HEADER)
wise_writer.writerow(HEADER)
pc_writer.writerow(PC_HEADER)
pc_writer.writerow(HEADER)
for arr in wise_output:
#    line = ','.join(arr)
    wise_writer.writerow(arr)
for arr in pc_output:
#    line = ','.join(arr)
    pc_writer.writerow(arr)



wise_output_file.close()
pc_output_file.close()
pv_file.close()
mt_file.close()
