from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.contrib import messages

from . import models
from profiles.models import Profile


class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10
    ordering = ['-id']


class ProductDetail(DetailView):
    model = models.Product
    template_name = 'product/detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class AddToCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        vid = self.request.GET.get('vid')

        if not vid:
            messages.error(
                self.request,
                'ERRO: O produto não existe!'
            )
            return redirect(http_referer)

        variation = get_object_or_404(models.Variation, id=vid)
        variation_stock = variation.stock
        product = variation.product

        product_id = product.id
        product_name = product.name
        variation_name = variation.name or ''
        unit_price = variation.price
        unit_promo_price = variation.promo_price
        quantity = 1
        slug = product.slug
        image = product.image

        if image:
            image = image.name
        else:
            image = ''

        if variation.stock < 1:
            messages.error(
                self.request,
                'ERRO: Estoque insuficiente!'
            )
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if vid in cart:
            cart_quantity = cart[vid]['quantity']
            cart_quantity += 1

            if variation_stock < cart_quantity:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {cart_quantity}x no produto "{product.name}". Há {variation_stock}x no seu carrinho.'
                )
                cart_quantity = variation_stock

            cart[vid]['quantity'] = cart_quantity
            cart[vid]['quantitative_price'] = unit_price * cart_quantity
            cart[vid]['quantitative_promo_price'] = unit_promo_price * cart_quantity
        else:
            cart[vid] = {
                'product_id': product_id,
                'product_name': product_name,
                'variation_name': variation_name,
                'variation_id': vid,
                'unit_price': unit_price,
                'unit_promo_price': unit_promo_price,
                'quantitative_price': unit_price,
                'quantitative_promo_price': unit_promo_price,
                'quantity': 1,
                'slug': slug,
                'image': image,
            }

        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {product_name} {variation_name} adicionado ao seu carrinho {cart[vid]["quantity"]}x.'
        )

        return redirect(http_referer)


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('product:list')
        )
        vid = self.request.GET.get('vid')

        if not vid:
            return redirect(http_referer)
        
        if not self.request.session.get('cart'):
            return redirect(http_referer)
        
        if vid not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][vid]

        messages.success(
            self.request,
            f'Produto {cart["product_name"]} {cart["variation_name"]} removido do seu carrinho.'
        )

        del self.request.session['cart'][vid]
        self.request.session.save()
        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        context = {
            'cart': self.request.session.get('cart') 
        }

        return render(self.request, 'product/cart.html', context)


class PurchaseOverview(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('profiles:create')

        profile = Profile.objects.filter(user=self.request.user).exists()

        if not profile:
            messages.error(
                self.request,
                'Usuário sem perfil. Preencha os campos vazios.'
            )
            return redirect('profiles:create')

        if not self.request.session.get('cart'):
            messages.error(
                self.request,
                'Seu carrinho está vazio.'
            )
            return redirect('product:list')

        context = {
            'user': self.request.user,
            'cart': self.request.session['cart'],
        }

        return render(self.request, 'product/purchaseoverview.html', context)