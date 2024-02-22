from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

import re
from utils.cpfvalidator import valid_cpf

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(verbose_name='Idade')
    cpf = models.CharField(max_length=11, help_text='Apenas números.', verbose_name='CPF')
    address = models.CharField(max_length=50, verbose_name='Endereço')
    address_number = models.CharField(max_length=5, verbose_name='Número')
    address_compliment = models.CharField(max_length=30, blank=True, verbose_name='Complemento')
    neighborhood = models.CharField(max_length=30, verbose_name='Bairro')
    cep = models.CharField(max_length=8, help_text='Apenas números.', verbose_name='CEP')
    city = models.CharField(max_length=30, verbose_name='Cidade')
    state = models.CharField(
        max_length=2,
        verbose_name='Estado',
        default='SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return f'{self.user}'

    def clean(self):
        error_messages = {}

        if not valid_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um CPF válido.'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP inválido, digite os 8 dígitos do CEP.'

        if error_messages:
            raise ValidationError(error_messages)