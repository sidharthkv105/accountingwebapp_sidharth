# main/models.py
# models.py
from django.db import models
from decimal import Decimal

class DocumentCounter(models.Model):
    last_document_number = models.IntegerField(default=0)  # Common counter for both invoice and receipt




from django.db import models

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
    tds = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.date} - {self.party} - {self.amount}"


