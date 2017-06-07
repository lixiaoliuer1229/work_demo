#Auther: Xiaoliuer Li

import socket
import os,shelve
client = socket.socket()
client.connect(("localhost",8000))

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db_Users = base_dir + r"\day8\conf\user_list"
db_user = base_dir + r"\day8\file_client\ "    #文件夹的路径 db_file+name




def Login():
    """用户登录"""
    name = input("请输入你的用户名：")
    if len(name.strip()) > 0:
        password = input("请输入你的密码：")
        user_file = shelve.open(db_Users)
        if name in user_file.keys():
            if str(user_file[name]['password']) == password:
                print("\33[31;0m欢迎你再次登录！\33[0m\n")
                user_file.close()
                Choice(name)
            else:
                print("\33[31;0m你输入的用户名或密码错误，请重试！\33[0m\n")
                Login()
        else:
            print("\33[31;0m你输入的用户名或密码错误，请重试！\33[0m\n")
            Login()
    else:
        print("\33[31;0m输入的用户名为空\33[0m\n")




def Register():
    """注册用户"""
    name = input("请输入你的用户名：")
    if len(name.strip()) > 0:
        password = input("请输入你的密码：")
        if len(password.strip()) > 0:
            Password = input("请再次输入密码：")
            if password == Password:
                user_file =  shelve.open(db_Users)
                if not os.path.exists(db_user+name):
                    user_file[name] = {"username":name,"password":password}
                    user_file.close()
                if os.path.exists(db_user+name):
                     print("用户名重复，请重新输入！")
                     Register()
                os.mkdir(db_user + name)
                print("\33[31;1m创建用户 %s 成功\33[0m\n" % name)
                Choice(name)
            else :
                print ("你的密码两次输入不一致，请重新输入！")
                Register()
        else:
            print("\33[31;0m输入的密码为空\33[0m\n")
    else:
        print("\33[31;0m输入的用户名为空\33[0m\n")





def Main():
    """主菜单函数"""
    while True:
        print('''\n\33[35;1m———登录界面————\33[0m \n
    \33[34;0m1.登录
    2.注册
    q.退出
    \33[0m''')
        choicec = input("请输入你的操作：")
        if choicec == "1":
            Login()
        elif choicec == "2":
            Register()
        elif choicec == "q":
            break
        else:
            print("你的输入有误，请重新输入！")
            continue

def Choice(name):
    """指令操作函数"""
    while True:
        print('''\n\33[35;1m———指令操作界面————\33[0m \n
         \33[34;0m上传文件（put + 文件名）
         下载文件 (get + 文件名)
         查看服务器文件 (ls)
         查看本地文件 (mls)
         \33[0m''')
        msg = input("请输入你想操作的指令").strip()
        if len(msg) == 0:continue
        client.send(msg.encode())
        if "ls" == msg:
            data = client.recv(1024)
            print("ftp`s file:",data.decode())
        elif "mls" == msg:
            data = client.recv(1024)
            print("client`s file: ",str(os.listdir(os.path.abspath(db_user+name+'\\'))))
        elif "get" in msg or "put" in  msg:
            if "get" != msg or "put"!=msg:
                data = client.recv(1024)
            if "get" in msg:
                size, filename = data.split()
                size = int(size.decode())
                filename = filename.decode()
                print("文件大小：",size," 文件名字： ",filename)
                file_object = open(db_user+name+'\\'+filename, 'wb')
                for i in range(size//1024+1):
                    data = client.recv(1024)
                    file_object.write(data)
                file_object.close()
            if "put" in msg:
                filename=data.decode()
                print(filename," 上传至服务器")
                re=str(os.path.getsize(db_user+name+'\\'+filename))+" "+filename
                client.send(re.encode())
                file_size=1024
                file_object = open(db_user+name+'\\'+filename, 'rb')
                for i in range(os.path.getsize(db_user+name+'\\'+filename)//1024+1):
                    chunk = file_object.read(file_size)
                    client.send(chunk)
                    file_size+=1024
                file_object.close()
        else:
            data = client.recv(1024)
            print("server return",data.decode())


Main()