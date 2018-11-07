from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from Rentals.models import Game, Location, Message, Profile

# TODO: Write tests for update, patch, and delete

# TODO: Write tests that check token generation

# TODO: Write tests that check password reset

# TODO: Write test that account activation via email

# Create your tests here.
class UserCreation(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_user.first_name = 'Hannah'
        self.test_user.last_name = 'Test'

        # URL for creating an account.
        self.create_url = reverse('user-list')

    def test_create_user(self):
        # Ensure we can create a new user and a valid token is created with it.
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'first_name': 'Jonny',
            'last_name': 'Tester',
        }

        response = self.client.post(self.create_url, data, format='json')

        # Check that status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that there are two users in the database
        self.assertEqual(User.objects.count(), 2)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
        self.assertFalse('password' in response.data)

        # Check that a profile was created as well
        self.assertEqual(Profile.objects.count(), 2)

    def test_create_user_with_no_username(self):
        data = {
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobar'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['username'][0], 'This field may not be blank.')

    def test_create_user_with_preexisting_username(self):
        data = {
                'username': 'testuser',
                'email': 'user@example.com',
                'password': 'testuser'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email': 'invalid.email',
            'passsword': 'foobarbaz'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')


class GameCreation(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('tester_one', 'test1@fakefalse.com', 'test1password')
        self.test_user_1.first_name = 'Hannah'
        self.test_user_1.last_name = 'Test'

        self.test_user_2 = User.objects.create_user('tester_two', 'test2@fakefalse.com', 'test2password')
        self.test_user_2.first_name = 'Rob'
        self.test_user_2.last_name = 'Tester'

        self.location = Location.objects.create(name='Kitchener',
                                                latitude=43.4516395,
                                                longitude=-80.49253369999997)

        self.create_url = reverse('game-list')

    def test_create(self):
        data = {
            'user': 1,
            'skill_level': 3,
            'location': self.location.id,
            'game_time': '2018-12-25T14:30:00Z',
            'two_goalies_needed': True,
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        # self.assertEqual(response.data['user'], data['user'])
        self.assertEqual(response.data['location'], data['location'])
        self.assertEqual(response.data['game_time'], data['game_time'])
        self.assertEqual(response.data['two_goalies_needed'], data['two_goalies_needed'])


class LocationCreation(APITestCase):
    def setUp(self):
        self.create_url = reverse('location-list')

    def test_create(self):
        data = {
            'name': 'Kitchener',
            'latitude': 43.45164,
            'longitude': -80.492534,
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['latitude'], data['latitude'])
        self.assertEqual(response.data['longitude'], data['longitude'])


class MessageTest(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('tester_one', 'test1@gmail.com', 'test1password')
        self.test_user_1.first_name = 'Hannah'
        self.test_user_1.last_name = 'Test'

        self.test_user_2 = User.objects.create_user('tester_two', 'test2@gmail.com', 'test2password')
        self.test_user_2.first_name = 'Rob'
        self.test_user_2.last_name = 'Tester'

        self.location = Location.objects.create()

        self.game = Game.objects.create(location=self.location)

        # URL for creation
        self.create_url = reverse('message-list')

    def test_create(self):
        data = {
            'game': self.game.id,
            'body': 'This is my test message. Hello other person',
            'game_user': 1,
            'goalie_user': 2,
            'sender_is_goalie': True
        }

        response = self.client.post(self.create_url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['body'], data['body'])
        self.assertEqual(response.data['game_user'], data['game_user'])
        self.assertEqual(response.data['goalie_user'], data['goalie_user'])
        self.assertEqual(response.data['sender_is_goalie'], data['sender_is_goalie'])
