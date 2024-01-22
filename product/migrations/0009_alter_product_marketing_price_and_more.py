# Generated by Django 5.0 on 2024-01-22 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_product_promo_marketing_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='marketing_price',
            field=models.FloatField(help_text='Obrigatório preencher na tabela abaixo mesmo se o produto não tiver variação.'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('V', 'Variável'), ('S', 'Simples')], default='V', help_text='Variável: produto com diferentes variações (Ex.: P, M, G).<br>Simples: produto genérico que não possui variações específicas.', max_length=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='promo_marketing_price',
            field=models.FloatField(default=0, help_text='Mantenha 0 se não existir preço promocional. Caso exista, preencher aqui e na tabela abaixo.'),
        ),
    ]