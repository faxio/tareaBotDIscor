import wikipedia
import os
import pika

from dotenv import load_dotenv


######################## Conexión ######################
HOST = os.environ['RABBITMQ_HOST']
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=HOST))
channel = connection.channel()

channel.exchange_declare(exchange='cartero', exchange_type='topic', durable=True)
#Cola para la busqueda
result = channel.queue_declare(queue="search", exclusive=True, durable=True)
queue_name = result.method.queue

#La cola se asigna a un 'exchange'
channel.queue_bind(exchange='cartero', queue=queue_name, routing_key="search")
#################################################
def callback(ch, method, properties, body):
    print(body.decode("UTF-8"))
    response = body.decode("UTF-8")
    wikipedia.set_lang("es")
    #url = wikipedia.page(body).url
    response = wikipedia.summary(response,sentences=1)
    channel.basic_publish(exchange='cartero',routing_key="discord_writer",body=response)



channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
