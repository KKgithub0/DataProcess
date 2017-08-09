import sys
import heapq
import Queue
#get test dictionary
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
        
#using PriorityQueue        
def sort_dic_by_priority_queue():
    queue = Queue.PriorityQueue()
    for k, v in dic.iteritems():
        queue.put((int)v, k)
    count = 0
    while count < 10 and not queue.empty():
        print queue.get()
        
#using K to limit the size of heap   
#to get topK of smallest by restore the value by -value
#get topK of largest
def sort_dic_by_heapq_topK():
    heap = []
    dic = get_dic('./word_pv.txt')
    # put all element into heapq or use count to limit its size
    for k, v in dic.iteritems():
        if len(heap) <= 10:
            heapq.heappush(heap, (int(v), k))
        else:
            if (int(v) > heap[0][0]):
                heapq.heapreplace(heap, (int(v), k))
    for item in heap:
        print str(item[1]) + '\t' + str(item[0])  
        
#we can also use class defined by yourself to define the compare function
#reference: http://blog.csdn.net/liu2012huan/article/details/53264162
#looking for source code of heapq
#def cmp_lt(x, y):
# Use __lt__ if available; otherwise, try __le__.
# In Py3.x, only __lt__ will be called.
#    return (x < y) if hasattr(x, '__lt__') else (not y <= x)
class Skill(object):
    def __init__(self,priority,description):
        self.priority = priority
        self.description = description
    def __lt__(self,other):#operator < 
        return self.priority < other.priority
    def __ge__(self,other):#oprator >=
        return self.priority >= other.priority
    def __le__(self,other):#oprator <=
        return self.priority <= other.priority
    def __cmp__(self,other):
    #call global(builtin) function cmp for int
        return cmp(self.priority,other.priority)
    def __str__(self):
        return '(' + str(self.priority)+',\'' + self.description + '\')'

def heapq_class():
    heap  = []
    heapq.heappush(heap,Skill(5,'proficient'))
    heapq.heappush(heap,Skill(10,'expert'))
    heapq.heappush(heap,Skill(1,'novice'))
    while heap:
        print heapq.heappop(heap),
    print 
    
#the same use of prioriry queue
if __name__ == '__main__':
    sort_dic_by_heapq()
