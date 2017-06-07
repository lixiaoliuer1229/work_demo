#Auther: Xiaoliuer Li

import socket
import os

def recvfile(filename):
    """文件接收函数"""
    conn.send(filename.encode())
    data =conn.recv(1024)
    size, filename = data.split()
    size = int(size.decode())
    filename = filename.decode()
    print(size,filename)
    file_object = open(os.getcwd()+"\\file\\"+filename, 'wb')
    for i in range(size//1024+1):
         data =conn.recv(1024)
         file_object.write(data)
         print(i)
    file_object.close()
    pass

def sendfile(filename):
    """文件传送函数"""
    re=str(os.path.getsize(os.getcwd()+"\\file\\"+filename))+" "+filename
    conn.send(re.encode())
    file_size=1024
    file_object = open(os.getcwd()+"\\file\\"+filename, 'rb')
    for i in range(os.path.getsize(os.getcwd()+"\\file\\"+filename)//1024+1):
        chunk = file_object.read(file_size)
        conn.send(chunk)
        file_size+=1024
        # print(i)
    file_object.close()
    pass




server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(("localhost",8000))
server.listen(5)
print("start to listen 8000".center(50,"-"))
while True:
    conn,client_addr = server.accept()
    while True:
        try:
            data =conn.recv(1024)
            data = data.decode()

            print("client`s messge",data)
            if "get" in data or "put" in data:
                if data == "get" or data == "put":
                    re=data+">正确命令格式 get+filename or put+filename or ?(help)."
                    conn.send(re.encode())
                    continue
                action, filename = data.split()
                if action == "put":
                    recvfile(filename)
                    continue
                elif action == "get":
                    sendfile(filename)
                    continue
                else:
                    print("Unknown Error!")
                    continue
            elif "ls" == data:
                list = str(os.listdir(os.path.abspath('.\\file')))
                conn.send(list.encode())
                continue
            elif "?" == data:
                re="FTP command is get+filename or put+filename or ls or mls"
                conn.send(re.encode())
                continue
            else:
                re=data+">ftp 语法错误.请输入'?'查询语法."
                conn.send(re.encode())
                continue
        except Exception as e:
            print(e)
            break