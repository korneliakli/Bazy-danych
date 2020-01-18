from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.make_order, name="make-order"),
    path('add_order_details/<int:order_id>/', views.add_order_details,name="add-order-details"),
    path('<int:pk>/', views.order_detail.as_view(), name='order-detail'),
    path('show_orders/', views.OrderList.as_view(), name="show-orders"),
]