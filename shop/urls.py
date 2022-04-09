import django
from django.urls import path
from . import views

urlpatterns = [
   path( '',views.IndexView.as_view(),name='index'),
   path('products',views.product_list_view,name='products_list'),
   path('product/<str:name>',views.product_detail_view,name='product_details'),
   path('category/<str:category>',views.category_view,name='category'),
   path('profile/',views.user_profile_view,name='profile'),
   path('register',views.register_new_customer,name='register'),
   path('login',views.login_view,name='login'),
   path('logout',views.logout_view,name='logout'),
   path('add_item/<str:name>',views.add_to_cart_view,name='add_to_cart'),
    path('remove_item/<uuid:product_uuid>',views.remove_from_cart_view,name='remove_from_cart'),
   path('search',views.search_products_view,name='search')
]