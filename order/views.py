from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages

from product.models import Variation
from .models import Order, OrderItem

from utils import cart_tools

# TODO: Remove get() method after tests

class DispatchLoginRequiredMixin(View):
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profiles:create')

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user=self.request.user)
        return qs


class Pay(DispatchLoginRequiredMixin, DetailView):
    template_name = 'order/pay.html'
    model = Order
    pk_url_kwarg = 'pk'
    context_object_name = 'order'


class SaveOrder(View):
    template_name= 'order/pay.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login para finalizar sua compra!'
            )
            return redirect('profiles:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Seu carrinho está vazio!'
            )
            return redirect('product:list')

        cart = self.request.session.get('cart')
        cart_variation_ids = [v for v in cart]
        bd_variations = list(
            Variation.objects.select_related('product').filter(id__in=cart_variation_ids)
        )

        for variation in bd_variations:
            vid = str(variation.id)

            stock = variation.stock
            cart_qnt = cart[vid]['quantity']
            unt_price = cart[vid]['unit_price']
            unt_promo_price = cart[vid]['unit_promo_price']

            error_msg_stock = ''

            if stock < cart_qnt:
                cart[vid]['quantity'] = stock
                cart[vid]['quantitative_price'] = stock * unt_price
                cart[vid]['quantitative_promo_price'] = stock * unt_promo_price

                error_msg_stock = 'Estoque insuficiente para alguns produtos do seu carrinho. Reduzimos a quantidade desses produtos. Por favor, verifique quais produtos foram afetados a seguir.'

            if error_msg_stock:
                messages.error(
                    self.request,
                    error_msg_stock
                )

                self.request.session.save()
                return redirect('product:cart')

        qnt_cart_total = cart_tools.cart_total_qnt(cart)
        value_cart_total = cart_tools.cart_totals(cart)

        order = Order(
            user=self.request.user,
            total=value_cart_total,
            qnt_total=qnt_cart_total,
            status='C',
        )

        order.save()

        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product=v['product_name'],
                    product_id=v['product_id'],
                    variation=v['variation_name'],
                    variation_id=v['variation_id'],
                    price=v['quantitative_price'],
                    promo_price=v['quantitative_promo_price'],
                    quantity=v['quantity'],
                    image=v['image'],
                ) for v in cart.values()
            ]
        )

        del self.request.session['cart']
        return redirect(
            reverse(
                'order:pay',
                kwargs={
                    'pk': order.pk
                }
            )
        )


class Detail(DispatchLoginRequiredMixin, DetailView):
    model = Order
    context_object_name = 'order'
    template_name = 'order/detail.html'
    pk_url_kwarg = 'pk'


class List(DispatchLoginRequiredMixin, ListView):
    model = Order
    context_object_name = 'orders'
    template_name = 'order/list.html'
    paginate_by = 10
    ordering = ['-id']