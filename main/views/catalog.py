from django.shortcuts import render
from django.db.models import Prefetch

from main.models import Product, Review


def catalog_page(request):
    products = (
        Product.objects
        .filter(is_active=True)
        .select_related("category")
        .prefetch_related("images")
    )

    return render(request, "catalog.html", {
        "products": products
    })


def product_page(request, slug: str):
    product = (
        Product.objects
        .prefetch_related(
            Prefetch(
                "orderitem_set__review",
                queryset=Review.objects.select_related("author")
            )
        )
        .get(slug=slug)
    )

    return render(request, "product.html", {
        "product": product
    })

