from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from .forms import Checkoutform, PriceRange
from .list import *
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, BillingAddress, Payment
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

class CheckOutView(View):
    def get(self, *args, **kwargs):
        #form
        form = Checkoutform()
        context = {
            'form' : form
        }
        return render(self.request, "checkout.html", context)
    
    def post(self, *args, **kwargs):
        form = Checkoutform(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                # f_name = form.cleaned_data.get('f_name')
                # l_name = form.cleaned_data.get('l_name')
                # email = form.cleaned_data.get('email')
                street_address = form.cleaned_data.get('street_address')
                apartment_address =form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                state = form.cleaned_data.get('state')
                zip = form.cleaned_data.get('zip')
                # TODO: add functions later
                # same_billing_address = form.cleaned_data.get(same_billing_address)
                # save_info = form.cleaned_data.get(save_info)
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user = self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                    # same_billing_address=same_billing_address,
                    # save_info=save_info
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                
                if payment_option == "ST":
                    return redirect('base:payment', payment_option='Stripe')
                elif payment_option == "PP":
                    return redirect('base:payment', payment_option='Paypal')
                else:
                    messages.warning(self.request, 'Invalid payment option')
                    return redirect('base:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect("/")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'payment.html', context )
    
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('reservation[stripe_token]')
        amount= int(order.final_price())
        
        try:
            charge = stripe.Charge.create(
                amount=amount,   # Cents
                currency="usd",
                source=token, # obtained with Stripe.js
                metadata={'order_id': '6735'}
            )
            
            # create payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = amount
            payment.save()
            
            # assign payment into the order
            
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()
            
            order.ordered = True
            order.payment = payment
            order.save()
            
            messages.success(self.request, "Your order was successful!")
            return redirect('base:cart')
            
        except stripe.error.CardError as e:
            messages.error(self.request, "Card error occurred: {}".format(e.user_message))
            return redirect('base:checkout')
        except stripe.error.InvalidRequestError:
            messages.error(self.request, "An invalid request occurred.")
            return redirect('base:checkout')
        except Exception:
            # send Email to self
            messages.error(self.request, "Another problem occurred, We have been notified.")
            return redirect('base:checkout')


def price_sort(request):
    mydata = Item.objects.all().order_by('price')
    template = loader.get_template('products.html')
    context = {
        'object_list': mydata
    }
    return HttpResponse(template.render(context, request))

def price_rev_sort(request):
    mydata = Item.objects.order_by('-price')
    template = loader.get_template('products.html')
    context = {
        'object_list': mydata
    }
    return HttpResponse(template.render(context, request))

def name_sort(request):
    mydata = Item.objects.order_by('title')
    template = loader.get_template('products.html')
    context = {
        'object_list': mydata
    }
    return HttpResponse(template.render(context, request))


class HomeView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'index.html'


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product-details.html'
  
class ProductsView(ListView):
    paginate_by = 9
    template_name = 'products.html'
    context_object_name = 'Products_Lists'
    
    def get_queryset(self):
        return Item.objects.order_by('-crated')
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        context['form'] = PriceRange
        context['brands'] = BRAND
        return context
    
    # def products(self, *args, **kwargs):
    #     brand_choice =  self.request.GET.get('filter-brand')
    #     if brand_choice:
    #         product = Item.objects.filter(brand__iexact=brand_choice)
    #     else:
    #         product = Item.objects.all()
            
    #     products = Item.objects.all()
    #     context = {
    #         'products' : products, 'product' : product, 'brands' : BRAND
    #     }
    #     return render(self.request, 'products.html', context)
    
    # def get(self, request, *args, **kwargs):
    #     model = Item.objects.all()
    #     form = PriceRange()
    #     template = loader.get_template('products.html')
    #     context = {
    #         'form' : form,
    #         'object_list': model
    #     }
    #     return HttpResponse(template.render(context, request))
    
    def post(self, *args, **kwargs):
        form = PriceRange(self.request.POST)
        if form.is_valid():
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            model =  Item.objects.filter(price__range=(min_price, max_price)).order_by('price')
            template = loader.get_template('products.html')
            context = {
                    'form' : form,
                    'object_list': model,
                    'brands' : BRAND
                }
            return HttpResponse(template.render(context, self.request))
    
        
#class ProductsView(ListView):
#    model = Item
#   paginate_by = 9
#   template_name = 'products.html'
    
    
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object' : order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect("/")



def account(request):
    return render(request, "account.html")

@login_required
def profile(request):
    return render(request, "profile.html")

def login(request):
    return render(request, "account/login.html")

def signup(request):
    return render(request, "account/signup.html")

def checkout(request):
    return render(request, "checkout.html")

def about(request):
    return render(request, "about.html")

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect("base:cart")
        else:
            order.items.add(order_item)
            order_item.quantity = 1
            order_item.save()
            messages.info(request, "This item was added to your cart")
            return redirect("base:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        order_item.save()
        messages.info(request, "This item was added to your cart")
        return redirect("base:cart")
    
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart")
            return redirect("base:cart")
            
        else:
            #add message =the order does not content this order item
            messages.info(request, "This item is not in your cart")
            return redirect("base:cart")
    else:
        #add message =the user does not have an order
        messages.info(request, "You do not have an active order")
        return redirect("base:cart")

    
    
@login_required
def delete_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "This item quantity was updated")
                return redirect("base:cart")
            else:
                order.items.remove(order_item)
                messages.info(request, "This item was removed from your cart")
                return redirect("base:cart")
        else:
            #add message =the order does not content this order item
            messages.info(request, "This item is not in your cart")
            return redirect("base:cart")
    else:
        #add message =the user does not have an order
        messages.info(request, "You do not have an active order")
        return redirect("base:cart")
    
