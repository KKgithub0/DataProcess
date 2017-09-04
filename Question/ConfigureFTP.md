1. 查看FTP状态
    1. netstat -nlp|grep 21 发现端口21未打开
    2. ps aux|grep ftp 没有ftp进程
    3. service proftpd status 提示无该服务
2. root登录
3. yum install proftpd
4. 启动服务：/sbin/service proftpd start
5. 添加启动项，让重启也能生效：echo "service proftpd start" >>/etc/rc.local
配置完成之后使用wget可能出现两个问题：
1. 无法匿名登录
    1. 解决方法：
        1. vi /etc/proftpd.conf
        2. 看到# Enable this with PROFTPD_OPTIONS=-DANONYMOUS_FTP in /etc/sysconfig/proftpd提示后，去响应文件修改配置
        3. 重启服务 service proftpd restart
2. no such file or no such dictionary
    1. 解决方法：
    2. vi /etc/proftpd.conf
    3. 看到# Put the user into /pub right after login
    4.  #   DefaultChdir                /pub
    5. 此行是设置默认匿名登录访问路径 改为 根目录 或者 /home/user
    6. usermod -d /    ftp
    7. chmod 755 /home/user 设置路径权限
        1. 当仍有问题时，遍历每一级目录看是否有权限，并逐级chmod
    8. 重启服务 service proftpd restart
    9. 如果还有问题：
        1. vi /etc/passwd
        2. 找到有ftp的行    ftp:x:14:50:FTP User:/tmp:/sbin/nologin
        3. 将/tmp改为根目录 或者自己的目录
        4. 重启service proftpd restart
