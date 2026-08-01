from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CheckoutForm, RegistrationForm
from .models import Cart, CartItem, Category, Order, OrderItem, Product


# Helper functions

def get_or_create_cart(request):
    cart = None
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


def home(request):
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(is_featured=True)[:6]
    more_products = Product.objects.exclude(is_featured=True)[:8]
    return render(request, 'store/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'more_products': more_products,
    })


def offers_page(request):
    featured_products = Product.objects.filter(is_featured=True)[:6]
    return render(request, 'store/offers.html', {
        'featured_products': featured_products,
    })


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'store/product_detail.html', {'product': product})


def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_or_create_cart(request)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    else:
        item.quantity = 1
    item.save()
    messages.success(request, f'{product.name} added to your cart.')
    return redirect(request.META.get('HTTP_REFERER', reverse('home')))


@login_required(login_url='login')
def update_cart(request, item_id):
    if request.method != 'POST':
        return redirect('cart')
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    return redirect('cart')


@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.info(request, 'Your cart is empty.')
        return redirect('cart')
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
            cart.items.all().delete()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, 'store/checkout.html', {'form': form, 'cart': cart})


@login_required(login_url='login')
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required(login_url='login')
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required(login_url='login')
def profile(request):
    return render(request, 'store/profile.html', {'user': request.user})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('home')
    if request.user.is_authenticated:
        return redirect(next_url)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if not form.is_valid():
            username = request.POST.get('username', '').strip()
            if '@' in username:
                try:
                    user = User.objects.get(email=username)
                    data = request.POST.copy()
                    data['username'] = user.username
                    form = AuthenticationForm(request, data=data)
                except User.DoesNotExist:
                    form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect(next_url)
        else:
            messages.error(request, 'Login failed. Please check your username/email and password.')
    else:
        form = AuthenticationForm(request)

    return render(request, 'store/login.html', {
        'form': form,
        'next': next_url,
    })


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required(login_url='login')
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    orders = Order.objects.all().order_by('-created_at')[:10]
    products = Product.objects.all()[:10]
    users = User.objects.all()[:10]
    return render(request, 'store/admin_dashboard.html', {
        'orders': orders,
        'products': products,
        'users': users,
    })
