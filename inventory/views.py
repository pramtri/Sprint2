from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from .models import Product

@require_GET
def health_check(request):
    return JsonResponse({"status": "ok"})

@require_GET
def availability(request):
    sku = request.GET.get("sku")
    if not sku:
        return HttpResponseBadRequest("missing sku")
    p = Product.objects.only("sku","stock","location","warehouse_id").select_related("warehouse").filter(sku=sku).first()
    if not p:
        return JsonResponse({"sku": sku, "available": False, "stock": 0}, status=404)
    return JsonResponse({
        "sku": p.sku,
        "available": p.stock > 0,
        "stock": p.stock,
        "location": p.location,
        "warehouse": p.warehouse.code
    })
