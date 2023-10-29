from django.forms import ValidationError
from django.test import TestCase
from .models import *


from faker import Faker

fake = Faker()


class ReviewTestCase(TestCase):
    
    def setUp(self):
        print("Setup called")
        
    def test_review(self):
        cont = ['abc','def']
        
        for reviews in cont:
            obj = Review.objects.create(
                subject = reviews,
                email = 'abc@gmail.com',
                body = 'abcacbacb'
            )
            self.assertEqual(reviews, obj.subject)
        
        objs = Review.objects.all()
        
        self.assertEqual(objs.count(),2)
    def test_model_string_representation(self):

        review = Review.objects.create(
        subject=fake.word(),
        email=fake.email(),
        body=fake.text(max_nb_chars=500)
    )

        self.assertEqual(str(review), str(review.review_id))
    def test_model_meta_options(self):
        self.assertEqual(Review._meta.verbose_name, "Review")
        self.assertEqual(Review._meta.db_table, "review")
        
        

class UserTestCase(TestCase):
    def test_create_user(self):

        email = 'abc@gmail.com'
        name = 'Shishir'
        password = '1234'
        location = 'Dhaka'
        city = 'Mirpur'
        number = '111111'
        active = True
        staff = True
        admin = True

        user = User.objects.create(
            email=email,
            name=name,
            password=password,
            location=location,
            city=city,
            number=number,
            active=active,
            staff=staff,
            admin=admin
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertEqual(user.active, active)
        self.assertEqual(user.number, number)
        self.assertEqual(user.admin, admin)
        self.assertEqual(user.password, password)
        self.assertEqual(user.city, city)
def test_model_string_representation(self):
    fake = Faker()
    email = fake.email()
    user = User.objects.create(
        email=email,
        name=fake.first_name(),
        password=fake.password(),
        location=fake.word(),
        city=fake.city(),
        number=fake.random_int(min=100000, max=999999),
        active=fake.boolean(),
        staff=fake.boolean(),
        admin=fake.boolean()
    )

    self.assertEqual(str(user), email)
    
def test_required_fields(self):
    with self.assertRaises(IntegrityError):
        # Creating a user without the 'name' field, which is required
        User.objects.create(
            email='test@example.com',
            password='securepassword',
            location='Somewhere',
            city='City',
            number=123456,
            active=True,
            staff=False,
            admin=False
        )
def test_model_string_representation(self):
    fake = Faker()
    email = fake.email()
    user = User.objects.create(
        email=email,
        name=fake.first_name(),
        password=fake.password(),
        location=fake.word(),
        city=fake.city(),
        number=fake.random_int(min=100000, max=999999),
        active=fake.boolean(),
        staff=fake.boolean(),
        admin=fake.boolean()
    )

    self.assertEqual(str(user), email)


        




