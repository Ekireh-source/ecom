from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Categories(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


CATEGORY_CHOICES = {
    ('S', 'Shirt'),
    ('P', 'Pants'),
    ('SU', 'Suits'),
    ('D', 'Dress')
}

class Item(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    discount_price = models.FloatField(null=True, blank=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:product', kwargs={
            'slug': self.slug
        })

    def add_to_cart_url(self):
        return reverse('core:add_to_cart', kwargs={
            'slug': self.slug
        })

    def remove_from_cart_url(self):
        return reverse('core:remove_from_cart', kwargs={
            'slug': self.slug
        })

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url




class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_item_price(self):
        return self.quantity * self.item.price

    def get_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_item_discount_price()
        return self.get_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)


    def __str__(self):
        return self.user.first_name

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def item_total_number(self):
        qs = Order.objects.filter(ordered=False)
        if qs.exists():
            return qs[0].items.count()
        return 0