from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Lead(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    status = models.CharField(
        max_length=50,
        choices=[("New", "New"), ("Contacted", "Contacted"), ("Converted", "Converted")],
        default="New"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_issued = models.DateField()
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Paid", "Paid"), ("Overdue", "Overdue")],
        default="Pending"
    )

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client.name}"
    

# Task Management


import uuid

class Task(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    task_id = models.AutoField(primary_key=True)  # Automatically generates a sequential ID
    task_name = models.CharField(max_length=40)
    date_issued = models.DateField(null=True)  # Make this field nullable
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Overdue", "Overdue")],
        default="Pending"
    )

    def __str__(self):
        return f"Task {self.task_id} - {self.client.name}"
    
# Product Management

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)  # Ensure default is 0
    category = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    reorder_level = models.PositiveIntegerField(default=0)  # Ensure default is 0 for reorder level
    stock_balance = models.PositiveIntegerField(default=0)  # Ensure stock_balance starts at 0

    def __str__(self):
        return self.name

    def update_stock_balance(self, stock_in, stock_out):
        """Method to calculate stock balance"""
        if self.stock_quantity is None:
            self.stock_quantity = 0  # Fallback to 0 if None
        if stock_in is None:
            stock_in = 0  # Fallback to 0 if None
        if stock_out is None:
            stock_out = 0  # Fallback to 0 if None
        
        self.stock_balance = self.stock_quantity + stock_in - stock_out
        self.stock_quantity += stock_in - stock_out
        self.save()
