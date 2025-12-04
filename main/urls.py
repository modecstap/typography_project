from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index'),
    path('about/', views.about_page, name='about'),
    path('cabinet/', views.cabinet_page, name='cabinet'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('catalog/<int:product_id>/', views.product_page, name='product'),
]
