from django.db import models
from decimal import Decimal

class DocumentCounter(models.Model):
    last_document_number = models.IntegerField(default=0)  # Common counter for both invoice and receipt

class Expense(models.Model):
    date = models.DateField()
    party = models.CharField(max_length=100)
    particulars = models.CharField(max_length=200)
    invoice_number = models.CharField(max_length=20)  # Should be defined as invoice_no
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_or_cash = models.CharField(max_length=20, default='Cash')
    igst = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    cgst = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    kgst = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tds = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))


    def save(self, *args, **kwargs):
            if self.amount:
                
                self.total = self.amount + (self.amount * self.igst / 100) + \
                            (self.amount * self.cgst / 100) + (self.amount * self.kgst / 100) - \
                            (self.amount * self.tds / 100)
            super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Automatically calculate total before saving
        # Note: total is not a field in the model anymore
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.party} - {self.amount}"



# class Expense(models.Model):
#     date = models.DateField()
#     party = models.CharField(max_length=100)
#     particulars = models.CharField(max_length=200)
#     invoice_number = models.CharField(max_length=20)  # Should be defined as invoice_no
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     bank_or_cash = models.CharField(max_length=20, default='Cash')
#     igst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
#     cgst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
#     kgst_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
#     tds_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
#     total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=Decimal('0.00'))

#     def save(self, *args, **kwargs):
#             if self.amount:
                
#                 self.total = self.amount + (self.amount * self.igst / 100) + \
#                             (self.amount * self.cgst / 100) + (self.amount * self.kgst / 100) - \
#                             (self.amount * self.tds / 100)
#             super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.invoice_no} - {self.party}"