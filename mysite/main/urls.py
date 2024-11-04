from django.urls import path
from .views import home, invoice, receipt, view_expenses, add_expenses, accounts, manage, profile, logout, create_invoice,create_receipt

urlpatterns = [
    path('', home, name='dashboard'),
    path('invoice/', invoice, name='invoice'),
    path('receipt/', receipt, name='receipt'),
    path('view_expenses/', view_expenses, name='view_expenses'),
    path('add_expenses/', add_expenses, name='add_expenses'),
    path('accounts/', accounts, name='accounts'),
    path('manage/', manage, name='manage'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout'),
    path('create-invoice/', create_invoice, name='invoice'),
    path('create-receipt/', create_receipt, name='receipt'),
    path('add-expense/', add_expenses, name='add_expenses'),
    path('view-expenses/', view_expenses, name='view_expenses'),
]

