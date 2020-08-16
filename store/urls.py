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
    path('orders_history/', views.orders_history, name="orders_history"),
    path('update_status/', views.update_status, name="update_status"),
    path('product_create/', views.product_create, name="product_create"),
    path('update_product/<int:product_id>/', views.update_product, name="update_product"),
    path('delete_product/<int:product_id>/', views.delete_product, name="delete_product"),
    path('update_category/<int:category_id>/', views.update_category, name="update_category"),
    path('add_category/', views.add_category, name="add_category"),
]