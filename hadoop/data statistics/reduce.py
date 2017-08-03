#coding = utf-8
from urllib import unquote
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def init():
    for count in range(1000):
        title_dic[count] = 0
        desc1_dic[count] = 0
        desc2_dic[count] = 0

def calc(count_sum):
    for line in sys.stdin:
#        line = line.decode('utf-8','ignore').encode('gbk','ignore')
        arr = line.strip().split('\t')
        if len(arr) != 3 and len(arr) != 2:
            continue
        if len(arr) == 3:
            title_dic[len(unquote(arr[0]))] += 1
            desc1_dic[len(unquote(arr[1]))] += 1
            desc2_dic[len(unquote(arr[2]))] += 1
        else:
            title_dic[len(unquote(arr[0]))] += 1
            desc1_dic[len(unquote(arr[1]))] += 1
            desc2_dic[0] += 1
        count_sum += 1
    return count_sum

def print_res(count_sum):
    if count_sum == 0:
        return
    print "sum =   " +  str(count_sum)
    for k, v in title_dic.iteritems():
        print "title" + '\t' + str(k) + '\t' + str(v) # + '\t' + str(float('%0.4f' % (float(v) / count_sum)))
    for k, v in desc1_dic.iteritems():
        print "desc1" + '\t' + str(k) + '\t' + str(v) #+ '\t' + str(float('%0.4f' % ((float)(v) / count_sum)))
    for k, v in desc2_dic.iteritems():
        print "desc2" + '\t' + str(k) + '\t' + str(v) #+ '\t' + str(float('%0.4f' % ((float)(v) / count_sum)))

if __name__ == '__main__':
    title_dic = {}
    desc1_dic = {}
    desc2_dic = {}
    count_sum = 0
    init()
    count_sum = calc(count_sum)
    print_res(count_sum)
