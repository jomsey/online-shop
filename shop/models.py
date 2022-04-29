import math
from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4



class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name='product_name')
    price =models.PositiveIntegerField()
    description = models.TextField(max_length=1000,verbose_name='product_description')
    image_url = models.URLField(max_length=3000)
    category  = models.ForeignKey('Category', on_delete=models.SET_NULL,null=True)
    discount = models.PositiveIntegerField(default=0)
    stock_number = models.PositiveBigIntegerField(default=0)
    available = models.PositiveIntegerField(default=0)

    def discount_product_price(self):
        if self.discount > 0:
            discount = self.discount/100*self.price
            new_price = self.price-discount
            return int(new_price)
        else:
            return self.price #for items without discount
        
    def product_short_name_version(self):
        if len(self.name) > 18:
            name = self.name[:18].strip()
            return f'{name}...'
        else:
            return self.name
        
    #calculate percentage remaining stoke
    def stoke_left_percentage(self):
        if self.available>0:
            percentage = math.floor(self.available/self.stock_number*100) #nondecimal percentage
            return f'width:{percentage}%;' #css width of the product stoke remaining progress bar
   
    def __str__(self):
        return self.name
    
#product bought by customer
class ProductInstance(models.Model):
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    product_uuid = models.UUIDField(primary_key=True,editable=False,default=uuid4) # #unique product id
    product_count = models.PositiveIntegerField(verbose_name='number of product',default=1)
    
    def __str__(self):
        return self.product.name
    
    
#category to which the product belongs
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'
    
class ProductSpecification(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    weight  = models.PositiveIntegerField()
    main_material = models.CharField(max_length=200,blank=True)
    model =models.CharField(max_length=200,blank=True) 



class Cart(models.Model):
    products = models.ManyToManyField(ProductInstance) #product instance to be added to the cart 
    cart_uuid = models.UUIDField(editable=False,default=uuid4,null=True,unique=True)


class ProductReview(models.Model):
    RATE_CHOICES = [
        (1,'very poor'),
        (2,'poor'),
        (3,'good'),
        (4,'very good'),
        (5,'excellent')
    ]
    customer=models.ForeignKey('Customer',on_delete= models.CASCADE,null=True) #customer making product review
    product = models.ForeignKey(Product,on_delete=models.CASCADE) #product being reviewed
    date_made = models.DateField(auto_now_add=True)
    review = models.TextField()
    rating = models.PositiveSmallIntegerField(verbose_name='product_rating',null=True,choices=RATE_CHOICES)
    
    def __str__(self) :  
        #return the first 30 charactors of the product name
        if len(self.product.name) > 30:
            return f'{self.product.name[:30]}..review'
        else:
            return self.product.name
        
    def get_rating(self):
        return range(1,self.rating+1)        
          
class Customer(models.Model):
    profile = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone_number = models.CharField(max_length=10,blank=True)
    cart =  models.OneToOneField(Cart,on_delete=models.SET_NULL,null=True,blank=True) 
    def __str__(self):
        return self.profile.username


    
class Order(models.Model):
    STATUS = [
        ('P','Pending'),
        ('D','Delivered')
    ]
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    status = models.CharField(max_length=1,choices=STATUS,default="P")
    date_made = models.DateTimeField(auto_now_add=True)
    order_cart = models.ForeignKey(Cart,on_delete=models.PROTECT,null=True,default=None,editable=False)
    order_id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    
    def __str__(self) -> str:
        return str(self.order_id)
    
    
class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    
class Trader(models.Model):
    trader = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    second_name = models.CharField(max_length=150)
    products = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    


class CustomerWishList(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductInstance)
  
class Promotion(models.Model):
    name = models.CharField(max_length=150)
    products = models.ManyToManyField(Product)

    