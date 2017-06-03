#Auther: Xiaoliuer Li

import pika
import os

class Server(object):
    def __init__(self,rabbitmq,queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmq))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def handle(self,command):
        command = command.decode()
        print(command,type(command))
        message = os.popen(command).read()
        if not message:
            message = "Wrong Command"
        return message

    def on_request(self,ch, method, props, body):
        response = self.handle(body)
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,  # 回信息队列名
                         properties=pika.BasicProperties(correlation_id=
                                                         props.correlation_id),
                         body=str(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        self.channel.basic_consume(self.on_request,
                                   queue=self.queue_name)

        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()


if __name__ == "__main__":
    rabbitmq = "localhost"      #rabbitmq服务器地址
    queue_name = "192.168.20.22"    #queue_name为本地ip地址
    server = Server(rabbitmq,queue_name)
    server.start()