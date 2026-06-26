from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    specifications = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

# Add this alongside your other models
class SupportTicket(models.Model):
    TICKET_TYPES = (
        ('TECH', 'Technical Inquiry 🧠'),
        ('RMA', 'Warranty Return (RMA) 🌸'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Processing Request ✨'),
        ('APPROVED', 'Approved / Shipping Label Ready 🎀'),
        ('RESOLVED', 'Completed 💕'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=4, choices=TICKET_TYPES, default='TECH')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_ticket_type_display()} - {self.subject}"
