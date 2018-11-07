from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from Rentals.models import *


# Create your tests here.
class AccountCreationTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_user.first_name = 'Hannah'
        self.test_user.last_name = 'Test'

        # URL for creating an account.
        self.create_url = reverse('user-list')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
            "username": "foobar",
            "email": "foobar@example.com",
            "password": "somepassword",
            "first_name": "Jonny",
            "last_name": "Tester",
        }

        response = self.client.post(self.create_url, data, format='json')
        print(response.data)
        user = User.objects.latest('id')

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

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
                "username": "foobar",
                "email": "foobarbaz@example.com",
                "password": "foo"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
                "username": "foobar",
                "email": "foobarbaz@example.com",
                "password": ""
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            "username": "foo"*30,
            "email": "foobarbaz@example.com",
            "password": "foobar"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_no_username(self):
        data = {
                "username": "",
                "email": "foobarbaz@example.com",
                "password": "foobar"
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
                "username": "testuser",
                "email": "user@example.com",
                "password": "testuser"
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            "username": "testuser2",
            "email": "test@example.com",
            "password": "testuser"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            "username": "foobarbaz",
            "email": "testing",
            "passsword": "foobarbaz"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        data = {
            "username": "foobar",
            "email": "",
            "password": "foobarbaz"
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_profile_create_default(self):
        data = {
            "username": "foobar",
            "email": "foobar@example.com",
            "password": "somepassword",
            "first_name": "Jonny",
            "last_name": "Tester",
        }
        # Check that status code is 201

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['profile']['is_goalie'], True)
        self.assertEqual(response.data['profile']['rating'], 0.0)
        self.assertEqual(response.data['profile']['games_played'], 0)

    def test_profile_create_non_default(self):
        data = {
            "username": "foobar",
            "email": "foobar@example.com",
            "password": "somepassword",
            "first_name": "Jonny",
            "last_name": "Tester",
            "is_goalie": False,
            "rating": '3.0',
            "games_played": 4,
            'skill_level': 2,
        }
        # Check that status code is 201

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['profile']['is_goalie'], False)
        self.assertEqual(response.data['profile']['rating'], 3.0)
        self.assertEqual(response.data['profile']['games_played'], 4)

    def test_profile_create_bad_rating(self):
        data = {
            "username": "foobar",
            "email": "foobar@example.com",
            "password": "somepassword",
            "first_name": "Jonny",
            "last_name": "Tester",
            "rating": '6.0',
        }
        # Check that status code is 201

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_create_bad_games_played(self):
        data = {
            "username": "foobar",
            "email": "foobar@example.com",
            "password": "somepassword",
            "first_name": "Jonny",
            "last_name": "Tester",
            "games_played": -1890,
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_create_bad_is_goalie(self):
        data = {
            "username": "foobar",
            "email": "foobar@example.com",
            "password": "somepassword",
            "first_name": "Jonny",
            "last_name": "Tester",
            "is_goalie": "Cheese",
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GoalieTest(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.test_user = User.objects.create_user('tester_one', 'test@gmail.com', 'testpassword')
        self.test_user.first_name = 'Hannah'
        self.test_user.last_name = 'Test'

        # URL for creation
        self.create_url = reverse('goalie-list')

        # Create locations
        self.location_1 = Location.objects.create()
        self.location_1.name = "Kitchener"
        self.location_1.save()
        self.location_2 = Location.objects.create()
        self.location_2.name = "Toronto"
        self.location_2.save()
        self.location_3 = Location.objects.create()
        self.location_3.name = "Ottawa"
        self.location_3.save()

    def test_create_default(self):
        data = {
            'location_ids': [1],  # One location is mandatory
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], None)
        self.assertEqual(response.data['location_ids'], [1])
        self.assertEqual(response.data['skill_level'], 5)

    def test_create_non_default(self):
        data = {
            'user': 1,
            'location_ids': [1, 2],
            'skill_level': 2
        }
        response = self.client.post(reverse('goalie-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], 1)
        self.assertEqual(response.data['location_ids'], [1, 2])
        self.assertEqual(response.data['skill_level'], 2)

    def test_create_invalid_user_1(self):
        data = {
            'user': -20,
            'location_ids': [1],
        }
        response = self.client.post(reverse('goalie-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_user_2(self):
        data = {
            'user': 40,
            'location_ids': [1],
        }
        response = self.client.post(reverse('goalie-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_skill_level_1(self):
        data = {
            'location_ids': [1],
            'skill_level': -5,
        }
        response = self.client.post(reverse('goalie-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_skill_level_2(self):
        data = {
            'location_ids': [1],
            'skill_level': 20,
        }
        response = self.client.post(reverse('goalie-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_location_1(self):
        data = {
            'location_ids': [-1],
        }
        response = self.client.post(reverse('goalie-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_location_2(self):
        data = {
            'location_ids': [1, 2, 20],
        }
        response = self.client.post(reverse('goalie-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MessageTest(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('tester_one', 'test1@gmail.com', 'test1password')
        self.test_user_1.first_name = 'Hannah'
        self.test_user_1.last_name = 'Test'

        self.test_user_2 = User.objects.create_user('tester_two', 'test2@gmail.com', 'test2password')
        self.test_user_2.first_name = 'Rob'
        self.test_user_2.last_name = 'Tester'

        # URL for creation
        self.create_url = reverse('message-list')

    # def test_create_default(self):



'''
class GameTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_user.first_name = 'Jonny'
        self.test_user.last_name = 'Test'

        # URL for creating an account.
        self.create_url = reverse('game-list')

    # def test_game_create(self):

'''
