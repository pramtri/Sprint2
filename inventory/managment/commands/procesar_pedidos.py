# pedidos/management/commands/procesar_pedidos.py
from django.core.management.base import BaseCommand
from inventory.models import Pedido
import pika
import time

# IP privada de tu broker-instance
RABBITMQ_HOST = 'tu-ip-privada-de-broker-instance'

class Command(BaseCommand):
    help = 'Procesa pedidos desde la cola de mensajes de RabbitMQ'

    def handle(self, *args, **options):
        credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials))
        channel = connection.channel()

        channel.queue_declare(queue='cola_pedidos')

        def callback(ch, method, properties, body):
            pedido_id = int(body.decode())
            try:
                pedido = Pedido.objects.get(id=pedido_id)
                # Simula el tiempo de empaque
                time.sleep(1) 
                pedido.estado = 'empacado'
                pedido.save()
                self.stdout.write(self.style.SUCCESS(f'Pedido {pedido.id} actualizado a "empacado por despachar"'))
            except Pedido.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Pedido con ID {pedido_id} no encontrado.'))

        channel.basic_consume(queue='cola_pedidos', on_message_callback=callback, auto_ack=True)
        self.stdout.write(' [*] Esperando pedidos. Para salir presiona CTRL+C')
        channel.start_consuming()