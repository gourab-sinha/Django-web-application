from django.db import models
from account.models import Account


class Category(models.Model):
    category = models.CharField(max_length=30, unique=True, null=False)

    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=30, null=False)
    image = models.ImageField(verbose_name="Image", blank=False, upload_to='product/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    seller = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    price = models.FloatField()
    description = models.CharField(max_length=300, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    zip_code = models.CharField(max_length=30, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address






