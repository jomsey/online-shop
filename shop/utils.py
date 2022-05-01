from uuid import UUID
from shop.models import Customer,Category,Product,Cart

def get_cart(request):
        """
        Creates or retrives user cart depending on their authenticity
        When user is registered retrieve their cart 
        When user not registered create a cart with with its uuid stored in the session data
        If session not found , create one
        """

        if request.user.is_authenticated:
                customer = Customer.objects.get(profile=request.user) 
                cart = customer.cart  #customer cart is created on register
        else:
                #create user cart or retrieve it from the session data
                if 'cart_id' in request.session:
                        cart = Cart.objects.get(cart_uuid=request.session['cart_id'])
                       
                else:
                         cart = Cart.objects.create() # create cart for the anonymous user
                         cart.save()
                         request.session['cart_id'] = cart.cart_uuid.hex #create session
                        
                request.session.modified = True

        return cart

def  cart_items_number(request):
        """Gets the user's cart and retirn the total number of product added to the cart"""
        cart = get_cart(request)
        cart_products = cart.products.all()
        
        number = 0
        for product in cart_products:
                number += product.product_count
        
        return number


def get_all_categories(request,*args, **kwargs):
         categories = Category.objects.all()
         return categories
 
 
def cart_overall_price_total(request):
        """
        Retrieves all products in the cart and calculates the total price
        """
        cart=get_cart(request)
        cart_products = cart.products.select_related('product').all()
        total = 0
        
        for product in cart_products:
                total+=(product.product.discount_product_price())*product.product_count
        return total
                
def get_recently_viewed_product(request):
        recent = request.session.get('recently_viewed')
        products = []
        
        if recent:
                 for product_name in recent:
                    products.append(Product.objects.get(name=product_name))
        return set(products)
   