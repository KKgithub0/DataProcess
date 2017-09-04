error: bogus escape (end of line)
patter中以一个backslash结尾 将出现此错误 
解决方案：在 pattern前加 r
详解：1. 将子串改为Unicode，pattern前面加u     2. 用下面的raw_string将pattern改写
def raw_string(s):
    if isinstance(s, str):
        s = s.encode('string-escape’)
    elif isinstance(s, unicode):
        s = s.encode('unicode-escape’)
    return s

[ERROR - 2017-07-30T03:28:31.552Z] RouterReqHand - _handle.error
phantomjs://platform/console++.js:263 in error
  9 [ERROR - 2017-07-30T03:28:39.451Z] Session [29265c60-74d7-11e7-b020-4749d30d30a4] - page.onError - msg: TypeError: undefined is not a function (evaluating 'u(e)’)
[INFO  - 2017-07-30T03:33:30.646Z] SessionManagerReqHand - _cleanupWindowlessSessions - Asynchronous Sessions clean-up phase starting NOW

 RouterReqHand - _handle.error - {"name":"Missing Command Parameter","message":"{\"headers\":{\"Accept\":\"application/json\",\"Accept-Encod    ing\":\"identity\",\"Connection\":\"close\",\"Content-Length\":\"71\",\"Cont
