from django.db import models


class Shop(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('complete', 'Complete'),
        ('pending', 'Pending'),
    ]

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    order_id = models.CharField(max_length=50)

    def __str__(self):
        return self.order_id
