from django.db import models
from django.utils.text import slugify
from utils.resizer import resize_image
from utils import priceformatter


class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(upload_to='product_images/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    marketing_price = models.FloatField()
    promo_marketing_price = models.FloatField(default=0)
    product_type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def get_formatted_price(self):
        return priceformatter.format_price(self.marketing_price)
    get_formatted_price.short_description = 'Price'

    def get_formatted_promo_price(self):
        return priceformatter.format_price(self.promo_marketing_price)
    get_formatted_promo_price.short_description = 'Promo Price'

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.image:
            resize_image(self.image, max_image_size)

    def __str__(self):
        return self.name


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    promo_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name or self.product.name