from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


########################## Product Models ###############################

class Product(models.Model):
    name = models.CharField(max_length=200,verbose_name='product_name')
    price =models.PositiveIntegerField()
    description = models.TextField(max_length=1000,verbose_name='product_description')
    image_url = models.URLField(max_length=3000)
    category  = models.ForeignKey('Category', on_delete=models.SET_NULL,null=True)
    discount = models.PositiveIntegerField(default=0)
    stock_number = models.PositiveBigIntegerField(default=0)
    available = models.PositiveIntegerField(default=0)
    # product_uuid = models.UUIDField(primary_key=True,editable=False,default=uuid4)

    @staticmethod
    def product_price(self):
        if self.discount > 0:
            discount = self.discount/100*self.price
            new_price = self.price-discount
            return new_price
        return self.price
    
    def __str__(self):
        return self.name
    
#product bought by customer
class ProductInstance(models.Model):
    STATUS = [
        ('D','Delivered'),
        ('P','Pending')
    ]
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    #unique product id
    product_uuid = models.UUIDField(primary_key=True,editable=False,default=uuid4) # to ren
    product_count = models.PositiveIntegerField(verbose_name='number of product',default=1)
    delivery_status = models.CharField(max_length=1,choices=STATUS,default='P')
    
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


#product instance to be added to thr cart  
class Cart(models.Model):
    products = models.ManyToManyField(ProductInstance)

#reviews of a product by the customer
class Product_Review(models.Model):
    customer=models.ForeignKey('Customer',on_delete= models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_made = models.DateTimeField(auto_now_add=True)
    review = models.TextField()

    def __str__(self):
        return f'{self.product.name[:15]}_review'
    

class Customer(models.Model):
    profile = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone_number = models.CharField(max_length=10,blank=True)
    cart =  models.OneToOneField(Cart,on_delete=models.SET_NULL,null=True,blank=True)
    def __str__(self):
        return self.profile.username


    