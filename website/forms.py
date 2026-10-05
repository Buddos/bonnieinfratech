from django import forms
from django.contrib.auth.models import User
from .models import ContactMessage, OrderInquiry, Product

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Full Name', 'class': 'form-control', 'required': True}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email Address', 'class': 'form-control', 'required': True}),
            'phone': forms.TextInput(attrs={'placeholder': 'Your Phone Number (Optional)', 'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'How can we help you?', 'rows': 4, 'class': 'form-control', 'required': True}),
        }

class OrderInquiryForm(forms.ModelForm):
    class Meta:
        model = OrderInquiry
        fields = ['product_name', 'customer_name', 'customer_phone', 'customer_email', 'notes']
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control', 'required': True}),
            'customer_phone': forms.TextInput(attrs={'placeholder': 'Phone Number (for M-Pesa / Call)', 'class': 'form-control', 'required': True}),
            'customer_email': forms.EmailInput(attrs={'placeholder': 'Email Address (optional)', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'placeholder': 'Delivery location or specific request...', 'rows': 3, 'class': 'form-control'}),
        }

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        confirm_pwd = cleaned_data.get('confirm_password')

        if pwd and confirm_pwd and pwd != confirm_pwd:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'in_stock', 'featured']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product Name', 'class': 'form-control', 'required': True}),
            'description': forms.Textarea(attrs={'placeholder': 'Product Description', 'rows': 3, 'class': 'form-control', 'required': True}),
            'price': forms.NumberInput(attrs={'placeholder': 'Price (KSh)', 'class': 'form-control', 'step': '0.01'}),
            'category': forms.TextInput(attrs={'placeholder': 'Category (e.g. Routers, Cables)', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
