from django.urls import path
from store import views

app_name = "store"
urlpatterns = [
    path('store/', views.home, name="home"),
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.update_item, name="update_item")
]