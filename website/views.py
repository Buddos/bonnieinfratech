import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import Product, Service, ContactMessage, OrderInquiry
from .forms import ContactForm, OrderInquiryForm, UserRegisterForm, ProductForm

def serialize_product(p):
    cat = (p.category or 'networking').lower()
    if 'router' in cat or 'cable' in cat or 'networking' in cat:
        norm_cat = 'networking'
    elif 'access' in cat or 'periph' in cat:
        norm_cat = 'accessories'
    elif 'soft' in cat:
        norm_cat = 'software'
    elif 'sec' in cat or 'firewall' in cat:
        norm_cat = 'security'
    else:
        norm_cat = cat

    return {
        'id': p.id,
        'name': p.name,
        'category': norm_cat,
        'description': p.description,
        'price': float(p.price) if p.price else 0,
        'price_formatted': f"KES {int(p.price):,}" if p.price else "KES 0",
        'image': p.display_image,
        'rating': 4.8,
        'stock': 15 if p.in_stock else 0,
        'badge': 'bestseller' if p.featured else '',
        'features': [
            "High performance & reliability",
            "Genuine manufacturer warranty",
            "Fast deployment ready"
        ]
    }

def home(request):
    featured_products = Product.objects.filter(in_stock=True)
    services = Service.objects.all()
    form = ContactForm()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent successfully. We will contact you soon.")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors in the contact form.")

    products_json = json.dumps([serialize_product(p) for p in featured_products])

    context = {
        'products': featured_products,
        'products_json': products_json,
        'services': services,
        'contact_form': form,
    }
    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


def services(request):
    services_list = Service.objects.all()
    return render(request, 'services.html', {'services': services_list})


def products(request):
    category = request.GET.get('category')
    query = request.GET.get('q')

    all_products = Product.objects.filter(in_stock=True)

    if category and category.lower() != 'all':
        all_products = all_products.filter(category__icontains=category)
    if query:
        all_products = all_products.filter(name__icontains=query) | all_products.filter(description__icontains=query)

    categories = Product.objects.values_list('category', flat=True).distinct()
    products_json = json.dumps([serialize_product(p) for p in all_products])

    context = {
        'products': all_products,
        'products_json': products_json,
        'categories': categories,
        'current_category': category,
        'query': query,
    }
    return render(request, 'product.html', context)



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for getting in touch! We will get back to you promptly.")
            return redirect('contact')
        else:
            messages.error(request, "There was an error in your submission. Please check the fields.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def order_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_name = request.POST.get('product_name')
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email', '')
        notes = request.POST.get('notes', '')

        product = None
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                product_name = product.name
            except Product.DoesNotExist:
                pass

        if customer_name and customer_phone:
            OrderInquiry.objects.create(
                product=product,
                product_name=product_name or "General Order",
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_email=customer_email,
                notes=notes,
            )
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': f'Thank you {customer_name}! Your order for {product_name} has been placed. We will contact you at {customer_phone}.'})
            messages.success(request, f"Order inquiry for '{product_name}' received! Our team will contact you shortly.")
            return redirect('products')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Please provide your name and phone number.'}, status=400)
            messages.error(request, "Name and phone number are required.")
            return redirect('products')

    return redirect('products')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            next_url = request.GET.get('next') or ('dashboard' if user.is_staff else 'home')
            return redirect(next_url)
        else:
            error = "Invalid username or password. Please try again."

    return render(request, 'login.html', {'error': error})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip() or (email.split('@')[0] if email else '')
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not email or not password:
            messages.error(request, "Email and password are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists. Please login.")
        else:
            # Generate unique username if needed
            orig_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{orig_username}{counter}"
                counter += 1

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.get_full_name() or user.username}!")
            return redirect('home')

    return render(request, 'registration.html')



def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


def is_admin_or_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def admin_dashboard(request):
    # Allows viewing dashboard; if not logged in as staff, redirect to login with prompt
    if not (request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)):
        messages.info(request, "Please log in with admin privileges to view the dashboard.")
        return redirect('/login/?next=/dashboard/')

    all_products = Product.objects.all()
    inquiries = ContactMessage.objects.all()[:10]
    orders = OrderInquiry.objects.all()[:10]

    product_form = ProductForm()
    if request.method == 'POST' and 'add_product' in request.POST:
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Product added successfully!")
            return redirect('dashboard')

    context = {
        'products': all_products,
        'inquiries': inquiries,
        'orders': orders,
        'total_products': all_products.count(),
        'total_inquiries': ContactMessage.objects.count(),
        'total_orders': OrderInquiry.objects.count(),
        'product_form': product_form,
    }
    return render(request, 'admin.html', context)


def privacy(request):
    return render(request, 'privacy.html')


def terms(request):
    return render(request, 'terms.html')


def cookies(request):
    return render(request, 'cookies.html')


def sitemap(request):
    return render(request, 'sitemap.html')
