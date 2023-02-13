
from django.urls import path
from .views import ( HomeView, ItemDetailView, OrderSummaryView, ProductsView,
                    account, profile, login, signup, about, add_to_cart, remove_from_cart, delete_from_cart, price_sort, price_rev_sort, name_sort,
                    CheckOutView, PaymentView
                    )

app_name = 'base'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductsView.as_view(), name='products'),
    path('product_details/<slug>/', ItemDetailView.as_view(), name='product_details'),
    path('account/', account, name='account'),
    path('profile/', profile, name='profile'),
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('cart/', OrderSummaryView.as_view(), name='cart'),
    path('about/', about, name='about'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('delete_from_cart/<slug>/', delete_from_cart, name='delete_from_cart'),
    path('checkout/', CheckOutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('products/price-sort', price_sort, name='price_sort'),
    path('products/price_rev_sort', price_rev_sort, name='price_rev_sort'),
    path('products/name-sort', name_sort, name='name_sort'),

]