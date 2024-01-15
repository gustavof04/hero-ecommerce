from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.Pay.as_view(), name='pay'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('detail/', views.Detail.as_view(), name='detail'),
]