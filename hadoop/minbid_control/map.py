import sys
for line in sys.stdin:
    line = line.strip()
    if line == '':
        continue
    arr = line.split("\001")
    if len(arr) == 4:
        query = arr[1].decode('utf-8','ignore').encode('gbk','ignore')
        arr[1] = query
    tmp = arr[0]
    arr[0] = arr[1]
    arr[1] = tmp
    print "\t".join(arr)
