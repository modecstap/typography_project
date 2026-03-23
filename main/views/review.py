from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from main.forms import ReviewForm
from main.models import OrderItem


@login_required
def add_review(request, item_id):
    item = get_object_or_404(
        OrderItem,
        id=item_id,
        order__user=request.user,
        order__status="delivered",
    )

    if hasattr(item, "review"):
        return redirect("orders")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.order_item = item
            review.author = request.user
            review.save()

    return redirect("cabinet")
