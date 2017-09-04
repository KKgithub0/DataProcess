处理文件格式为gbk或者utf-8的字串时，有时候会出现  图 == 加盟 这种情况，猜测是由于编码格式问题 
解决方法是将字串decode为Unicode编码，之后再进行匹配

'ascii' codec can't encode characters in position 8-50: ordinal not in range(128)
Python在安装时，默认的编码是ascii，当程序中出现非ascii编码时，python的处理常常会报这样的错UnicodeDecodeError: 'ascii' codec can't decode byte 0x?? in position 1: ordinal not in range(128)，python没办法处理非ascii编码的，此时需要自己设置将python的默认编码，一般设置为utf8的编码格式。
查询系统默认编码可以在解释器中输入以下命令：
Python代码    
1. >>>sys.getdefaultencoding()  
设置默认编码时使用：
Python代码    
1. >>>sys.setdefaultencoding('utf8')  
 可能会报AttributeError: 'module' object has no attribute 'setdefaultencoding'的错误，执行reload(sys)，在执行以上命令就可以顺利通过。
此时在执行sys.getdefaultencoding()就会发现编码已经被设置为utf8的了，但是在解释器里修改的编码只能保证当次有效，在重启解释器后，会发现，编码又被重置为默认的ascii了，那么有没有办法一次性修改程序或系统的默认编码呢。
 
有2种方法设置python的默认编码：
一个解决的方案在程序中加入以下代码：
Python代码    
1. import sys  
2. reload(sys)  
3. sys.setdefaultencoding('utf8')   
 另一个方案是在python的Lib\site-packages文件夹下新建一个sitecustomize.py，内容为：
Python代码    
1. # encoding=utf8  
2. import sys  
3.   
4. reload(sys)  
5. sys.setdefaultencoding('utf8')   
此时重启python解释器，执行sys.getdefaultencoding()，发现编码已经被设置为utf8的了，多次重启之后，效果相同，这是因为系统在python启动的时候，自行调用该文件，设置系统的默认编码，而不需要每次都手动的加上解决代码，属于一劳永逸的解决方法。
 
另外有一种解决方案是在程序中所有涉及到编码的地方，强制编码为utf8，即添加代码encode("utf8")，这种方法并不推荐使用，因为一旦少写一个地方，将会导致大量的错误报告，我曾经遇到这种情况，错误日志压缩之后尚有70多K，全都是这一个问题，让人有很崩溃的感觉。
1. #coding=gbk
2. # -*- encoding = gbk -*-
3. 三行：
    1. #coding=gbk
    2. import sys  
    3. reload(sys)  
    4. sys.setdefaultencoding(‘gbk')  
                    
    
  

