from django.http import HttpResponse
from django.template import loader
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.conf import settings
from .list import *



class Item (models.Model):
    title = models.CharField(max_length=50)
    price = models.FloatField()
    d_price = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    brand = models.CharField(choices=BRAND, max_length=2, blank=True, null=True)
    gender = models.CharField(choices=GENDER, max_length=2, blank=True, null=True)
    color = models.CharField(choices=COLORS, max_length=2, blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField()
    crated = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos', null=False, blank=False)
    image1 = models.ImageField(upload_to='photos', null=False, blank=False)
    image2 = models.ImageField(upload_to='photos', null=False, blank=False)
    image3 = models.ImageField(upload_to='photos', null=False, blank=False)
    image4 = models.ImageField(upload_to='photos', null=False, blank=False)

    

    def __str__(self):
        return self.title
    
    def percent_saving(self):
        if self.d_price:
            x = self.price - self.d_price
            y = (x / self.price) * 100
            return int(y)
        
        
    def saving(self):
        return self.price - self.d_price
        
    
    def get_absolute_url(self):
        return reverse('base:product_details', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('base:add_to_cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('base:remove_from_cart', kwargs={
            'slug': self.slug
        })
        
    def get_delete_from_cart_url(self):
        return reverse('base:delete_from_cart', kwargs={
            'slug': self.slug
        })
        
    def testing(request):
        mydata = Item.objects.order_by('price')
        template = loader.get_template('products.html')
        context = {
            'object_list': mydata,
        }
        return HttpResponse(template.render(context, request))
        
        
    @property
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url

    @property
    def get_image1_url(self):
        if self.image1 and hasattr(self.image1, 'url'):
            return self.image1.url
        
    @property
    def get_image2_url(self):
        if self.image2 and hasattr(self.image2, 'url'):
            return self.image2.url
        
    @property
    def get_image3_url(self):
        if self.image3 and hasattr(self.image3, 'url'):
            return self.image3.url
        
    @property
    def get_image4_url(self):
        if self.image4 and hasattr(self.image4, 'url'):
            return self.image4.url

class OrderItem (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def total_price(self):
        return self.quantity * self.item.price
    
    def total_d_price(self):
        return self.quantity * self.item.d_price
    
    def saving(self):
        return self.total_price() - self.total_d_price()
    
    def get_total_price(self):
        if self.item.d_price:
            return self.total_d_price()
        return self.total_price()


class Order (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
 
    def final_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
            return total

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=50)
    apartment_address = models.CharField(max_length=50)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=50)
    
    def __str__(self):
        return self.user.username
    
    
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    