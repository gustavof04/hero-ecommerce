from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from . import models

# TODO: Remove get() method after tests

class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10


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

        return HttpResponse(f'{variation.product}')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover do Carrinho')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')


class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')