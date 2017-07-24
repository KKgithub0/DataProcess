#!/bin/env python
#encoding=utf-8
import sys
import os
import math
import heapq
import datetime
import traceback
import bisect
import collections

EXT_TITLE_PX = 26
EXT_DESC_PX = 22
EXT_SUBLINK_PX = 18
EXT_1047_SUBLINK = 28

#### 日志打印 ####
WARN = "WARN"
NOTICE = "NOTICE"
FATAL = "FATAL"
logfile = "./py.log"
logfd = open(logfile, 'a')
logid = "%s"%(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))

def writelog(errlevel, info):
    #print("[%s] %s"%(errlevel, info))  # stdout as output of pipe which can be read by C program
    #logfd = open(logfile, "a")
    logfd.write("[%s][%s][%s] %s\n" % (logid, datetime.datetime.now().strftime("%Y%m%d %H:%M:%S"), errlevel, info))
    #fd.close()
    logfd.flush()

def log_warn(msg):
    writelog(WARN, msg)

def log_notice(msg):
    writelog(NOTICE, msg)

def log_fatal(msg):
    writelog(FATAL, msg)

def log_exception(msg):
    writelog(WARN, "%s\nexception:%s"%(msg, str(traceback.format_exc())))


#### 正态分布 ####
def normal_distr(num_vec, count_vec):
    count_sum = sum(count_vec)
    prob_vec = [c*1.0/count_sum for c in count_vec]
    mean_val = sum([x*p for (x,p) in zip(num_vec, prob_vec)])
    variance = sum([x*x*p for (x,p) in zip(num_vec, prob_vec)]) - mean_val*mean_val
    std_var = math.sqrt(variance)
    #confidence(num_vec, count_vec, mean_val, std_var)
    return (mean_val, std_var)

def normal_distr2(occur_dic):
    return normal_distr(occur_dic.keys(), occur_dic.values())

def get_confidence_zone(num_vec, count_vec, mean, std_var, step):
    zone = [mean - step*std_var, mean + step*std_var]
    confidence_occur_dic = {x:p for (x,p) in zip(num_vec, count_vec) if x >= zone[0] and x <= zone[1]}
    return confidence_occur_dic

# @brief: 字典累加计数
def incr_dic_count(d, k, v):
    if k not in d:
        d[k] = 0
    d[k] += v

# @brief: 给定一个值，从一个排序的列表中找到与该值最接近的值
# >>> x = [3, 16, 28, 30, 54, 57]
# >>> near_match(x, 40)
# >>> 30
def near_match(haystack, needle):
    idx = bisect.bisect_left(haystack, needle)
    if idx == 0:
        return haystack[idx]
    elif idx >= len(haystack):
        return haystack[len(haystack) - 1]
    else:
        if abs(haystack[idx] - needle) <= abs(haystack[idx - 1] - needle):
            return haystack[idx]
        else:
            return haystack[idx - 1]

# @brief: 将字典dic输出到文件fn中去
def dumpDict(dic, fn):
    try:
        fd = open(fn, 'w')
        for (k,v) in dic.items():
            fd.write("%s\t%s\n"%(k,v))
        fd.close()
    except:
        log_exception("dump fn: %s error, exception: %s"%(fn, str(traceback.format_exc())))
        return False
    return True

def dumpOrderedDict(dic, fn):
    try:
        fd = open(fn, 'w')
        ordered_dic = collections.OrderedDict(sorted(dic.items()))
        for (k,v) in ordered_dic.iteritems():
            fd.write("%s\t%s\n"%(k,v))
        fd.close()
    except:
        log_exception("dump fn: %s error, exception: %s"%(fn, str(traceback.format_exc())))
        return False
    return True

EPSINON = 1.0 / math.pow(10, 9)
def isFloatZero(f):
    if abs(f) < EPSINON:
        return True
    return False

# 生成随机数
import random
#>>> R=random.sample(xrange(0,100),10)
#>>> R
#[91, 58, 68, 44, 33, 6, 40, 5, 22, 39]

#### 上面的代码是靠谱的 #######
##########################################

def zone_prob(num_vec, count_vec, zone):
    count_sum = sum(count_vec)
    prob_vec = [c*1.0/count_sum for c in count_vec]
    zone_prob_sum = sum([p for (x,p) in zip(num_vec, prob_vec) if x >= zone[0] and x <= zone[1]])
    return zone_prob_sum

def filter_dict(occur_dic, filter_zone):
    #filtered_sample = [(x, c) for (x,c) in zip(num_vec, count_vec) if x >= filter_zone[0] and x <= filter_zone[1]]
    #filtered_sample = zip(*filtered_sample)
    filtered_dic = {k:v for (k,v) in occur_dic if k >= filter_zone[0] and k <= filter_zone[1]}
    return filtered_dic

def confidence(num_vec, count_vec, mean, std_var):
    for step in [1,1.5,2,2.5,3]:
        zone = [mean - step*std_var, mean + step*std_var]
        print "[%.2f, %.2f], zone: [%.1f][%.2f, %.2f], confidence: %.3f"%(
                mean, std_var, step, zone[0], zone[1], zone_prob(num_vec, count_vec, zone))

def incr_dic(d, key, count):
    if key not in d:
        d[key] = 0
    d[key] += count

def load(line, occur_dic, indexNum, indexCount):
    fields = line.split()
    if len(fields) < max(indexNum, indexCount):
        return False
    num = int(fields[indexNum])
    count = int(fields[indexCount])
    incr_dic(occur_dic, num, count)

# PART-A: <cmatch rank filtered_mt_list width height> => <count>
# PART-B: <cmatch rank filtered_mt_list> => <SUM_show> <SUM_clk> <SUM_price>
def load_whole(fd, colNum):
    whole = []
    for line in fd:
        fields = line.strip().split()
        if colNum > 0 and len(fields) != colNum:
            continue
        whole.append(fields)
    return whole

# get the most 10 bin
def get_top_bin(occur_dic, top_num):
    count_sum = sum(occur_dic.values())
    # 将个数转换为概率
    #occur_dic = {k:v*1.0/count_sum for (k,v) in occur_dic.items()}
    top_sample_vec = []
    top_occur_vec = []
    # 取最大的前10个bin
    for key in heapq.nlargest(top_num, occur_dic, key=occur_dic.get):
        #print key, occur_dic[key]
        top_sample_vec.append(key)
        top_occur_vec.append(occur_dic[key])
    #print sum(top_occur_vec)
    return [top_sample_vec, top_occur_vec]
    # 按照occur数对sample进行排序
    zipped = zip(top_sample, top_occur_vec)
    # 取最高的bin,我们假设这个就是未扩高时的广告高度
    zipped = sorted(zipped, key=lambda x:x[1], reverse=True)
    top1Sample = zipped[0][0]
    top1Occr = zipped[0][1]
    # 验证: 未扩高的高度的bin的sample值必须小于其它3个top4的值
    #for i in range(1, 4):
    #    if top1Sample >= zipped[i][0]:
    #        LOG_WARNING("highest bin assumption is valid for zipped: %s"%(zipped))
    #        return []
    #extTitle = top1Sample + EXT_TITLE_PX
    #extDesc = top1Sample + EXT_DESC_PX
    #extSublink = top1Sample + EXT_SUBLINK_PX
    # 验证三种扩高模式均在topN中
    #top4Sample
    return True

############################################
# 分"k1=v1&k2=v2...",返回一个dict
def split_dic(line, delim1, delim2):
    d = {}
    for kvstr in line.split(delim1):
        kv = kvstr.split(delim2)
        if len(kv) != 2:
            continue
        d[kv[0]] = kv[1]
    return d

# 将字符串转换为float
def convert_float(intstr):
    try:
        return float(intstr)
    except:
        return -1

# 将字符串转换为int
def convert_uint(intstr):
    try:
        return int(float(intstr))
    except:
        return -1

# 尝试从dic获取key的value
def try_getkey(dic, key):
    if key in dic:
        return dic[key]
    else:
        return None

# 从一个list里面获取另外一个list相同下标的值
# src=111,615,878,877,830,904,912,942,927,964, res=(3,0,0,0,0,0,0,1,0,0,)
# 例如想要获取数据源830的返回广告数
def try_index_key(list_a, list_b, value_a):
    if len(list_a) != len(list_b):
        return None
    index_a = -1
    try:
        index_a = list_a.index(value_a)
    except:
        index_a = -1
    if index_a < 0:
        return None
    return list_b[index_a]

# 字符串是否为None或空
def check_str(s):
    if s is None or len(s) <= 0:
        return False
    return True
