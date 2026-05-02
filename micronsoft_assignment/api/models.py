from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale: {self.product.name}"

class Transaction(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        indexes = [
            models.Index(fields=['created_at']),
        ]