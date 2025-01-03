import random
import os
import urllib.request
from django.core.management.base import BaseCommand
from faker import Faker
from core.models import User, Product, Category, Order, OrderLine
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Directory to store downloaded images
        image_dir = os.path.join(settings.MEDIA_ROOT, 'product_images')
        os.makedirs(image_dir, exist_ok=True)

        # URLs of placeholder images
        image_urls = [
            'https://via.placeholder.com/150',
            'https://via.placeholder.com/200',
            'https://via.placeholder.com/250',
            'https://via.placeholder.com/300',
        ]

        # Create Categories
        categories = []
        for _ in range(5):
            category = Category.objects.create(
                name=fake.word(),
                slug=fake.slug(),
                parent_id=None
            )
            categories.append(category)

        # Create Users
        users = []
        admin = User.objects.create_user(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=f"admin@gmail.com",
            password="pass",
            phone_number=fake.phone_number(),
            address_country=fake.country(),
            address_city=fake.city(),
            address_street=fake.street_address(),
            address_postal_code=fake.postcode(),
            role='admin',
            profile_picture=None
        )
        users.append(admin)
        
        for i in range(10):
            customer = User.objects.create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=f"user{i + 1}@gmail.com",
                password="pass",
                phone_number=fake.phone_number(),
                address_country=fake.country(),
                address_city=fake.city(),
                address_street=fake.street_address(),
                address_postal_code=fake.postcode(),
                role='customer',
                profile_picture=None
            )
            users.append(customer)

        # Create Products with random images
        products = []
        for _ in range(20):
            # Download a random image
            image_url = random.choice(image_urls)
            image_name = f'{fake.slug()}.jpg'
            image_path = os.path.join(image_dir, image_name)
            urllib.request.urlretrieve(image_url, image_path)

            with open(image_path, 'rb') as image_file:
                product = Product.objects.create(
                    title=fake.sentence(nb_words=3),
                    slug=fake.slug(),
                    desc=fake.paragraph(nb_sentences=3),
                    price=random.uniform(10.0, 100.0),
                    category=random.choice(categories),
                    image=File(image_file, name=image_name),
                    stock=100,
                    product_type="physical",
                    author=admin
                )
                products.append(product)

        # Create Orders and OrderLines
        """
        for _ in range(15):
            order = Order.objects.create(
                placed_at=fake.date_time_this_year(),
                customer=random.choice(customers),
                total_amount=0.0
            )

            total_amount = 0.0
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                quantity = random.randint(1, 10)
                unit_price = product.price
                line_total = quantity * unit_price
                total_amount += line_total

                OrderLine.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price
                )

            order.total_amount = total_amount
            order.save()
        """

        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with dummy data'))

