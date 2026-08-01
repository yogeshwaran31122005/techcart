# TechCart

TechCart is a Django-based ecommerce storefront built with SQLite, Django templates, and simple product catalog features.

## Features

- Homepage with featured and category-based product browsing
- Product detail pages with add-to-cart flow
- Cart and checkout experience
- User registration and login with SQLite-backed authentication
- Admin dashboard for managing products and orders

## Setup

1. Create a Python virtual environment
2. Install dependencies from `requirements.txt`
3. Run `python manage.py migrate`
4. Run `python manage.py runserver`

## Notes

- The project uses SQLite for the database.
- Add product images via `seed_data.py` or the Django admin.
- Use `manage.py test store` to validate application tests.
