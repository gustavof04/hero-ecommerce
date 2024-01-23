from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ListProducts.as_view(), name='list'),
    path('<slug>', views.ProductDetail.as_view(), name='detail'),
    path('addtocart/', views.AddToCart.as_view(), name='addtocart'),
    path('removefromcart/', views.RemoveFromCart.as_view(), name='removefromcart'),
    path('cart/', views.Cart.as_view(), name='cart'),
    path('purchaseoverview/', views.PurchaseOverview.as_view(), name='purchaseoverview'),
]
