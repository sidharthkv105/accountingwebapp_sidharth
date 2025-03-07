from django import forms
from django.core.validators import DecimalValidator
from django.forms.widgets import SelectDateWidget
from .models import Expense
from django.core.validators import MinValueValidator
from decimal import Decimal

class InvoiceForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    company_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    description = forms.ChoiceField(choices=[
        ('resource_utilization', 'Resource Utilization Charge'),
        ('resource_recruitment', 'Resource Recruitment Charge'),
    ])
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        error_messages={
            'min_value': 'Amount must be greater than 0'
        }
    )
    gst_applicable = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')])


class ReceiptForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date'
            }
        )
    )
    name = forms.CharField(max_length=100)
    batch = forms.CharField(max_length=50)
    course = forms.CharField(max_length=100)
    DESCRIPTION_CHOICES = [
        ('fees', 'Fees'),
    ]
    description = forms.ChoiceField(choices=DESCRIPTION_CHOICES, label="Description")
    
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        error_messages={
            'min_value': 'Amount must be greater than 0'
        }
    )
    gst_applicable = forms.ChoiceField(choices=[('yes', 'Yes'), ('no', 'No')])

from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'party', 'particulars', 'invoice_number', 'amount', 'bank_or_cash']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


        
