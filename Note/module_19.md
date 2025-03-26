# **Module 19: Introduction to Django REST Framework and Project Setup**

This module introduces the **Django REST Framework (DRF)**, a powerful toolkit for building APIs in Django. We’ll set up a new project called **PhiMart**, a simple e-commerce application, and establish the foundation with custom user models, necessary models, and tools like the debug toolbar and fixtures.

---

## **19.1 🌟 Intro to DRF**

### **What Is DRF?**
- Until now, we’ve used Django’s **MVT (Model-View-Template)** pattern, where the backend renders HTML for the frontend.  
- Modern applications often separate the **backend** (data and logic) and **frontend** (UI), using frameworks like React or Vue.js for the frontend.  
- To connect these, we need **APIs** (Application Programming Interfaces), which allow the frontend to request data from the backend.  
- **Django REST Framework (DRF)** extends Django to build these APIs easily, handling data serialization (converting models to JSON) and request/response management.

### **Why Use DRF?** ✅  
- Simplifies API creation with built-in tools for authentication, serialization, and routing.  
- Supports modern web standards (e.g., RESTful APIs).  
- Integrates seamlessly with Django’s ORM and authentication system.

---

## **19.2 📋 PhiMart Requirement Analysis**

### **Project Overview**
- **PhiMart** is our DRF-based e-commerce project, featuring users, products, carts, and orders.  
- Proper planning prevents issues like database resets (as seen in our task management project).  

### **Documentation Goals**
- Define **endpoints** (API URLs), **models** (database tables), and their **relationships** clearly.  
- Ensure both backend and frontend developers understand the system.  

### **Key Concepts**
- **Endpoints**: URLs like `/api/products/` that trigger backend functions based on **HTTP methods**:  
  - `GET`: Retrieve data (e.g., list products).  
  - `POST`: Create data (e.g., add a product).  
  - `DELETE`: Remove data.  
  - `PATCH`: Update data partially.  
- **Models**: Tables like `User`, `Product`, and `Order`, with relationships (e.g., foreign keys).  

### **Example Plan**
- **Endpoints**: `/api/users/`, `/api/products/`, `/api/orders/`.  
- **Models**: User (authentication), Product (items), Order (purchases).  
- **Relationships**: A `Product` belongs to a `Category`, an `Order` links to a `User`.

---

## **19.3 🚀 Setup Project**

### **Step-by-Step Setup**
1. **Create Virtual Environment**  
   ```bash
   python -m venv .phi_env
   ```
   - `.phi_env`: Hidden folder (good practice with `.`). Activate it: `.phi_env/Scripts/activate` (Windows) or `source .phi_env/bin/activate` (Linux/Mac).  

2. **Install Dependencies**  
   ```bash
   pip install --upgrade pip
   pip install django
   ```

3. **Start Project**  
   ```bash
   django-admin startproject phi_mart .
   ```
   - `phi_mart`: Project directory. `.` creates it in the current folder.

4. **Create Apps**  
   ```bash
   django-admin startapp users
   django-admin startapp order
   django-admin startapp product
   django-admin startapp api
   ```
   - Apps: `users` (authentication), `order` (orders/carts), `product` (items), `api` (common API logic).

5. **Update `settings.py`**  
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'users',
       'order',
       'product',
       'api',
   ]
   ```

6. **Install DRF**  
   ```bash
   pip install djangorestframework
   ```
   - Add to `INSTALLED_APPS`:  
     ```python
     INSTALLED_APPS += ['rest_framework']
     ```

7. **Update `urls.py`**  
   ```python
   from django.contrib import admin
   from django.urls import path, include

   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
   ]
   ```

8. **Generate `requirements.txt`**  
   ```bash
   pip freeze > requirements.txt
   ```
   - Lists all installed packages (e.g., `django==4.x.x`, `djangorestframework==3.x.x`).

- **Detailed Explanation** ✅  
  - **Virtual Environment**: Isolates project dependencies. `.phi_env` keeps it hidden.  
  - **Apps**: Modularize the project. `api` might handle shared API logic.  
  - **DRF**: Adds API-building tools. `api-auth/` provides DRF’s built-in authentication views (e.g., login page).  
  - **`requirements.txt`**: Ensures consistent setup across machines.

---

## **19.4 🔑 Customizing User Model with Email-Based Authentication**

### **Why Customize?**
- Default `User` uses `username`. We want **email-based authentication** without `username`.  

#### **users/models.py**
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None  # Disable username
    email = models.EmailField(unique=True)  # Primary identifier
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'  # Login with email
    REQUIRED_FIELDS = []  # No extra required fields

    def __str__(self):
        return self.email
```

#### **users/managers.py**
```python
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)  # Standardize email
        user = self.model(email=email, **extra_fields)  # Create user instance
        user.set_password(password)  # Hash password
        user.save(using=self._db)  # Save to database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Admin access
        extra_fields.setdefault('is_superuser', True)  # Superuser privileges

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email, password, **extra_fields)
```

#### **Updated `users/models.py`**
```python
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()  # Use custom manager

    def __str__(self):
        return self.email
```

#### **users/admin.py**
```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
```

#### **settings.py**
```python
AUTH_USER_MODEL = 'users.User'  # Custom user model
```

- **Detailed Explanation** ✅  
  - **`User` Model**:  
    - `username = None`: Removes the default `username` field.  
    - `email = models.EmailField(unique=True)`: Makes email the unique identifier.  
    - `USERNAME_FIELD = 'email'`: Tells Django to use `email` for login.  
    - `REQUIRED_FIELDS = []`: No extra fields are mandatory (unlike default `User`, which requires `email` alongside `username`).  
  - **`CustomUserManager`**:  
    - Replaces the default manager because `USERNAME_FIELD` changed.  
    - `create_user`: Ensures email is provided, normalizes it (e.g., `EXAMPLE@GMAIL.COM` → `example@gmail.com`), hashes the password, and saves the user.  
    - `create_superuser`: Adds `is_staff` and `is_superuser` flags for admin access.  
  - **`objects = CustomUserManager()`**: Links the manager to the model.  
  - **Admin**: Customizes the admin interface to show `email` instead of `username` and include new fields.  
  - **`AUTH_USER_MODEL`**: Registers `User` as the default model. Must be set before migrations.

---

## **19.5 🛠️ Creating Necessary Models**

### **PhiMart Models**
- Define models for products, carts, and orders.

#### **product/models.py**
```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/images/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
```

#### **order/models.py**
```python
from django.db import models
from users.models import User
from product.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    PENDING = 'Pending'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
```

- **Detailed Explanation** ✅  
  - **`Category`**: Stores product categories (e.g., “Electronics”).  
  - **`Product`**:  
    - `price`: Uses `DecimalField` for precise currency values.  
    - `category`: Links to `Category` (deletes products if category is deleted).  
    - `auto_now_add`/`auto_now`: Timestamps creation and updates.  
  - **`Cart`**: One cart per user (`OneToOneField`).  
  - **`CartItem`**: Links products to a cart with quantities.  
  - **`Order`**: Tracks user orders with a status (e.g., “Pending”).  
  - **`OrderItem`**: Details items in an order, storing price at purchase time.  
  - **Database**: Uses SQLite (default). Viewable with tools like the “SQLite” VSCode extension.

---

## **19.6 🛠️ Setup Debug Toolbar & Add Dummy Data Using Fixtures**

### **Debug Toolbar**
- **Install**: Follow [django-debug-toolbar docs](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html).  
```bash
pip install django-debug-toolbar
```
- **Configure `settings.py`**:
```python
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']
```
- **Configure `urls.py`**:
```python
from django.conf import settings
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```
- **Explanation**: Adds a toolbar to debug requests, queries, and performance in development.

### **Fixtures for Dummy Data**
#### **fixtures/product_data.json**
```json
[
  {
    "model": "product.category",
    "pk": 1,
    "fields": {
      "name": "Electronics",
      "description": "Devices and gadgets"
    }
  },
  {
    "model": "product.category",
    "pk": 2,
    "fields": {
      "name": "Fashion",
      "description": "Clothing and accessories"
    }
  },
  {
    "model": "product.category",
    "pk": 3,
    "fields": {
      "name": "Home Appliances",
      "description": "Appliances for home use"
    }
  },
  {
    "model": "product.category",
    "pk": 4,
    "fields": {
      "name": "Books",
      "description": "Books and educational materials"
    }
  }
]
```
#### **Load Data**
```bash
python manage.py loaddata fixtures/product_data.json
```
- **Detailed Explanation** ✅  
  - **Debug Toolbar**: Helps debug API performance (e.g., SQL queries). Requires `DEBUG = True`.  
  - **Fixtures**:  
    - `product_data.json`: Defines dummy `Category` data in JSON format. Each entry specifies the model, primary key (`pk`), and field values.  
    - `loaddata`: Imports the JSON into the database, creating the specified categories.  
  - **Why Fixtures?**: Unlike `Faker` (used previously), fixtures provide static, predictable data for testing.

---

# **✅ Final Summary**

1. **Intro to DRF**: Shift from MVT to API-driven development with DRF.  
2. **PhiMart Analysis**: Planned endpoints and models for an e-commerce app.  
3. **Project Setup**: Created `phi_mart` with apps and DRF.  
4. **Custom User**: Replaced `username` with `email` using a custom model and manager.  
5. **Models**: Defined `Category`, `Product`, `Cart`, and `Order` structures.  
6. **Debug & Fixtures**: Added debugging tools and dummy data.  

This module sets up a solid foundation for building PhiMart with DRF, ready for API development! 🌟