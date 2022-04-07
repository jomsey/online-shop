from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib.auth import login,authenticate

from shop.forms import RegisterNewCustomer
from shop.models import Product,Category,Customer,Cart


class IndexView(TemplateView):
    template_name = 'shop/index.html'
    
def product_list_view(request):
    """retrieves all products"""
    template = 'shop/product_list.html'
    queryset = Product.objects.all()

    #paginate the products list
    paginator = Paginator(queryset,4,orphans=2)
    page_number = 1
    paginated_products = paginator.page(page_number)

    context  ={
        'products':paginated_products
    }
    return render(request,template,context)
 
def product_detail_view(request,name):
    """
    handles the details of a single product 
    """
    queryset = get_object_or_404(Product,name=name)
    product_reviews = queryset.product_review_set.all()

    template = 'shop/product_detail.html'

    context  ={
        'product':queryset,
        'reviews':product_reviews
    }
    return render(request,template,context)

def category_view(request,category):
    """
    handles products which belong to the same category
    e.g Fashion , Electronics
    """
    queryset = Category.objects.get(name=category)
    products = queryset.product_set.all()
    template = 'shop/category_list.html'
    context  ={
        'products':products
    }
    return render(request,template,context)

def user_profile_view(request):
    # customer = Customer.objects.get(profile=request.user)
    # cart = customer.cart
    # cart_products = cart.products.all()
    
    context={
    'cart_products':[]

    }
    template='shop/profile.html'
    return render(request,template,context=context)
    
   
def register_new_customer(request):
    message=""
    form = RegisterNewCustomer()
    if request.method == 'POST':
        form = RegisterNewCustomer(request.POST)
        
        if form.is_valid():
            #save and login the customer
            form.save()
            
            #customer data from form for login
            username= request.POST.get('username')
            password =request.POST.get('password1')
            auth_user = authenticate(username=username,password=password)
             
            #create customer profile and the cart
            customer_cart =Cart.objects.create()
            customer_profile = Customer.objects.create(profile= auth_user,cart=customer_cart)
            customer_profile.save()
            
            #immedately login the customer 
            # login(request,auth_user)
            
            message='customer saved' #will django messages
    template='shop/register.html'
    context = {
        'form':form,
        'message':message
        
    }
    return render(request,template,context=context)
    