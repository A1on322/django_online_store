# 🛍️ Django online store

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

E-commerce pet-project built with modern Django deployment stack. Users can browse a product catalogue with 
category filters, add items to a shopping-cart, complete checkout (Stripe), and edit their profile 
(name, avatar, password, e-mail). Sign-in is flexible: classic username + password, e-mail + password, or social login 
via Google / GitHub OAuth.

---

## Content
- [Technologies](#technologies)
- [Features](#features)
- [Getting started](#getting-started)
- [Testing](#testing)


---
## Technologies

* **Backend:** Django 5 | PostgreSQL 17 | Redis 7 | Celery 5 | Stripe Checkout  
* **Auth:** Google OAuth2, GitHub OAuth  
* **Infra:** Docker Compose, Nginx, Gunicorn  
* **Tests / Lint:** pytest, flake8, GitHub Actions

---

## Features
- Product catalogue with category filter & pagination
- Cart, orders, Stripe payment flow (Checkout + Webhooks)
- Flexible sign-in system  
  - classic **username + password** login  
  - **e-mail + password** login (custom auth backend)  
  - social login — `social-auth-app-django`
- Email (SMTP) password reset links are sent as Celery tasks
- Redis-backed caching with automatic invalidation
- Automated creation of products in stripe dashboard
- 100 % Dockerised (one‐command start)

---

## Getting started

1. Clone the repository  
   ```sh
   git clone https://github.com/A1on322/django_online_store.git
   cd django_online_store
    ```

2. Copy the environment template and fill in your values (Stripe keys, DB creds, e-mail, …):
    ```sh
    cp .env.example .env
    nano .env            # or any editor
    ```

3. Install stripe:
    https://docs.stripe.com/stripe-cli?install-method=homebrew
    ```sh
    brew install stripe/stripe-cli/stripe
    ```

4. Log in to Stripe CLI and forward webhooks; copy the printed whsec_… secret:
    ```sh
    stripe login
    stripe listen --forward-to localhost:8000/webhook/stripe/
    ```

5. Paste the webhook secret into .env (STRIPE_ENDPOINT_SECRET=whsec_xxx):
    ```sh
    nano .env
    ```

6. Build images and start the full stack (backend, Postgres, Redis, Nginx, Celery)
    ```sh
    docker compose up --build 
    ```

7. Create a Django superuser inside the running backend container
    ```sh
    docker compose exec store-backend python manage.py createsuperuser
    ```

8. Generate Stripe Price IDs for all existing products
    ```sh
    docker compose exec store-backend python manage.py shell_plus
   
    [p.save() for p in Product.objects.all()]
    ```
9. Open your browser and navigate to `http://127.0.0.1`
---

## Testing

- to run tests execute:
    ```sh
    docker compose exec store-backend python manage.py test
    ```
- to lint:
    ```sh
    docker compose exec store-backend flake8
    ```
- to enter shell_plus:
    ```sh
    docker compose exec store-backend python manage.py shell_plus
    ```



