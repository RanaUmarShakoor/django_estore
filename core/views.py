from django.templatetags.static import static
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    UserUpdateForm,
    CustomPasswordChangeForm
)

from .models import *

def index_view(request):
    featured_products = Product.objects.order_by('id')[:4]  # Randomly pick 4 products
    return render(request, "core/index.html", {
        'featured_products': featured_products,
    })

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = CustomAuthenticationForm()

    return render(request, "core/login.html", {
        'form': form,
    })

def logout_view(request):
    logout(request)
    return redirect('index')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()

    return render(request, "core/signup.html", {
        'form': form
    })

@login_required
def profile_view(request):
    user = request.user

    orders = Order.objects.filter(customer=user)

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    pfp = user.profile_picture

    return render(request, 'core/profile.html', {
        'user': user,
        'page_obj': page_obj,
        'pfp_url': pfp.url if pfp else static('core/img/profile_empty.png')
    })

@login_required
def profile_edit_view(request):
    user = request.user

    user_form = None
    password_form = None

    if request.method == 'POST':
        if 'update_info' in request.POST:
            user_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect('profile_edit')
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Keeps the user logged in after password change
                return redirect('profile_edit')
            else:
                messages.error(request, 'Please correct the errors below.')

    if user_form is None:
        user_form = UserUpdateForm(instance=request.user)

    if password_form is None:
        password_form = CustomPasswordChangeForm(user=request.user)

    pfp = user.profile_picture
    return render(request, 'core/profile_edit.html', {
        'user': user,
        'user_form': user_form,
        'password_form': password_form,
        'pfp_url': pfp.url if pfp else static('core/img/profile_empty.png')
    })

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []

    total_price = 0

    for product in products:
        qty = cart[str(product.id)]
        price = qty * product.price
        total_price += price
        cart_items.append((
            product,
            qty,
            price
        ))

    return render(request, 'core/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'core/product.html', {
        'product': product
    })

def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Search by title
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(title__icontains=search_query)

    # Filter by category
    category_id = request.GET.get('category')
    # category_id = str(category_id).strip() or None
    if category_id:
        products = products.filter(category_id=category_id)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'popularity':
        products = products.order_by('-id')  # Dummy popularity sorting, for example

    layout = request.GET.get('layout', 'grid')

    # Pagination
    paginator = Paginator(products, 6)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/product_list.html', {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_sort_by': sort_by,
        'layout': layout,
        'next_layout': 'grid' if layout == 'list' else 'list' 
    })

def thanks_view(request):
    return render(request, 'core/thanks.html', {})

@login_required
def order_details_view(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )
    order_lines = order.order_lines.all()

    return render(request, 'core/order_details.html', {
        'order': order,
        'order_lines': order_lines,
    })


# -------------------------


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    # Get the quantity from the POST data
    quantity = int(request.POST.get('quantity', 1))
    existing_quantity = cart.get(str(product_id), 0)
    new_quantity = existing_quantity + quantity

    # Check if the new quantity exceeds the available stock
    if new_quantity > product.stock:
        messages.error(request, f'Cannot add more than {product.stock} units of {product.title}.')
    else:
        cart[str(product_id)] = new_quantity
        request.session['cart'] = cart
        messages.success(request, f'{quantity} units of {product.title} added to cart!')

    return redirect('product', slug=product.slug)
    
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        delta = int(request.POST.get('delta'))
        cart = request.session.get('cart', {})

        if product_id in cart:
            product = get_object_or_404(Product, id=product_id)
            new_quantity = cart[product_id] + delta

            if new_quantity > product.stock:
                messages.error(request, f'Cannot add more than {product.stock} units of {product.title}.')
            elif new_quantity <= 0:
                cart.pop(product_id)
            else:
                cart[product_id] = new_quantity

            request.session['cart'] = cart
        else:
            messages.error(request, 'Product not found in cart.')

    return redirect('cart')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        cart.pop(str(product_id))
    request.session['cart'] = cart
    return redirect('cart')



# -----------------------------------------

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')

    # Validate stock for all items in the cart
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        if quantity > product.stock:
            messages.error(request, f'Not enough stock for {product.title}. Available: {product.stock}.')
            return redirect('cart_view')

    # Create Order
    order = Order.objects.create(customer=request.user, total_amount=0)

    # Create OrderLines and update stock
    total_amount = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        OrderLine.objects.create(order=order, product=product, quantity=quantity, unit_price=product.price)
        product.stock -= quantity
        product.save()
        total_amount += product.price * quantity

    # Update the total amount of the order
    order.total_amount = total_amount
    order.save()

    # Reset the cart
    request.session['cart'] = {}

    # Redirect to a success page
    return redirect('thanks')
