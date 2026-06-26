from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product

# Update your homepage index view inside app_1/views.py
def index(request):
    # Grab the selected category filter choice from the browser URL address bar
    category_slug = request.GET.get('category')
    
    if category_slug:
        # Filter products that match this specific category slug code parameter
        products = Product.objects.filter(category__slug=category_slug)
    else:
        # Fallback to fetching all items if no filter selection exists
        products = Product.objects.all()
        
    context = {
        'products': products
    }
    return render(request, 'index.html', context)


# 2. Registration Logic
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Simple Kawaii Error Validations
        if password != password_confirm:
            messages.error(request, "Oops! Passwords do not match! 💕")
            return render(request, 'register.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "Oh noes! That username is already taken! 🌸")
            return render(request, 'register.html')
            
        # Create user and log them in immediately
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f"Welcome to the family, {username}! ✨")
        return redirect('index')
        
    return render(request, 'register.html')

# 3. Login Logic
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in safely! 🥰")
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password! 👉👈")
            return render(request, 'login.html')
            
    return render(request, 'login.html')

# 4. Logout Logic
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully. See you soon! 🌸")
    return redirect('index')

from django.shortcuts import get_object_or_404

# 1. View Cart Page
def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    # Fetch details for each item currently stored in session cart
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total_price += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })
        
    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)

# 2. Add Item to Cart Action
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    # Convert ID to string because session JSON keys must be strings
    pid_str = str(product_id)
    
    # Increment quantity or add new item
    if pid_str in cart:
        cart[pid_str] += 1
    else:
        cart[pid_str] = 1
        
    request.session['cart'] = cart
    messages.success(request, "Added to your kawaii bundle! 🛍️")
    return redirect('index')

# 3. Clear Whole Cart Action
def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']
    messages.info(request, "Your cart is cleared! 🧹")
    return redirect('cart_view')

# 4. Custom PC Builder Simulator
def builder_view(request):
    products = Product.objects.all()
    
    # Filter products into separate lists for easy dropdown selection
    cpus = products.filter(category__name__icontains='cpu') or products.filter(name__icontains='cpu')
    gpus = products.filter(category__name__icontains='graphics') or products.filter(name__icontains='rtx') or products.filter(name__icontains='rx')
    cases = products.filter(category__name__icontains='case') or products.filter(name__icontains='case')
    
    # Fallback: if you haven't made those specific categories yet, just show all products in the selectors
    context = {
        'cpus': cpus if cpus.exists() else products,
        'gpus': gpus if gpus.exists() else products,
        'cases': cases if cases.exists() else products,
    }
    
    return render(request, 'builder.html', context)

from django.contrib import messages

# 5. Order Checkout System Processing View
def checkout_view(request):
    cart = request.session.get('cart', {})
    
    # If the user tries to checkout with an empty cart, boot them back to home
    if not cart:
        messages.warning(request, "Your shopping cart is completely empty! 🛒")
        return redirect('index')
    
    # Calculate totals for the checkout summary receipt invoice view
    cart_items = []
    grand_total = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total_price = product.price * quantity
            grand_total += total_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': total_price
            })
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        # This simulates order processing saving details
        # In a real app, you would save an Order model entry here
        request.session['cart'] = {}  # Empty out the shopping basket memory
        messages.success(request, "🎉 Yay! Your custom hardware order has been successfully placed!")
        return redirect('index')

    context = {
        'cart_items': cart_items,
        'grand_total': grand_total,
    }
    return render(request, 'checkout.html', context)

from .models import SupportTicket

# 6. Tech Support & RMA Request Module
def support_view(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to open a support desk case! 💕")
        return redirect('login')

    # Fetch all past tickets logged by this authenticated user
    tickets = SupportTicket.objects.filter(user=request.user).order_by("-created_at")


    if request.method == 'POST':
        ticket_type = request.POST.get('ticket_type')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        SupportTicket.objects.create(
            user=request.user,
            ticket_type=ticket_type,
            subject=subject,
            message=message
        )
        messages.success(request, "🌸 Your help request/RMA ticket has been safely transmitted to our team!")
        return redirect('support_view')

    return render(request, 'support.html', {'tickets': tickets})

# View to remove a single specific item from the cart basket memory
def remove_cart_item_view(request, product_id):
    cart = request.session.get('cart', {})
    
    # Convert product_id to string since session keys are strings
    prod_id_str = str(product_id)
    
    if prod_id_str in cart:
        del cart[prod_id_str] # Delete only this item!
        request.session['cart'] = cart # Save the updated cart back to memory
        messages.success(request, "🌸 Item successfully removed from your cart!")
        
    return redirect('cart_view')
