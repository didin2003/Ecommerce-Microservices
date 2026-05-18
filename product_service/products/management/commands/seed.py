from django.core.management.base import BaseCommand
from products.models import Product
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):

    help = 'Seed Product Data'

    def handle(self, *args, **kwargs):

        for _ in range(10):

            Product.objects.create(
                name=fake.word(),
                description=fake.text(),
                price=random.randint(100, 5000),
                image='https://via.placeholder.com/150',
                stock=random.randint(1, 100)
            )

        self.stdout.write(
            self.style.SUCCESS('Products Seeded Successfully')
        )