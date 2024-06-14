from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



    
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length = 200, null=True)
    last_name = models.CharField(max_length = 200, null=True)
    email = models.CharField(max_length = 200, null=True)

    def __str__(self):
        return self.name or 'blad'
    
@receiver(post_save, sender=User)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(
            user=instance,
            name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email
        )    

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True, null=False)

    def __str__(self):
        return self.name or 'blad'

class Product(models.Model):
    name = models.CharField(max_length = 200, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=1)  # Assuming '1' is the id for 'Uncategorized'
    description = models.TextField(null=True, blank=True, default="")
    rating = models.FloatField(default=0, null=True, blank=True)

    def __str__(self):
        return self.name or 'blad'
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url=''
        return url
 
class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.product.name or 'blad'}"
       
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.transaction_id or 'blad'}, {self.date_ordered or 'blad'}"
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    city = models.CharField(max_length = 200, null=True)
    address = models.CharField(max_length = 200, null=True)    
    phone_number = models.CharField(max_length = 9, null=True)
    zipcode = models.CharField(max_length = 200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.address or 'blad'}, {self.city or 'blad'}, {self.zipcode or 'blad'}"
