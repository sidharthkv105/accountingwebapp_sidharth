from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import InvoiceForm, ReceiptForm
from decimal import Decimal
import os
from .models import DocumentCounter
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader

def home(request):
    return render(request, 'dashboard.html')

def invoice(request):
    return render(request, 'invoice.html')

def receipt(request):
    return render(request, 'receipt.html')

def view_expenses(request):
    return render(request, 'view_expenses.html')

def add_expense(request):
    return render(request, 'add_expense.html')

def accounts(request):
    return render(request, 'accounts.html')

def manage(request):
    return render(request, 'manage.html')

def profile(request):
    return render(request, 'profile.html')

def logout(request):
    return render(request, 'logout.html')

def generate_pdf(invoice_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)

    # Logo image (top right)
    logo_path = "{% static 'images/logo.png' %}"
    logo = ImageReader(logo_path)
    p.drawImage(logo, 450, 750, width=1.5*inch, height=1.5*inch)

    # Main heading (AY TECH) with larger font size
    p.setFont("Helvetica-Bold", 20)
    p.drawString(40, 800, "AY TECH")

    # Company details (below the heading)
    p.setFont("Helvetica", 10)
    p.drawString(40, 780, "1st Floor K A Mammen Arcade Building")
    p.drawString(40, 765, "Pookode Road, Elanthoor")
    p.drawString(40, 750, "Pathanamthitta. PIN: 689643")
    p.drawString(40, 735, "Ph:+91-9074585583")
    p.drawString(40, 720, "contact@aytech.co.in")
    p.drawString(40, 705, "www.aytech.co.in")
    # Heading (centered)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 700, "Invoice")

    p.setFont("Helvetica", 12)

    # Labels (left column)
    p.drawString(100, 640, "Invoice Number:")
    p.drawString(100, 620, "Date:")
    p.drawString(100, 600, "Company Name:")
    p.drawString(100, 580, "Address:")
    p.drawString(100, 560, "Description:")
    p.drawString(100, 540, "Amount:")
    p.drawString(100, 520, "GST:")
    p.drawString(100, 500, "Total:")

    # Values (right column)
    p.drawString(250, 640, f"{invoice_data['invoice_number']}")
    p.drawString(250, 620, f"{invoice_data['date']}")
    p.drawString(250, 600, f"{invoice_data['company_name']}")
    p.drawString(250, 580, f"{invoice_data['address']}")
    p.drawString(250, 560, f"{invoice_data['description']}")
    p.drawString(250, 540, f"{invoice_data['amount']}")
    p.drawString(250, 520, f"{invoice_data['gst_applicable']}")
    p.drawString(250, 500, f"{invoice_data['total']}")
    # Finalize the PDF and close the canvas
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer

def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice_data = form.cleaned_data
            invoice_number = generate_document_number()  # Get the common document number
            invoice_data['invoice_number'] = invoice_number

            # Calculate GST and total
            amount = invoice_data.get('amount', Decimal('0'))
            gst_applicable = invoice_data.get('gst_applicable', 'no')
            gst_rate = Decimal('0.18') if gst_applicable == 'yes' else Decimal('0')
            gst_amount = amount * gst_rate
            total = amount + gst_amount

            # Add total and gst_amount to invoice_data
            invoice_data['gst_amount'] = gst_amount
            invoice_data['total'] = total

            # Generate PDF
            pdf_buffer = generate_pdf(invoice_data)

            # Serve PDF as download
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{invoice_number}.pdf"'
            return response
    else:
        form = InvoiceForm()

    return render(request, 'mysite/invoice.html', {'form': form})

def generate_receipt_pdf(receipt_data):
    # Create a buffer to hold the PDF
    buffer = BytesIO()

    # Create a PDF canvas
    p = canvas.Canvas(buffer, pagesize=A4)

    # Logo image (top right)
    logo_path = "{% static 'images/logo.png' %}"
    if os.path.exists(logo_path):
        logo = ImageReader(logo_path)
        p.drawImage(logo, 450, 750, width=1.5*inch, height=1.5*inch)
    else:
        print(f"Error: Logo file not found at {logo_path}")

    # Main heading (AY TECH) with larger font size
    p.setFont("Helvetica-Bold", 20)
    p.drawString(40, 750, "AY TECH")

    # Company details (below the heading)
    p.setFont("Helvetica", 10)
    p.drawString(40, 730, "1st Floor K A Mammen Arcade Building")
    p.drawString(40, 715, "Pookode Road, Elanthoor")
    p.drawString(40, 700, "Pathanamthitta. PIN: 689643")
    p.drawString(40, 685, "Ph:+91-9074585583")
    p.drawString(40, 670, "contact@aytech.co.in")
    p.drawString(40, 655, "www.aytech.co.in")

    # Receipt heading (centered)
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(300, 620, "Receipt")

    # Arrange receipt details in a structured format
    p.setFont("Helvetica", 12)

    # Labels (left column)
    p.drawString(100, 580, "Receipt Number:")
    p.drawString(100, 560, "Date:")
    p.drawString(100, 540, "Name:")
    p.drawString(100, 520, "Batch:")
    p.drawString(100, 500, "Course:")
    p.drawString(100, 480, "Description:")
    p.drawString(100, 460, "Amount:")
    p.drawString(100, 440, "GST Amount:")
    p.drawString(100, 420, "Total:")

    # Values (right column)
    p.drawString(250, 580, f"{receipt_data['receipt_number']}")
    p.drawString(250, 560, f"{receipt_data['date']}")
    p.drawString(250, 540, f"{receipt_data['name']}")
    p.drawString(250, 520, f"{receipt_data['batch']}")
    p.drawString(250, 500, f"{receipt_data['course']}")
    p.drawString(250, 480, f"{receipt_data['description']}")
    p.drawString(250, 460, f"{receipt_data['amount']}")
    p.drawString(250, 440, f"{receipt_data['gst_amount']}")
    p.drawString(250, 420, f"{receipt_data['total']}")

    # Finalize the PDF and close the canvas
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and return it
    pdf_value = buffer.getvalue()
    buffer.close()
    
    return pdf_value

def create_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            receipt_data = form.cleaned_data
            receipt_number = generate_document_number()  # Get the common document number
            receipt_data['receipt_number'] = receipt_number

            # Calculate GST and total
            amount = receipt_data.get('amount', Decimal('0'))
            gst_applicable = receipt_data.get('gst_applicable', 'no')
            gst_rate = Decimal('0.18') if gst_applicable == 'yes' else Decimal('0')
            gst_amount = amount * gst_rate
            total = amount + gst_amount

            receipt_data['gst_amount'] = gst_amount
            receipt_data['total'] = total

            # Generate the PDF
            pdf_buffer = generate_receipt_pdf(receipt_data)

            # Serve the PDF as a download
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{receipt_number}.pdf"'
            return response
    else:
        form = ReceiptForm()

    return render(request, 'mysite/receipt.html', {'form': form})

def generate_document_number():
    counter = DocumentCounter.objects.first()
    if not counter:
        counter = DocumentCounter.objects.create(last_document_number=0)
    
    # Increment the document number
    new_number = counter.last_document_number + 1
    counter.last_document_number = new_number
    counter.save()

    return f"aytech_ir{new_number:03d}"  # Format: aytech_ir009




from django.shortcuts import render, redirect
from .models import Expense
from .forms import ExpenseForm
from datetime import datetime
import calendar

from django.shortcuts import render, redirect
from .forms import ExpenseForm

def add_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_expenses')  # Redirect to view expenses
    else:
        form = ExpenseForm()
    
    return render(request, 'mysite/add_expenses.html', {'form': form})

def view_expenses(request):
    # Get the current month and year
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Create a list of months for the dropdown with month numbers and names
    months = [(i, calendar.month_name[i]) for i in range(1, 13)]  # (month_number, month_name)

    # Default values for selected month and year, converting to int to handle GET parameters correctly
    selected_month = int(request.GET.get('month', current_month))
    selected_year = int(request.GET.get('year', current_year))

    # Fetch expenses based on selected month and year
    expenses = Expense.objects.filter(date__month=selected_month, date__year=selected_year)

    # Create a list of years for the dropdown (Last 5 years)
    years = range(current_year - 5, current_year + 1)

    context = {
        'expenses': expenses,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'months': months,
        'years': years,
    }

    return render(request, 'mysite/view_expenses.html', context)
