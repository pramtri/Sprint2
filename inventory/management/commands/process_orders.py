from django.core.management.base import BaseCommand
from inventory.models import Order
import pika
import json
import time
import os

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'localhost')

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials('provesi_user', 'isis2503')
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials, heartbeat=600)
    )

class Command(BaseCommand):
    help = "Starts a worker to process packaging orders from RabbitMQ"

    def handle(self, *args, **options):
        self.stdout.write("Starting order processing worker...")
        
        while True:
            try:
                connection = get_rabbitmq_connection()
                channel = connection.channel()

                channel.exchange_declare(exchange='orders_exchange', exchange_type='topic')
                
                # Declarar una cola exclusiva para este worker
                result = channel.queue_declare(queue='', exclusive=True)
                queue_name = result.method.queue

                # Vincular la cola al exchange para recibir mensajes de 'order.pack'
                channel.queue_bind(exchange='orders_exchange', queue=queue_name, routing_key='order.pack')

                def callback(ch, method, properties, body):
                    message = json.loads(body)
                    order_id = message.get('order_id')
                    self.stdout.write(f"Received order to pack: {order_id}")
                    
                    try:
                        order = Order.objects.get(order_id=order_id, status='verified')
                        order.status = 'packed'
                        order.save()
                        self.stdout.write(self.style.SUCCESS(f"Successfully updated order {order_id} to 'packed'"))
                    except Order.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"Order {order_id} not found or already processed."))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Error processing order {order_id}: {e}"))
                    
                    ch.basic_ack(delivery_tag=method.delivery_tag)

                channel.basic_consume(queue=queue_name, on_message_callback=callback)
                
                self.stdout.write("Worker is waiting for messages. To exit press CTRL+C")
                channel.start_consuming()

            except pika.exceptions.AMQPConnectionError as e:
                self.stdout.write(self.style.ERROR(f"Connection failed: {e}. Retrying in 5 seconds..."))
                time.sleep(5)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}. Restarting..."))
                time.sleep(5)