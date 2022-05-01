from django.contrib import messages
from django.contrib.auth import (login,
                                 authenticate,logout)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,PageNotAnInteger
from django.http import  HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User,Group
from django.db.models import Q
from django.shortcuts import(render,
                             get_object_or_404,
                             redirect
                             )

from shop.utils import( cart_items_number,
                       get_all_categories,
                       cart_overall_price_total,
                       get_recently_viewed_product,
                       get_cart)

from shop.models import (Product,
                         Category,
                         Customer,
                         Cart,
                         ProductInstance
                         ,Category,
                         Order, Promotion)


    
def index_view(request):
  
    template = 'shop/index.html'
    categories = get_all_categories(request)
    cart_items = cart_items_number(request)
    promotions = Promotion.objects.prefetch_related('products').all()
    
    recent=get_recently_viewed_product(request)

    context = {'categories':categories,
               'promotions':promotions,
               'cart_number':cart_items,
               'recent':recent
               }
    return render(request,template,context)
    
  
def product_list_view(request):
    """retrieves all products"""

    template = 'shop/product_list.html'
    queryset = Product.objects.select_related('category').all()
    
    #paginate the products list
    paginator = Paginator(list(queryset),8)
    
    try:
        page_number = request.GET.get('page')
        paginated_products = paginator.page(page_number)
    
        
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
        
   
    cart_items = cart_items_number(request)

    context  ={
        'page_obj':paginated_products,
        'total_pages':paginator.num_pages,
        'cart_number':cart_items,
       
    }
    return render(request,template,context)
 
def product_detail_view(request,name):
    """
    handles the details of a single product 
    """
    # recent_products=get_recently_viewed_product(request)
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
        'page_obj':products
    }
    return render(request,template,context)

#accessed by only authenticated users
@login_required(login_url='login')
def user_profile_view(request):
    customer = Customer.objects.get(profile=request.user)
    cart = get_cart(request)
    cart_products = cart.products.all()
    cart_items_total =cart_items_number(request)
    
    context={
    'cart_products':cart_products,
    'cart_number':cart_items_total,
    'user':customer

    }
    template='shop/profile.html'
    return render(request,template,context)
    
   
def register_new_customer(request):
   
    current_user=request.user
    if current_user.is_authenticated:
        return redirect('profile')
    
    else:
        if request.method == 'POST':
            username= request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password1 =request.POST.get('password1')
            password2 =request.POST.get('password2')
           
            if password1 == password2:
                user = User(username =username,last_name=last_name,first_name=first_name,email=email)
                user.save()
                #add user to the customer group->created the group in the admin panel
                group=Group.objects.get(name='customers')
                group.user_set.add(user)
                group.save()
                #create user profile and the cart
                customer_cart = get_cart(request)
                customer_profile = Customer.objects.create(profile=user,cart=customer_cart,phone_number = phone)
                customer_profile.save()
                messages.success(request,"Account created successfully")
                #immediately login the customer 
                login(request,user)
                
            else:
                messages.error(request,'Account not created make sure , you enter valid input ')
                
                
               
    template='shop/register.html'
    context = {
        
    }
    return render(request,template,context=context)

def login_view(request):
    template = 'shop/login.html'
    error = ''
    cart_items_total = cart_items_number(request)
    current_user=request.user
    if current_user.is_authenticated:
        return redirect('profile')
     
    if request.POST:
            username= request.POST['username']
            password =request.POST['password']
            cart_number=cart_items_number(request)
            
            #authenticate and login user/customer
            user = authenticate(request,username=username,password=password)

            if user:
                login(request,user)
                return redirect('profile') #redirect to profile jst for testing
            else:
                error = "Invalid data entered,please check your username or password"
            
    context = {'error':error,
               'cart_number':cart_items_total}

    return render(request,template,context)

def logout_view(request):
    logout(request)
    return redirect('index')

def add_to_cart_view(request,name):
    template = 'shop/login.html'
    product = get_object_or_404(Product,name=name)
    product_instance = ProductInstance.objects.create(product=product)#create the instance of the product to be added to the cart
    cart = get_cart(request)
    cart.products.add(product_instance)#add new product to the cart
    cart.save()
    messages.success(request,f"{name} added to the cart")
    return HttpResponseRedirect(reverse('cart'))
    

def remove_from_cart_view(request,product_uuid):
    product_instance = get_object_or_404(ProductInstance,product_uuid=product_uuid)#product instance to be removed from the cart
    cart = get_cart(request)
    cart.products.remove(product_instance) #remove the product from the cart
    cart.save()
    messages.success(request,f"{product_instance.product.name} has been removed from the cart")
    return HttpResponseRedirect(reverse('cart'))

def increase_product_quantity(request,product_uuid):
     product= get_object_or_404(ProductInstance,product_uuid=product_uuid)
     product.product_count+=1
     product.save()
     messages.success(request,'Product Added')
     return HttpResponseRedirect(reverse('cart'))
 
def decrease_product_quantity(request,product_uuid):
     product= get_object_or_404(ProductInstance,product_uuid=product_uuid)
     if product.product_count > 1:
         product.product_count-=1
         product.save()
         messages.success(request,'Product removed')
     return HttpResponseRedirect(reverse('cart'))

def cart_view(request):
    template = 'shop/cart.html'
    cart = get_cart(request)
    cart_products = cart.products.select_related('product').all()
    cart_items_total = cart_items_number(request)
    total_price=cart_overall_price_total(request)
    
    print(total_price)
    # recent=get_recently_viewed_product(request)
    
  
    context={
    'cart_products':cart_products,
    'cart_number':cart_items_total,
    'total':total_price,
    # 'recent':recent,

    }
    
    return render(request,template,context)
    
def search_products_view(request):
    queryset =  Product.objects.all()
    search_query = request.GET.get('q')
    cart_items = cart_items_number(request)
    template = 'shop/search.html'
    
    if search_query:
        queryset = Product.objects.select_related('category').filter(Q(name__icontains=search_query) | Q(category__name__icontains=search_query))
    
    context ={
        'page_obj':queryset,
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
@login_required(login_url='login')
def orders_view(request):
    template ='shop/orders.html'
    customer = Customer.objects.get(profile=request.user)
    orders = customer.order_set.select_related('order_cart').all()
    return render(request,template,{'orders':orders})

@login_required(login_url='login')
def delete_order(request,order_id):
    order = Order.objects.get(order_id=order_id)
    order.delete()
    return HttpResponseRedirect(reverse('orders'))
    
    