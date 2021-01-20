from django.urls import path, include
from . import views

app_name = 'shoppingcart'
urlpatterns = [
    path('', views.get_cart, name='get_cart'),
    path('add/<slug:slug>', views.add_to_cart, name='add_to_cart'),
    path('remove/<slug:slug>', views.remove_from_cart, name='remove_from_cart'),
]

