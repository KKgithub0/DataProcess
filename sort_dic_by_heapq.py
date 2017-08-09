import sys
import heapq
import Queue
def get_dic(file):
    dic = dict()
    with open(file, 'r') as f:
        for line in f:
            arr = line.strip().split('\t')
            if len(arr) != 2:
                continue
            dic[arr[0]] = arr[1]

    return dic
#insert dic element as tuple, so we can sort them as value
def sort_dic_by_heapq():
    heap = []
    dic = get_dic('./word_pv.txt')
    # put all element into heapq or use count to limit its size
    for k, v in dic.iteritems():
        heapq.heappush(heap, (int(v), k))
    list = heapq.nlargest(10, heap)
    for item in list:
        print str(item[1]) + '\t' + str(item[0])
        
def sort_dic_by_priority_queue():
    queue = Queue.PriorityQueue()
    for k, v in dic.iteritems():
        queue.put((int)v, k)
    count = 0
    while count < 10 and not queue.empty():
        print queue.get()
        
#we can also use class defined by yourself to redefine the compare function
#detail and reference: http://blog.csdn.net/liu2012huan/article/details/53264162
if __name__ == '__main__':
    sort_dic_by_heapq()
