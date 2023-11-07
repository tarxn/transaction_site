from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_order, name='add_order'),
    path('delete/', views.delete_order, name='delete_order'),
    path('', views.home, name='home'),
    # path('', views.order_management, name='home'),
]