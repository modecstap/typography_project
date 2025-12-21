from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path('', index_page, name='index'),
    path('about/', about_page, name='about'),
    path('cabinet/', cabinet_page, name='cabinet'),
    path('logout/', logout_view, name='logout'),
    path("catalog/", catalog_page, name="catalog"),
    path("product/<slug:slug>/", product_page, name="product"),
    path("order/create/<int:product_id>/", create_order, name="create_order"),
    path("reviews/add/<int:item_id>/", add_review, name="add_review"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
