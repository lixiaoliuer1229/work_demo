﻿#类 Fabric 主机管理程序开发

作者：李昌武
博客地址：
http://www.cnblogs.com/lixiaoliuer/p/6706308.html
---

有感：这次作业写的蛮顺利，一个难题是虚拟机的建立，不知道是为什么电脑的虚拟机上不了网所以连得同学的。其他的方面，完成度还是比较满意的。

功能介绍：
1. 运行程序列出主机组或者主机列表
2. 选择指定主机或主机组
3. 选择让主机或者主机组执行命令或者向其传输文件（上传/下载）
4. 充分使用多线程或多进程
5. 不同主机的用户名密码、端口可以不同

目录结构：
 New_Fabric
    ├── Folder #本地文件
    ├── bin #入口文件
    │   ├── Fabric 
    ├── core #核心代码文件
    │   ├── main #核心代码
    ├── database #远程客户端下载文件

运行说明：

                欢迎来到Fabric主机管理界面
                    1,创建主机
                    2,删除主机
                    3,自动激活所有主机
                    4,开始远程操控
                    5,退出程序
        
请输入你的选择：3

                    警告！程序准备开启多线程模式激活主机，请确保：
                    1，远程服务器处于开启状态
                    2，DNS或本地hosts映射能够解析远程服务器主机名
            
 是否确定开始激活远程主机（y/n）？: y
程序开始自动激活远程主机，请稍后...
主机名：192.168.30.224的主机激活成功！
主机名：192.168.30.223的主机激活失败！失败原因：Authentication failed.
所有主机激活完毕！

                欢迎来到Fabric主机管理界面
                    1,创建主机
                    2,删除主机
                    3,自动激活所有主机
                    4,开始远程操控
                    5,退出程序
        
请输入你的选择：4
已激活主机如下：
1,主机名：192.168.30.224
请输入你想操控的主机的索引（可多选,n=返回上级）：1
正在操控1台主机，如下：
主机名：192.168.30.224
请输入你想执行的命令（输入n=返回上级，输入help获取帮助）：>>pwd
主机：192.168.30.224,执行pwd命令的结果如下：
/root

命令执行完毕！
正在操控1台主机，如下：
主机名：192.168.30.224

测试环境说明：
Windows：
OS:Windows 7 旗舰版
Python:Python 3.6.0
PyCharm版本：PyCharm 2016.1.3