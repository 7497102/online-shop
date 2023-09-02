from django.urls import path
from .views import *

urlpatterns = [
    # path('', ProductList.as_view(), name='product_list')
    path('', product_list, name='product_list'),
    path('category/<slug:slug>/', category_page, name='category_detail'),
    path('product/<slug:slug>/', product_detail, name='product_detail'),

    path('logout/', user_logout, name='logout'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),

    path('review_save/<int:product_id>/', save_review, name='save_review'),

    path('cart/', cart, name='cart'),
    path('to_cart/<int:product_id>/<str:action>/', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout')

]
