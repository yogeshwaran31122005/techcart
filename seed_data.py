import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product


def ensure_categories():
    electronics, _ = Category.objects.get_or_create(name='Electronics', slug='electronics', defaults={'description': 'Gadgets and tech essentials'})
    fashion, _ = Category.objects.get_or_create(name='Fashion', slug='fashion', defaults={'description': 'Modern clothing and accessories'})
    home, _ = Category.objects.get_or_create(name='Home', slug='home', defaults={'description': 'Comfort and lifestyle products'})
    return electronics, fashion, home


def seed_products(electronics, fashion, home):
    products = [
        {'name': 'TechCart Mobile Phone', 'slug': 'techcart-mobile-phone', 'category': electronics, 'price': 799.99, 'stock': 12, 'description': 'A sleek flagship phone with stunning display and all-day battery.', 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1512496015851-a90fb38ba796?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Aurora Headphones', 'slug': 'aurora-headphones', 'category': electronics, 'price': 149.99, 'stock': 25, 'description': 'Immersive sound with noise cancellation.', 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1511376777868-611b54f68947?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Luma Smart Lamp', 'slug': 'luma-smart-lamp', 'category': home, 'price': 89.50, 'stock': 18, 'description': 'Ambient lighting with smart controls.', 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1491218480215-954275a8b9b1?auto=format&fit=crop&w=900&q=80'},
        {'name': 'North Jacket', 'slug': 'north-jacket', 'category': fashion, 'price': 119.00, 'stock': 12, 'description': 'Weather-ready outerwear for everyday use.', 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Nova Smartwatch', 'slug': 'nova-smartwatch', 'category': electronics, 'price': 199.99, 'stock': 16, 'description': 'Track your wellness and stay connected.', 'is_featured': True, 'image_url': 'https://images.unsplash.com/photo-1511732357994-3b8d9b1be0e5?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Cedar Tote Bag', 'slug': 'cedar-tote-bag', 'category': fashion, 'price': 64.00, 'stock': 20, 'description': 'A sleek everyday tote for work and travel.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Orchid Desk Lamp', 'slug': 'orchid-desk-lamp', 'category': home, 'price': 48.00, 'stock': 22, 'description': 'Soft illumination for focused evenings.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1517705008128-361805f42e86?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Halo Camera', 'slug': 'halo-camera', 'category': electronics, 'price': 349.00, 'stock': 10, 'description': 'Capture crisp memories with a compact body.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1519183071298-a2962f9b63ff?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Sage Sneakers', 'slug': 'sage-sneakers', 'category': fashion, 'price': 88.00, 'stock': 15, 'description': 'Comfortable sneakers for city strolls.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1511381939415-9d6ff75b1397?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Ridge Blender', 'slug': 'ridge-blender', 'category': home, 'price': 74.00, 'stock': 17, 'description': 'Blend smoothies and soups with ease.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1595433562696-06034f56e394?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Aero Wireless Earbuds', 'slug': 'aero-wireless-earbuds', 'category': electronics, 'price': 129.00, 'stock': 24, 'description': 'Crystal-clear sound in a compact design.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Marble Coffee Set', 'slug': 'marble-coffee-set', 'category': home, 'price': 54.00, 'stock': 13, 'description': 'Elevate your morning ritual with refined pieces.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Drift Leather Wallet', 'slug': 'drift-leather-wallet', 'category': fashion, 'price': 59.00, 'stock': 14, 'description': 'Minimal style with premium finishing.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1523785785292-0d67bdd74f5b?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Echo Portable Speaker', 'slug': 'echo-portable-speaker', 'category': electronics, 'price': 109.99, 'stock': 19, 'description': 'Portable audio with rich bass and bold style.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Mira Knit Throw', 'slug': 'mira-knit-throw', 'category': home, 'price': 39.00, 'stock': 21, 'description': 'Soft comfort for colder evenings.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Linen Travel Jacket', 'slug': 'linen-travel-jacket', 'category': fashion, 'price': 97.00, 'stock': 11, 'description': 'Lightweight layers for weekend escapes.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Atlas Tablet', 'slug': 'atlas-tablet', 'category': electronics, 'price': 419.00, 'stock': 9, 'description': 'A balanced tablet for work and play.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Pine Planter Set', 'slug': 'pine-planter-set', 'category': home, 'price': 29.50, 'stock': 16, 'description': 'Bring a fresh touch of greenery indoors.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1498962815851-92a9a580aec5?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Harbor Messenger Bag', 'slug': 'harbor-messenger-bag', 'category': fashion, 'price': 69.00, 'stock': 12, 'description': 'Organized storage with a modern silhouette.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Contour Keyboard', 'slug': 'contour-keyboard', 'category': electronics, 'price': 79.00, 'stock': 18, 'description': 'Comfortable typing with quiet switches.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Atelier Ceramic Bowl', 'slug': 'atelier-ceramic-bowl', 'category': home, 'price': 34.00, 'stock': 14, 'description': 'Handcrafted style for your tableware.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1534801099348-9d4a854886fd?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Piper Sunglasses', 'slug': 'piper-sunglasses', 'category': fashion, 'price': 49.00, 'stock': 10, 'description': 'Bold shades for sunny weekends.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Terra Coffee Maker', 'slug': 'terra-coffee-maker', 'category': home, 'price': 99.00, 'stock': 8, 'description': 'Brew your favorite cup with speed and style.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Orbit Phone Case', 'slug': 'orbit-phone-case', 'category': electronics, 'price': 24.00, 'stock': 27, 'description': 'Durable protection with a modern finish.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=900&q=80'},
        {'name': 'Solstice Scarf', 'slug': 'solstice-scarf', 'category': fashion, 'price': 42.00, 'stock': 13, 'description': 'A soft layer for cool mornings.', 'is_featured': False, 'image_url': 'https://images.unsplash.com/photo-1515125520148-52a3b5f5b04a?auto=format&fit=crop&w=900&q=80'},
    ]

    for data in products:
        Product.objects.update_or_create(
            slug=data['slug'],
            defaults={
                'name': data['name'],
                'category': data['category'],
                'price': data['price'],
                'stock': data['stock'],
                'description': data['description'],
                'is_featured': data['is_featured'],
                'image_url': data['image_url'],
            },
        )


if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')


electronics, fashion, home = ensure_categories()
seed_products(electronics, fashion, home)

print('Seed data loaded successfully.')
