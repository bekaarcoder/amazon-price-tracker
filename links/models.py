from django.db import models
from .utils import get_url_data


class Link(models.Model):
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField()
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    in_stock = models.CharField(max_length=200, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ("price_difference", "-created")

    def save(self, *args, **kwargs):
        name, price, in_stock = get_url_data(self.url)
        if self.current_price:
            if price != self.current_price:
                self.price_difference = round((price - self.current_price), 2)
                self.old_price = self.current_price
        else:
            self.old_price = 0
            self.price_difference = 0

        self.name = name
        self.current_price = price
        self.in_stock = in_stock

        super().save(*args, **kwargs)
