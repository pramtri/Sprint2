from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
import pika
import json

# --- Conexión a RabbitMQ (configúrala con las IPs de tus instancias) ---
RABBITMQ_HOST = 'PRIVATE_IP_OF_BROKER_INSTANCE' # Reemplazar después

def get_rabbitmq_connection():
    credentials = pika.PlainCredentials('provesi_user', 'isis2503')
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, credentials=credentials)
    )

@require_GET
def health_check(request):
    return JsonResponse({"status": "ok"})

# --- NUEVA VISTA (PUBLICADOR) ---
@csrf_exempt
@require_POST
def request_packaging(request):
    try:
        data = json.loads(request.body)
        order_id = data.get("order_id")
        if not order_id:
            return HttpResponseBadRequest("Missing order_id")

        connection = get_rabbitmq_connection()
        channel = connection.channel()

        # Declarar el exchange (si no existe, se crea)
        channel.exchange_declare(exchange='orders_exchange', exchange_type='topic')

        # Publicar el mensaje
        routing_key = 'order.pack'
        message = json.dumps({'order_id': order_id})
        channel.basic_publish(
            exchange='orders_exchange',
            routing_key=routing_key,
            body=message
        )
        connection.close()

        return JsonResponse({"status": "packaging request received", "order_id": order_id})

    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        # En un sistema real, aquí habría un manejo de errores más robusto
        return JsonResponse({"status": "error", "message": str(e)}, status=500)