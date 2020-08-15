from django.urls import path
from store import views

app_name = "store"
urlpatterns = [
    path('store/', views.home, name="home"),
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/<int:order_id>/', views.checkout, name="checkout"),
    path('update_item/', views.update_item, name="update_item"),
    path('add_address/', views.add_address, name="add_address"),
    path('orders/', views.orders, name="orders"),
    path('orders_status/', views.orders_status, name="orders_status"),
    # path('orders_status/<int:order_item_id>/', views.orders_status, name="orders_status"),
    path('orders_approved/', views.orders_approved, name="orders_approved"),
    path('update_status/', views.update_status, name="update_status")
]