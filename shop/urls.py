from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
   path( '',views.IndexView.as_view(),name='index'),
   path('products',views.product_list_view,name='products_list'),
   path('product/<str:name>',views.product_detail_view,name='product_details'),
   path('category/<str:category>',views.category_view,name='category'),
   path('profile/',views.user_profile_view,name='profile'),
   path('register',views.register_new_customer,name='register')
   
    
]
