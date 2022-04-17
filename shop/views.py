import re
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,get_object_or_404,redirect

from shop.utils import( cart_items_number,
                       get_all_categories,
                       cart_overall_price_total,
                       get_recently_viewed_product,
                       get_cart)
from shop.forms import RegisterNewCustomer, UserLoginForm
from shop.models import Product,Category,Customer,Cart, ProductInstance,Category,Order



def index_view(request):
    template = 'shop/index.html'
    categories = get_all_categories(request)
    cart_items = cart_items_number(request)
    products = Product.objects.all()[:4]
    recent=get_recently_viewed_product(request)

    context = {'categories':categories,
               'products':products,
               'cart_number':cart_items,
               'recent':recent
               }
    return render(request,template,context)
    
  
def product_list_view(request):
    """retrieves all products"""

    template = 'shop/product_list.html'
    queryset = Product.objects.all()
    
    #paginate the products list
    paginator = Paginator(list(queryset),4,orphans=2)
    page_number = 1
    paginated_products = paginator.page(page_number)

    cart_items = cart_items_number(request)

    context  ={
        'products':queryset,
        'cart_number':cart_items
    }
    return render(request,template,context)
 
def product_detail_view(request,name):
    """
    handles the details of a single product 
    """
    recent_products=get_recently_viewed_product(request)
    queryset = get_object_or_404(Product,name=name)
    request.session['recent'] = name
    product_reviews = queryset.productreview_set.all()
    product_category = queryset.category
    same_category_products= Product.objects.exclude(id=queryset.id).filter(category=product_category) #get products belonging to the same category living out the current product
    cart_items = cart_items_number(request)

    if 'recently_viewed' in request.session:
         recent = request.session['recently_viewed'] #list of recently viewed products
         
         if name in recent:
             recent.remove(name)
             
         recent.insert(0,name)
         if len(recent)>4:
            recent.pop()

    else:
        request.session['recently_viewed']=[name]

    request.session.modified = True
        

    template = 'shop/product_detail.html'

    context  ={
        'product':queryset,
        'reviews':product_reviews,
        'same_category':same_category_products,
        'cart_number':cart_items,
        # 'recent':recent_products
       
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

#accessed by only authenticated users
@login_required(login_url='login')
def user_profile_view(request):
    cart = get_cart(request)
    cart_products = cart.products.all()
    cart_items_total = cart_products.count()
    
    context={
    'cart_products':cart_products,
    'cart_items_total':cart_items_total

    }
    template='shop/profile.html'
    return render(request,template,context={})
    
   
def register_new_customer(request):
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
            
            messages.success(request,"Account created successfully")
            
            #immediately login the customer 
            login(request,auth_user)
               
    template='shop/auth_page.html'
    context = {
        'form':form,
    }
    return render(request,template,context=context)

def login_view(request):
    template = 'shop/auth_page.html'
    login_form = UserLoginForm()

    current_user=request.user

    if current_user.is_authenticated:
        return redirect('profile')
     
    if request.POST:
        if login_form.is_valid():
            login_form = UserLoginForm(request.POST)
            username= login_form.cleaned_data.POST['username']
            password =login_form.cleaned_data.POST['password']
            print(username)

            #authenticate and login user/customer
            user = authenticate(request,username=username,password=password)

            if user:
                login(request,user)
                return redirect('profile') #redirect to profile jst for testing
            messages.error(request,'User Account does not exist')
    context = {'form':login_form}
    
    return render(request,template,context)

def logout_view(request):
    logout(request)
    return redirect('index')

def add_to_cart_view(request,name):
    product = get_object_or_404(Product,name=name)
    product_instance = ProductInstance.objects.create(product=product)#create the instance of the product to be added to the cart
    cart = get_cart(request)
    cart.products.add(product_instance)#add new product to the cart
    cart.save()
    messages.success(request,f"{name} added to the cart")
    return HttpResponseRedirect(reverse('product_details',args=(name,)))
    

def remove_from_cart_view(request,product_uuid):
    product_instance = get_object_or_404(ProductInstance,product_uuid=product_uuid)#product instance to be removed from the cart
    cart = get_cart(request)
    cart.products.remove(product_instance) #remove the product from the cart
    cart.save()
    messages.success(request,f"{product_instance.product.name} has been removed from the cart")
    return HttpResponseRedirect(reverse('cart'))

def cart_view(request):
    template = 'shop/cart.html'
    cart = get_cart(request)
    cart_products = cart.products.all()
    cart_items_total = cart_products.count()
    total_price=cart_overall_price_total(request)
    recent=get_recently_viewed_product(request)
    
    context={
    'cart_products':cart_products,
    'cart_number':cart_items_total,
    'total':total_price,
    'recent':recent,

    }
    
    return render(request,template,context)
    
def search_products_view(request):
    queryset =  Product.objects.all()
    search_query = request.GET.get('q')
    cart_items = cart_items_number(request)
    template = 'shop/search.html'
    
    if search_query:
        queryset = Product.objects.filter(name__icontains=search_query)
    
    context ={
        'products':queryset,
        'cart_number':cart_items,
        'search':search_query
    }
    return render(request,template,context)

@login_required(login_url='login') #proceed to make an order after login
def create_order(request):
    customer = Customer.objects.get(profile=request.user)
    cart = customer.cart #to be submitted for checkout
    cart_items  = cart_items_number(request)
    
    #order should only be processed  when cart is not empty
    if cart_items:
        order = Order.objects.create(customer=customer,order_cart=cart)
        order.save()
        messages.success(request,"Your order has been successfully submitted")
        
    return HttpResponseRedirect(reverse('cart'))
    