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
        
        


        




