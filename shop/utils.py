from shop.models import Customer,Category

def  cart_items_number(request):
        customer = Customer.objects.get(profile=request.user)
        cart = customer.cart
        cart_products = cart.products.all()
        cart_items_total = cart_products.count()
        
        return cart_items_total

def get_all_categories(request,*args, **kwargs):
         categories = Category.objects.all()
         return categories

 
    