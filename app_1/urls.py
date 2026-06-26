from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    # New Cart Routes
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/clear/', views.clear_cart, name='clear_cart'),
    
    # New Builder Route!
    path('builder/', views.builder_view, name='builder_view'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('support/', views.support_view, name='support_view'),
    path('cart/remove/<int:product_id>/', views.remove_cart_item_view, name='remove_cart_item_view'),

]
