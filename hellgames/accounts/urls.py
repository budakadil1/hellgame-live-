from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.index, name='index'),
    path('categories/<slug:slug>', views.game_category_list, name='game_category_list'),
    path('product/<slug:slug>', views.product_view, name='game_product_view'),
    path('games/<slug:slug>/', views.category_detail, name='game_category'),
    path('addlisting/', views.add_listing, name='add_listing'),
    path('mylistings/', views.my_listings, name='mylistings'),
    path('editlisting/<slug:slug>', views.edit_listing, name='editlisting'),
    path('deletelisting/<slug:slug>', views.delete_listing, name='deletelisting'),
    # addlisting without slug with addlisting/. Add to somewhere else in the site if required.
]

