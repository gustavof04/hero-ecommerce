from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import copy

from . import models
from . import forms

# TODO: Remove get() method after tests

class BaseProfile(View):
    template_name = 'profiles/create.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.profile = None

        if self.request.user.is_authenticated:
            self.profile = models.Profile.objects.filter(
                user=self.request.user
            ).first()

            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                    instance=self.profile,
                )
            }
        else:
            self.context = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                ),
                'profileform': forms.ProfileForm(
                    data=self.request.POST or None,
                )
            }

        self.userform = self.context['userform']
        self.profileform = self.context['profileform']

        if self.request.user.is_authenticated:
            self.template_name = 'profiles/update.html'

        self.render = render(self.request, self.template_name, self.context)

    def get(self, *args, **kwargs):
        return self.render


class Create(BaseProfile):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.profileform.is_valid():
            return self.render

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        if self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user.username)

            user.username = username

            if password:
                user.set_password(password)

            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            if not self.profile:
                self.profileform.cleaned_data['user'] = user
                profile = models.Profile(**self.profileform.cleaned_data)
                profile.save()
            else:
                profile = self.profileform.save(commit=False)
                profile.user = user
                profile.save()

        else:
            user = self.userform.save(commit=False)
            user.set_password(password)
            user.save()

            profile = self.profileform.save(commit=False)
            profile.user = user
            profile.save()

        if password:
            auth = authenticate(self.request, username=user, password=password)

            if auth:
                login(self.request, user=user)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        if self.request.user.is_authenticated and self.profile is not None:
            messages.success(
                self.request,
                'Seu cadastro foi atualizado com sucesso.'
            )
        else:
            messages.success(
                self.request,
                'Seu cadastro foi criado com sucesso.'
            )
            messages.success(
                self.request,
                'Você agora é um(a) hero 🦸! Aproveite os nossos produtos direto de sua residência.'
            )

        return redirect('profiles:create')


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Logout')