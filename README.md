**## Small Business CRM**

## Overview
Small Business CRM is a lightweight, offline Customer Relationship Management (CRM) system tailored for small businesses that do not operate through an e-commerce platform but require an organized method for managing clients, leads, sales, products, and tasks.

This system helps business owners efficiently manage operations by providing tools to handle invoices, track product sales, manage stock, and view insightful reports within a user-friendly interface.

### Technologies Used
- **Backend:** Django 5.1.5
- **Database:** SQLite3
- **Frontend:** HTML, CSS, Bootstrap 4

### User Roles
- **Admin (Superuser):** Manages system settings, users, and social accounts.
- **User (Business Owner):** Manages clients, leads, sales, tasks, and products.

---

## Project Scenario

### Actors & Their Roles

#### 1. Admin (Superuser)
- Manages user accounts (add, modify, and delete users).
- Controls system settings and social accounts.
- Uses Django's built-in admin panel for advanced management.

#### 2. User (Business Owner)
- Logs in and manages daily business activities.
- Handles clients, leads, sales (invoices & payments), products, and tasks.
- Tracks bestselling products and manages stock.
- Uses the search bar to quickly find clients, leads, invoices, and products.
- Views dashboard statistics for business insights.
- Updates their profile (but cannot delete it).

---

## Key Features & Functionalities

### 1. User Authentication & Profile Management
- Secure login/sign-in system.
- Users can update their profile but cannot delete it.

### 2. Client & Lead Management
- Add, edit, view, and delete clients.
- Store and track potential customers (leads).
- Manage lead statuses and follow-ups.

### 3. Sales & Invoice Management
- Create, edit, view, and delete invoices & payments.
- Track pending and completed sales transactions.

### 4. Product Management (New Feature)
- Users can add, view, edit, and delete products.
- Track bestselling products on the dashboard for stock and promotions.
- Manage inventory by monitoring which products are in high demand.

### 5. Task Management
- Assign and track daily business tasks.
- Mark tasks as completed or pending.

### 6. Dashboard & Reports
- View business statistics and key performance insights.
- Get a summary of sales, clients, leads, and product performance.
- See bestselling products and make data-driven decisions.

### 7. Search Functionality (New Feature)
- Users can now search for clients, leads, invoices, and products quickly.
- Helps in faster data retrieval and improves efficiency.

### 8. Admin Panel (Django Admin)
- Manages users and settings.
- Can delete user accounts if necessary.
- Handles system configurations.

### 9. File Import Functionality (New Feature)
- Users can import files (CSV/Excel) to automate client, lead, and invoice management.
- Saves time by bulk uploading data instead of manual entry.

### 10. Stock Notifications (New Feature)
- System alerts users when stock falls below 100 units.
- Provides notifications for overdue and pending tasks.

---

## Use Case Example

### Scenario: A Small Retail Store Owner Using the CRM
A local retail shop owner wants to keep track of customers, payments, and product sales. Since they do not have an online store, they need a simple yet effective system to manage everything from client details to inventory and invoices.

1. **Admin** registers the business owner as a user.
2. **User** logs in, adds clients and leads, and records sales transactions.
3. **User** checks the dashboard for sales performance and bestselling products to plan restocking and promotions.
4. **User** searches for specific clients, invoices, or products to update information quickly.
5. **User** assigns daily tasks and tracks their completion.
6. **System** notifies the user when stock is low or tasks are overdue.
7. **Admin** oversees user activity and system settings from the Django admin panel.

This CRM system provides a well-organized solution for small businesses looking to manage offline sales, customers, and inventory efficiently without needing an online platform.

---

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/rahiltrivedi/small-business-crm.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd small-business-crm
   ```

3. **Create and Activate Virtual Environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # For Windows: env\Scripts\activate
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Apply Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

---

## Conclusion
Small Business CRM is designed to simplify client and product management for offline businesses. With features like file import automation, stock alerts, and task notifications, it provides an efficient and user-friendly approach to managing everyday business activities.

**
