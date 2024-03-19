
from django.urls import path

from . import views

urlpatterns = [
    path('cats/<int:cat_id>/', views.catg, name='cats_id'),
    path('product/<int:product_id>/', views.show_product, name='product'),
    path('c/<slug:category_slug>/', views.show_category, name='category'),
    path('shop/<int:seller_id>/', views.show_shop, name='shop'),
    path('addprod/', views.addprod, name='addprod'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('cart-add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart-delete/<int:cart_id>/', views.cart_delete, name='cart_delete'),
    path('cart-decr/<int:cart_id>/', views.cart_decr, name='cart_decr'),
    path('cart/', views.show_cart, name='cart'),
    path('cart-decr-index/<int:product_id>/', views.cart_decr_in_index, name='cart_decr_in_index'),
    path('add-fav/<int:product_id>/', views.add_fav, name='add_fav'),
    path('rem-fav/<int:product_id>/', views.rem_fav, name='rem_fav'),
    path('favorites/', views.show_favorites, name='favorites'),
    path('', views.index, name='home'),

]
