import sys

def func(sum_line):
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            continue
        if 'sum' in line:
            arr = line.split('   ')
            if len(arr) != 2:
                continue
            sum_line += int(arr[1])
        else:
            arr = line.split('\t')
            if len(arr) != 3:
                continue
            if arr[0] == 'title':
                title_count[int(arr[1])] += int(arr[2])
            elif arr[0] == 'desc1':
                desc1_count[int(arr[1])] += int(arr[2])
            elif arr[0] == 'desc2':
                desc2_count[int(arr[1])] += int(arr[2])
    return sum_line

def init():
    for i in range(1000):
        title_count[i] = 0
        desc1_count[i] = 0
        desc2_count[i] = 0

def print_func():
    if sum_line == 0:
        return
    print 'total_num' + '\t' + str(sum_line)
    print 'encode : utf-8' + '\t' + 'length : byte'
    print 'type\tlength\tline_num\tpercent'
    print '********'
    start = 0
    end = 0
    tmp_v = 0
    for k, v in title_count.iteritems():
        tmp_v += v
        end += 1
        if float(tmp_v) / sum_line >= 0.1:
            print 'title' + '\t' + str(start) + '---' + str(end)  + '\t' + str(tmp_v) + '\t' + str(float('%0.4f' % (float(tmp_v) / sum_line)) * 100) + '%'
            start = end + 1
            tmp_v = 0
    print 'title' + '\t' + str(start) + '---' + str(end)  + '\t' + str(tmp_v) + '\t' + str(float('%0.4f' % (float(tmp_v) / sum_line)) * 100) + '%'

    print '********'
    start = 0
    end = 0
    tmp_v = 0
    for k, v in desc1_count.iteritems():
        tmp_v += v
        end += 1
        if float(tmp_v) / sum_line >= 0.1:
            print 'desc1' + '\t' + str(start) + '---' + str(end)  + '\t' + str(tmp_v) + '\t' + str(float('%0.4f' % (float(tmp_v) / sum_line)) * 100) + '%'
            start = end + 1
            tmp_v = 0
    print 'desc1' + '\t' + str(start) + '---' + str(end)  + '\t' + str(tmp_v) + '\t' + str(float('%0.4f' % (float(tmp_v) / sum_line)) * 100) + '%'

    print '********'
    start = 0
    end = 0
    tmp_v = 0
    for k, v in desc2_count.iteritems():
        tmp_v += v
        end += 1
        if float(tmp_v) / sum_line >= 0.1:
            print 'desc2' + '\t' + str(start) + '---' + str(end)  + '\t' + str(tmp_v) + '\t' + str(float('%0.4f' % (float(tmp_v) / sum_line)) * 100) + '%'
            start = end + 1
            tmp_v = 0
    print 'desc2' + '\t' + str(start) + '---' + str(end)  + '\t' + str(tmp_v) + '\t' + str(float('%0.4f' % (float(tmp_v) / sum_line))* 100) + '%'

if __name__ == '__main__':
    title_count = dict()
    desc1_count = dict()
    desc2_count = dict()
    sum_line = 0
    init()
    sum_line = func(sum_line)
    print_func()
