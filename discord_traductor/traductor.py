import os
import pika

from dotenv import load_dotenv
from googletrans import Translator


######################## Conexión ######################
HOST = os.environ['RABBITMQ_HOST']
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)
#Cola para la busqueda
result = channel.queue_declare(queue="translate", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="translate")


def callback(ch, method, properties, body):   
    response = body.decode("UTF-8")     
    traductor = Translator()
    result = traductor.translate(response,dest="es").text
    channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=result)




channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
