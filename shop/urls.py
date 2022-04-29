import django
from django.urls import path
from . import views

urlpatterns = [
   path( '',views.index_view,name='index'),
   path('products',views.product_list_view,name='products_list'),
   path('product/<str:name>',views.product_detail_view,name='product_details'),
   path('category/<str:category>',views.category_view,name='category'),
   path('profile/',views.user_profile_view,name='profile'),
   path('register',views.register_new_customer,name='register'),
   path('login',views.login_view,name='login'),
   path('logout',views.logout_view,name='logout'),
   path('add_item/<str:name>',views.add_to_cart_view,name='add_to_cart'),
   path('remove_item/<uuid:product_uuid>',views.remove_from_cart_view,name='remove_from_cart'),
   path('search',views.search_products_view,name='search'),
   path('cart',views.cart_view,name='cart'),
   path('increase/<uuid:product_uuid>',views.increase_product_quantity,name='increase'),
   path('decrease/<uuid:product_uuid>',views.decrease_product_quantity,name='decrease'),
   path('orders',views.orders_view,name="orders"),
   path('checkout',views.create_order,name='checkout'),
   path('delete/<uuid:order_id>',views.delete_order,name='delete')
   
]