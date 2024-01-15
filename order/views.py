from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse

# TODO: Remove get() method after tests

class Pay(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagar')


class Checkout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Finalizar Pedido')


class Detail(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Detalhe')