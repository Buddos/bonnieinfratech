from django.contrib import admin
from .models import Product, Service, ContactMessage, OrderInquiry

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock', 'featured', 'created_at')
    list_filter = ('category', 'in_stock', 'featured')
    search_fields = ('name', 'description')
    list_editable = ('in_stock', 'featured')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order', 'created_at')
    list_editable = ('order',)
    search_fields = ('title', 'description')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_read',)

@admin.register(OrderInquiry)
class OrderInquiryAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'customer_name', 'customer_phone', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone', 'customer_email', 'product_name')
    list_editable = ('status',)
