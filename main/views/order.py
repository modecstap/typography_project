import json
import uuid
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.db import transaction

from main.models import Product, Order, OrderItem


@login_required
@require_POST
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    try:
        data = json.loads(request.body)
        quantity = int(data.get("quantity", 1))
        comment = data.get("comment", "")
    except Exception:
        return JsonResponse({"error": "Неверные данные"}, status=400)

    with transaction.atomic():
        order_number = uuid.uuid4().hex[:12].upper()

        order = Order.objects.create(
            user=request.user,
            order_number=order_number,
            total_amount=product.price * quantity,
            description=comment
        )

        OrderItem.objects.create(
            order=order,
            product=product,
            price=product.price,
            quantity=quantity
        )

    return JsonResponse({"success": True, "order_number": order_number})
