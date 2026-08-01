from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

import seed_data
from .models import Category, Product


class StoreViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            name='Laptop',
            slug='laptop',
            category=self.category,
            price=999.99,
            description='A powerful laptop for work and play.',
            stock=10,
            image='products/laptop.jpg',
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to TechCart')

    def test_product_detail_page_loads(self):
        response = self.client.get(reverse('product_detail', args=[self.product.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_offers_page_loads(self):
        response = self.client.get(reverse('offers'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Shop the new season')

    def test_product_display_image_url_uses_remote_source(self):
        self.product.image_url = 'https://images.unsplash.com/photo-1518770660439-4636190af475'
        self.product.save(update_fields=['image_url'])
        self.assertEqual(self.product.display_image_url, self.product.image_url)

    def test_mobile_phone_is_seeded_into_catalog(self):
        electronics, fashion, home = seed_data.ensure_categories()
        seed_data.seed_products(electronics, fashion, home)

        self.assertTrue(Product.objects.filter(slug='techcart-mobile-phone').exists())

    def test_registration_creates_user_and_logs_in(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'SecurePass123',
            'password2': 'SecurePass123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_with_email_works(self):
        user = User.objects.create_user(username='emailuser', email='emailuser@example.com', password='SecurePass123')
        response = self.client.post(reverse('login'), {
            'username': 'emailuser@example.com',
            'password': 'SecurePass123',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertEqual(response.context['user'].username, user.username)
