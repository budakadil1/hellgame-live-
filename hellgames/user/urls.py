from django.urls import path, include
from django.contrib import admin
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<slug:user_id>', views.profile, name='browseotherprofile'),
    path('profile/', views.own_profile, name='browseownprofile'),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name='login'),
    path('review/<slug:slug>', views.review, name='review'),
    path('edit_profile/', views.editprofile, name='editprofile'),
    path('logout/', views.userlogout, name="logout"),
    # anyone with access to the link can leave a review - Implement something else with checkout.
]
