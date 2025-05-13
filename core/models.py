from django.db import models

# Create your models here.

class Sale(models.Model):
    date = models.DateField()
    order_id = models.CharField(max_length=100)
    amount_sgd = models.DecimalField(max_digits=10, decimal_places=2)
    product_id = models.CharField(max_length=100)
    imported_file = models.ForeignKey('ImportedFile', on_delete=models.CASCADE, null=True, blank=True, related_name='sales')

    def __str__(self):
        return f"Order {self.order_id} - Product {self.product_id} on {self.date}"

class ImportedFile(models.Model):
    filename = models.CharField(max_length=255)
    imported_at = models.DateTimeField(auto_now_add=True)
    num_rows = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='success')
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.filename} ({self.status}) at {self.imported_at}"
