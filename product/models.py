from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.shortcuts import reverse
# Create your models here.


class Product(models.Model):
    SIZE_CHOICES = (('S', 'S'),
                    ('M', 'M'),
                    ('L', 'L'),
                    ('XL', 'XL'),)
    CATEGORY_CHOICES = (('S', 'Shirts'),
                        ('SW', 'Sports wear'),
                        ('C', 'Casuals'),
                        ('OW', 'Outwear'),
                        ('WW', 'Winter Wear'),)
    LABEL_CHOICES = (('P', 'primary'),
                     ('S', 'secondary'),
                     ('D', 'danger'),)
    title = models.CharField(max_length=150)
    image = models.ImageField()
    price = models.FloatField()
    discounted_price = models.FloatField(blank=True, null=True)
    size = models.CharField(choices=SIZE_CHOICES, max_length=2)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField(unique=True, editable=False)
    description = models.TextField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product:product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('order:add-to-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('order:remove-from-cart', kwargs={
            'slug': self.slug
        })


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = '%s-%s' % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_product_receiver, sender=Product)
