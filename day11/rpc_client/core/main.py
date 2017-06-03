#Auther: Xiaoliuer Li



from modules.client import Client
import random,time
import threading

#rabbitmq服务地址ip
RabbitMQ_IP = 'localhost'

class Handler(object):
    def __init__(self):
        self.information = {}   # 后台进程信息

    def check_all(self,*args):
        '''查看所有task_id信息'''
        time.sleep(2)
        for key in self.information:
            print("TASK_ID【%s】\tHOST【%s】\tCOMMAND【%s】"%(key,self.information[key][0],
                                                                    self.information[key][1]))

    def check_task(self,user_cmd):
        '''查看task_id执行结果'''
        time.sleep(2)
        try:
            task_id = user_cmd.split()[1]
            task_id = int(task_id)
            callback_queue=self.information[task_id][2]
            callback_id=self.information[task_id][3]
            client = Client()
            response = client.get_response(callback_queue, callback_id)
            print(response.decode())
            del self.information[task_id]

        except KeyError  as e :
            print("\33[31;0mWrong id[%s]\33[0m"%e)
        except IndexError as e:
            print("\33[31;0mWrong id[%s]\33[0m"%e)

    def run(self,user_cmd):
        '''执行命令'''
        try:
            time.sleep(2)
            #print("--->>",user_cmd)
            command = user_cmd.split("\"")[1]
            hosts = user_cmd.split()[3:]
            for host in hosts:
                task_id = random.randint(10000, 99999)
                client = Client()
                response = client.call(host, command)
                # print(response)
                self.information[task_id] = [host, command, response[0],response[1]]
        except IndexError as e:
            print("\33[31;0mError：%s\33[0m"%e)

    def reflect(self,str,user_cmd):
        '''反射'''
        if hasattr(self, str):
            getattr(self, str)(user_cmd)
        # else:
        #     setattr(self, str, self.foo)
        #     getattr(self, str)()

    def start(self):
        while True:
            user_cmd = input("->>").strip()
            if not user_cmd:continue
            str = user_cmd.split()[0]
            t1 = threading.Thread(target=self.reflect,args=(str,user_cmd))  #多线程
            t1.start()

if __name__ == '__main__':
    obj = Handler()
    obj.start()
