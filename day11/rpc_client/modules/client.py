import pika
import uuid

#rabbitmq服务地址ip
RabbitMQ_IP = 'localhost'

class Client(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=RabbitMQ_IP))
        self.channel = self.connection.channel()

    def on_response(self, ch, method, props, body):
        '''获取命令执行结果的回调函数'''
        # print("验证码核对",self.callback_id,props.correlation_id)
        if self.callback_id == props.correlation_id:  # 验证码核对
            self.response = body
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def get_response(self,callback_queue,callback_id):
        '''取队列里的值，获取callback_queued的执行结果'''
        self.callback_id = callback_id
        self.response = None
        self.channel.basic_consume(self.on_response,  # 只要收到消息就执行on_response
                                   queue=callback_queue)
        while self.response is None:
            self.connection.process_data_events()  # 非阻塞版的start_consuming
        return self.response

    def call(self,queue_name,command):
        '''队列里发送数据'''
        result = self.channel.queue_declare(exclusive=False) #exclusive=False 必须这样写
        self.callback_queue = result.method.queue
        self.corr_id = str(uuid.uuid4())
        # print(self.corr_id)
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,  # 发送返回信息的队列name
                                       correlation_id=self.corr_id,  # 发送uuid 相当于验证码
                                   ),
                                   body=command)

        return self.callback_queue,self.corr_id