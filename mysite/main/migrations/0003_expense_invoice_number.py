# Generated by Django 5.1.2 on 2024-10-19 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_expense'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='invoice_number',
            field=models.CharField(default='N/A', max_length=20),
        ),
    ]