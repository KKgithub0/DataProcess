1. 可以在开发机上在线安装：yum install samba
2. 创建samba账号(用户名必须是linux系统已存在的用户名)：smbpasswd -a xuyikai(开发机上用户名为xuyikai，依个人情况而定)
3. 创建samba-log所使用的目录：mkdir /var/log/samba
4. 启动samba服务：/etc/init.d/smb restart
5. samba配置
    1. 进入samba文件夹：cd etc/samba/
    2. 编辑smb.conf：vim smb.conf
[global]
diplay charset = utf8
unix charset = gbk
dos charset = gbk
workgroup = xuyikai
netbios name = xuyikai
server string = uc
security = user
[xuyikai]
comment = uc
path=/home/xuyikai
create mask = 0664
directory mask = 0775
writable = yes
valid users = xuyikai
browseable = yes
   3. 最后一步是在mac机器上远程连接服务器（输入连接主机的名称），连接成功就可以在mac共享的看到连接的主机。
