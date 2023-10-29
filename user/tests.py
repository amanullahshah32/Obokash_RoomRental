from django.test import TestCase
from .models import User, Room, House

class UserModelTestCase(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
    email='testuser@example.com',
    name='Test User',
    password='testpassword',
    number=12345,  # Provide a valid number
    # Add other fields as needed
)

        self.assertEqual(User.objects.count(), 1)

    # Add more test methods for User model

class RoomModelTestCase(TestCase):
    def test_room_creation(self):
        room = Room.objects.create(
            dimention='10x10',
            location='Test Location',
            city='Test City',
            state='Test State',
            cost=100,
            bedrooms=2,
            kitchen='Yes',
            hall='No',
            balcany='Yes',
            desc='Test Description',
            AC='Yes',
            # Add other fields as needed
        )
        self.assertEqual(Room.objects.count(), 1)

    # Add more test methods for Room model

class HouseModelTestCase(TestCase):
    def test_house_creation(self):
        house = House.objects.create(
            area=1500,
            floor=2,
            location='Test Location',
            city='Test City',
            state='Test State',
            cost=200000,
            bedrooms=4,
            kitchen=1,
            hall='Yes',
            balcany='No',
            desc='Test Description',
            AC='Yes',
            # Add other fields as needed
        )
        self.assertEqual(House.objects.count(), 1)

    # Add more test methods for House model
