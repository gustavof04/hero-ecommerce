from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from . import models

# TODO: Remove get() method after tests

class ListProducts(ListView):
    model = models.Product
    template_name = 'product/list.html'
    context_object_name = 'products'
    paginate_by = 10


class ProductDetail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe')


class AddToCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Adicionar ao carrinho')


class RemoveFromCart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Remover do Carrinho')


class Cart(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Carrinho')


class Finish(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar')