import email
from django.db import models
from django.contrib.auth.models import User


class InstagramPost(models.Model):
    like_count=models.IntegerField(default=0)
    tname=models.CharField(max_length=200,default='NULL')

class Profile(models.Model):
    prouser = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile/")
    counts=models.IntegerField(default=0)
    amount=models.IntegerField(default=0)
    dis = models.CharField(max_length=399)
    reward=models.IntegerField(default=0)
    bill=models.IntegerField(default=0)
    tname=models.CharField(max_length=399,default=0)
    like=models.IntegerField(default=0)
    followers=models.IntegerField(default=0)
    repost=models.IntegerField(default=0)
    views=models.IntegerField(default=0)
    comments=models.IntegerField(default=0)
    ru=models.IntegerField(default=0)
    # first=models.IntegerField(default=0)
    address = models.CharField(max_length=1000,default='undefined')
    mobile=models.IntegerField(default=0)
    # second=models.IntegerField(default=0)
    # second_name = models.CharField(max_length=399,default=0)
    # third=models.IntegerField(default=0)
    # third_name = models.CharField(max_length=399,default=0)
    def __str__(self):
        return self.prouser.username

class Category(models.Model):
    title = models.CharField(max_length=199)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title

class Cos_Category(models.Model):
    title = models.CharField(max_length=199)
    date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.title

class Cos_Product(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Cos_Category,on_delete=models.SET_NULL,blank=True, null=True)
    image0 = models.ImageField(upload_to="products/",blank=False)

    sold=models.IntegerField(default=1,blank=True,null=True)
    # marcket_price = models.PositiveIntegerField()
    selling_price= models.PositiveIntegerField(default=0, blank=True, null=True)
    selling_price1= models.PositiveIntegerField(default=0, blank=True, null=True)
    selling_price2= models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.TextField()
    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Cos_Category,on_delete=models.SET_NULL,blank=True, null=True)
    image0 = models.ImageField(upload_to="products/",blank=False)
    image1 = models.ImageField(upload_to="products/",blank=False)
    image2 = models.ImageField(upload_to="products/",blank=False)
    image3 = models.ImageField(upload_to="products/",blank=False)
    image4 = models.ImageField(upload_to="products/",blank=False)
    sold=models.IntegerField(default=1,blank=True,null=True)
    # marcket_price = models.PositiveIntegerField()
    allrating=models.IntegerField(default=0)
    rating=models.DecimalField(default=0,blank=False,max_digits=5,decimal_places=1)
    selling_price= models.PositiveIntegerField(default=0, blank=True, null=True)
    selling_price1= models.PositiveIntegerField(default=0, blank=True, null=True)
    selling_price2= models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.TextField()
    def __str__(self):
        return self.title

class Filterpro(models.Model):
    protitle = models.CharField(max_length=200)
    prodate = models.DateField(auto_now_add=True)
    procategory = models.ForeignKey(Category,on_delete=models.SET_NULL,blank=True, null=True)
    proimage = models.ImageField(upload_to="products/",blank=False)
    proimage1 = models.ImageField(upload_to="products/",blank=False)
    proimage2 = models.ImageField(upload_to="products/",blank=False)
    proimage3 = models.ImageField(upload_to="products/",blank=False)
    proimage4 = models.ImageField(upload_to="products/",blank=False)
    prosold=models.IntegerField(default=1,blank=True,null=True)
    # marcket_price = models.PositiveIntegerField()
    proselling_price= models.PositiveIntegerField(default=0, blank=True, null=True)
    proselling_price1= models.PositiveIntegerField(default=0, blank=True, null=True)
    proselling_price2= models.PositiveIntegerField(default=0, blank=True, null=True)
    prodescription = models.TextField()

class Cart(models.Model):
    customer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    total = models.PositiveIntegerField()
    complit = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

class CartProduct(models.Model):
    # customer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()
    def __str__(self):
        return f"Cart=={self.cart.id}<==>CartProduct:{self.id}==Qualtity=={self.quantity}"


ORDER_STATUS = (
    ("Order Received", "Order Received"),
    ("Order Processing", "Order Processing"),
    ("On the way", "On the way"),
    ("Order Completed", "Order Completed"),
    ("Order Canceled", "Order Canceled"),
)

class Order(models.Model):
    # title= models.CharField(max_length=255)
    cart  = models.OneToOneField(Cart,on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    mobile = models.CharField(max_length=16)
    email = models.CharField(max_length=200)
    mode = models.CharField(max_length=100,default="COD")
    total = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=1,blank=True,null=True)
    order_status = models.CharField(max_length=100,choices=ORDER_STATUS,default="Order Received")
    date = models.DateField(auto_now_add=True)
    payment_complit = models.BooleanField(default=False,blank=True, null=True)
    isdeleted=models.BooleanField(default=False)
    reason = models.CharField(max_length=100,default="Others")

class con(models.Model):
    usname=models.TextField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    message = models.TextField()

    
class OTPVerifiaction(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=4)
    is_verfied = models.BooleanField(default=False)

class Post(models.Model):
    name = models.CharField(max_length=100,default='null')
    title = models.CharField(max_length=100,default='null')
    model=models.CharField(max_length=100,default='null')
    year=models.CharField(max_length=100,default='null')
    rang=models.CharField(max_length=100,default='null')
    phone_number=models.CharField(max_length=100,default='null')
    email=models.CharField(default='null',max_length=100)
    content = models.TextField(max_length=100,default='null')
    # image = models.ImageField(upload_to="posts/")
    
    def __str__(self):
        return self.name

class Call(models.Model):
    name=models.CharField(max_length=100,default='null')
    phone_number=models.CharField(max_length=100,default='null')
    def __str__(self):
        return self.name

class search(models.Model):
    pro_name=models.CharField(max_length=100,default='null')


class review(models.Model):
    productname=models.CharField(max_length=100,default='null')
    customername=models.CharField(max_length=100,default='null')
    comments=models.CharField(max_length=100,blank=False,default='null')
    customerrating=models.IntegerField(default=3,blank=False)