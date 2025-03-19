from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count, Sum
import json
from django.utils.timezone import now
from django.db.models.functions import TruncDay
from django.db.models import Q


from .forms import SignUpForm, UserForm, ProfileForm, ClientForm, LeadForm, InvoiceForm, TaskForm, ProductForm
from .models import Client, Lead, Invoice, Task, Product

# Home Views
class HomeView(TemplateView):
    template_name = 'common/home.html'

class FrontView(TemplateView):
    template_name = 'common/front.html'

from django.db.models import Q
from django.shortcuts import render
from .models import Client, Lead, Invoice, Product
from django.db.models import Sum, Count
from django.db.models.functions import TruncDay
import json
from django.urls import reverse_lazy
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'common/dashboard.html'
    login_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the search query from GET request
        query = self.request.GET.get('q', '').strip()

       
        context['total_clients'] = Client.objects.count()  # Ensure fresh count
        context['total_leads'] = Lead.objects.count()
        context['total_revenue'] = Invoice.objects.aggregate(Sum('amount'))['amount__sum'] or 0

        # Fetch products with low stock (less than 100)
        low_stock_products = Product.objects.filter(stock_quantity__lt=100)
        context['low_stock_products'] = low_stock_products
        context['low_stock_count'] = low_stock_products.count()
        
        # Task Notifications
        today = now().date()
        context['overdue_tasks'] = Task.objects.filter(due_date__lt=today, status="Overdue")
        context['overdue_count'] = context['overdue_tasks'].count()

        context['pending_tasks'] = Task.objects.filter(status="Pending")
        context['pending_count'] = context['pending_tasks'].count()

        # Total Notification Count
        context['total_notifications'] = (
            context['low_stock_count'] +
            context['overdue_count'] +
            context['pending_count']
        )


        # Initialize the no_results flag to False
        context['no_results'] = False

        # Perform search if query exists
        if query:
            # Determine if the query is numeric (to handle number fields like amount, phone number, etc.)
            is_numeric = query.isdigit()  # Checks if the query is numeric (phone number, amount, etc.)

            # Search Clients (by name, email, etc.)
            context['clients'] = Client.objects.filter(
                Q(name__icontains=query) | 
                Q(email__icontains=query) |
                Q(id__icontains=query) |
                (Q(phone__icontains=query) if not is_numeric else Q(phone__iexact=query))  # Handling phone number search
            )
            
            # Search Leads (by name, email, etc.)
            context['leads'] = Lead.objects.filter(
                Q(name__icontains=query) | 
                Q(email__icontains=query) |
                Q(id__icontains=query) |
                (Q(phone__icontains=query) if not is_numeric else Q(phone__iexact=query))  # Handling phone number search
            )
            
            # Search Invoices (by invoice_number, client, dates, etc.)
            context['invoices'] = Invoice.objects.filter(
                Q(invoice_number__icontains=query) | 
                Q(client__name__icontains=query) |
                Q(date_issued__icontains=query) |
                Q(due_date__icontains=query) |
                (Q(amount__icontains=query) if not is_numeric else Q(amount=query))  # Handling amount search
            )
            
            # Search Products (by name, description, etc.)
            context['products'] = Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(id__icontains=query)
            )

            # If no results are found for any of the queries, set no_results flag to True
            if not (context['clients'] or context['leads'] or context['invoices'] or context['products']):
                context['no_results'] = True

        else:
            # If no search query, show products with images for the carousel
            context['clients'] = []
            context['leads'] = []
            context['invoices'] = []
            context['products'] = Product.objects.filter(image__isnull=False)[:5]  # Always show 5 products with images

        # Prepare the context data for charts (same as before)
        client_growth = Client.objects.annotate(day=TruncDay('created_at')) \
            .values('day').annotate(count=Count('id')).order_by('day')
        client_labels = [entry['day'].strftime('%d %b') for entry in client_growth]
        client_values = [entry['count'] for entry in client_growth]

        lead_growth = Lead.objects.annotate(day=TruncDay('created_at')) \
            .values('day').annotate(count=Count('id')).order_by('day')
        lead_labels = [entry['day'].strftime('%d %b') for entry in lead_growth]
        lead_values = [entry['count'] for entry in lead_growth]

        revenue_data = Invoice.objects.annotate(day=TruncDay('date_issued')) \
            .values('day').annotate(total=Sum('amount')).order_by('day')
        revenue_labels = [entry['day'].strftime('%d %b') for entry in revenue_data]
        revenue_values = [float(entry['total']) for entry in revenue_data]

        # Convert Data to JSON for Chart.js
        context['client_growth_labels'] = json.dumps(client_labels)
        context['client_growth_values'] = json.dumps(client_values)
        context['lead_growth_labels'] = json.dumps(lead_labels)
        context['lead_growth_values'] = json.dumps(lead_values)
        context['revenue_growth_labels'] = json.dumps(revenue_labels)
        context['revenue_growth_values'] = json.dumps(revenue_values)

        return context

class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'common/register.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'common/profile.html'

class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'common/profile-update.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(user_form=user_form, profile_form=profile_form)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# CRUD for Clients
def client_list(request):
    clients = Client.objects.all()
    return render(request, "common/client_list.html", {"clients": clients})

def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("client_list")
    else:
        form = ClientForm()
    return render(request, "common/client_form.html", {"form": form})

def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("client_list")
    else:
        form = ClientForm(instance=client)
    return render(request, "common/client_form.html", {"form": form})

def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == "POST":
        client.delete()
        return redirect("client_list")
    return render(request, "common/client_confirm_delete.html", {"client": client})

# CRUD for Leads
def lead_list(request):
    leads = Lead.objects.all()
    return render(request, "common/lead_list.html", {"leads": leads})

def lead_create(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lead_list")
    else:
        form = LeadForm()
    return render(request, "common/lead_form.html", {"form": form})

def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("lead_list")
    else:
        form = LeadForm(instance=lead)
    return render(request, "common/lead_form.html", {"form": form})

def lead_delete(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    if request.method == "POST":
        lead.delete()
        return redirect("lead_list")
    return render(request, "common/lead_confirm_delete.html", {"lead": lead})

# CRUD for Invoices
def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, "common/invoice_list.html", {"invoices": invoices})

def invoice_create(request):
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("invoice_list")
    else:
        form = InvoiceForm()
    return render(request, "common/invoice_form.html", {"form": form})

def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            form.save()
            return redirect("invoice_list")
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, "common/invoice_form.html", {"form": form})

def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == "POST":
        invoice.delete()
        return redirect("invoice_list")
    return render(request, "common/invoice_confirm_delete.html", {"invoice": invoice})

# Task management

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "common/task_list.html", {"tasks": tasks})

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "common/task_form.html", {"form": form})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "common/task_form.html", {"form": form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "common/task_confirm_delete.html", {"task": task})


# Product Management

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm  # Make sure to create a ProductForm

# Product List View
def product_list(request):
    products = Product.objects.all()  # Get all products
    return render(request, "common/product_list.html", {"products": products})

# Product Create View
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()  # Save the new product
            
            # Handle stock_in and stock_out if present
            stock_in = request.POST.get("stock_in", 0)
            stock_out = request.POST.get("stock_out", 0)
            
            # Convert them to integers
            try:
                stock_in = int(stock_in) if stock_in else 0
                stock_out = int(stock_out) if stock_out else 0
            except ValueError:
                stock_in = stock_out = 0

            # Update stock balance
            product.update_stock_balance(stock_in, stock_out)

            return redirect("product_list")
        else:
            print(form.errors)  # Debug form errors

    else:
        form = ProductForm()

    return render(request, "common/product_form.html", {"form": form})


# Product Edit View (similar logic to create view)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()  # Save the updated product
            
            stock_in = request.POST.get("stock_in", 0)
            stock_out = request.POST.get("stock_out", 0)

            try:
                stock_in = int(stock_in) if stock_in else 0
                stock_out = int(stock_out) if stock_out else 0
            except ValueError:
                stock_in = stock_out = 0

            # Update stock balance
            product.update_stock_balance(stock_in, stock_out)

            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "common/product_form.html", {"form": form})


# Product Delete View
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)  # Get the product by primary key
    if request.method == "POST":
        product.delete()  # Delete the product
        return redirect("product_list")  # Redirect to the product list after deletion
    return render(request, "common/product_confirm_delete.html", {"product": product})

# Product Restock View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductRestockForm, ProductSaleForm # Create a form for restocking

def product_restock(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = ProductRestockForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            product.update_stock(quantity, is_incoming=True)
            return redirect("product_list")  # Redirect to product list after restocking
    else:
        form = ProductRestockForm()
        
    return render(request, "common/product_form.html", {"form": form, "product": product})


# Product Sale View
def product_sale(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = ProductSaleForm(request.POST)  # Create a sale form for input
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            if product.stock_balance() < quantity:
                # Handle case where not enough stock is available
                return render(request, "common/insufficient_stock.html", {"product": product})
            product.update_stock(quantity, is_incoming=False)  # Decrease stock after sale
            return redirect("product_list")  # Redirect to product list after sale
    else:
        form = ProductSaleForm()
        
    return render(request, "common/product_form.html", {"form": form, "product": product})



# Download Buttons

import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import make_naive

def export_clients_excel(request):
    clients = Client.objects.values("name", "email", "phone", "address", "created_at")
    
    # Convert datetime fields to naive if they are timezone-aware
    for client in clients:
        if client["created_at"]:
            client["created_at"] = make_naive(client["created_at"])

    df = pd.DataFrame(clients)
    
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="clients.xlsx"'
    
    df.to_excel(response, index=False)
    return response

def export_leads_excel(request):
    leads = Lead.objects.values("name", "email", "phone", "status", "created_at")
    
    # Convert datetime fields to naive if they are timezone-aware
    for lead in leads:
        if lead["created_at"]:
            lead["created_at"] = make_naive(lead["created_at"])

    df = pd.DataFrame(leads)
    
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="leads.xlsx"'
    
    df.to_excel(response, index=False)
    return response


from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
import os
from .models import Invoice  # ✅ Import Invoice model

def export_invoices_pdf(request):
    invoices = Invoice.objects.all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    # 🔹 Add Company Logo (Optional)
    # logo_path = os.path.join("static", "images", "company_logo.png")  # Adjust if needed
    # if os.path.exists(logo_path):
    #     logo = Image(logo_path, width=150, height=50)
    #     elements.append(logo)

    # 🔹 Invoice Title (Centered & Bold)
    styles = getSampleStyleSheet()
    title_style = styles["Title"]  # Default title style
    title_style.alignment = 1  # 1 = Center
    title_style.fontName = "Helvetica-Bold"

    invoice_title = Paragraph("<b>Invoice List</b>", title_style)
    elements.append(invoice_title)

    # 🔹 Company Name & Header
    company_details = [
        ["Company Name: Esfina Technology and Solution LLP"],
        ["Email: esfinatechnology@proton.me"],
        ["Phone: +91 9316304724"],
    ]
    table = Table(company_details, colWidths=[400])
    table.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.darkblue),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)

    # 🔹 Invoice Title
    # elements.append(Table([["Invoice List"]], colWidths=[400], hAlign="CENTER"))

    # 🔹 Invoice Table Data
    data = [["Invoice #", "Client", "Amount", "Date Issued", "Due Date", "Status"]]
    for invoice in invoices:
        status = invoice.status  # ✅ Uses correct field
        data.append([
            invoice.invoice_number,
            invoice.client.name,
            f"Rs. {invoice.amount:.2f}",
            invoice.date_issued.strftime("%d-%b-%Y"),
            invoice.due_date.strftime("%d-%b-%Y"),
            status,
        ])

    # 🔹 Create Table
    invoice_table = Table(data, colWidths=[80, 120, 80, 80, 80, 80])
    invoice_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(invoice_table)

    # 🔹 Footer
    elements.append(Spacer(1, 50))  # Adjust 50 to increase/decrease gap
    footer_text = """This is a system-generated invoice for record-keeping purposes only. 
    No payment is required.""" 
    """Please contact at esfinatechnology@proton.me for any discrepancies."""
    footer_table = Table([[footer_text]], colWidths=[400])
    footer_table.setStyle(TableStyle([
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.darkgray),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 20),
    ]))
    elements.append(footer_table)

    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename="Invoices.pdf")

# Import function

import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Client, Lead, Invoice
from django.utils.timezone import make_aware
import datetime

def import_clients_excel(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        try:
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                client, created = Client.objects.get_or_create(
                    name=row["name"], 
                    email=row["email"],
                    phone=row["phone"],
                    defaults={"address": row.get("address", ""), "created_at": make_aware(datetime.datetime.now())}
                )
            messages.success(request, "Clients imported successfully!")
        except Exception as e:
            messages.error(request, f"Error importing clients: {e}")
        return redirect("dashboard")  # Redirect to your dashboard

    return render(request, "common/import_clients.html")

def import_leads_excel(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        try:
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                lead, created = Lead.objects.get_or_create(
                    name=row["name"],
                    email=row["email"],
                    phone=row["phone"],
                    defaults={"status": row.get("status", "New"), "created_at": make_aware(datetime.datetime.now())}
                )
            messages.success(request, "Leads imported successfully!")
        except Exception as e:
            messages.error(request, f"Error importing leads: {e}")
        return redirect("dashboard")

    return render(request, "common/import_leads.html")

def import_invoices_excel(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        try:
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                invoice, created = Invoice.objects.get_or_create(
                    invoice_number=row["invoice_number"],
                    client_id=row["client_id"],  # Ensure the client exists
                    amount=row["amount"],
                    date_issued=make_aware(datetime.datetime.strptime(row["date_issued"], "%Y-%m-%d")),
                    due_date=make_aware(datetime.datetime.strptime(row["due_date"], "%Y-%m-%d")),
                    defaults={"status": row.get("status", "Pending")}
                )
            messages.success(request, "Invoices imported successfully!")
        except Exception as e:
            messages.error(request, f"Error importing invoices: {e}")
        return redirect("dashboard")

    return render(request, "common/import_invoices.html")


