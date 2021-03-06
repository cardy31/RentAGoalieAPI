from django.contrib.auth.models import User

import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from Rentals.models import Game, Location, Message, Profile
from Rentals.views import GameList, GameDetail, LocationList, LocationDetail, MessageList, MessageDetail,\
    UserList, UserDetail, ProfileList, ProfileDetail

# TODO: Write tests for create, patch, and delete

# TODO: Write tests that check password reset

# TODO: Write test to check account activation via email

# TODO: Write ApplyForGame tests

factory = APIRequestFactory()


class GameCreate(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('tester_one', 'test1@fakefalse.com', 'test1password')
        self.test_user_1.first_name = 'Hannah'
        self.test_user_1.last_name = 'Test'
        self.test_user_1.save()

        self.test_user_2 = User.objects.create_user('tester_two', 'test2@fakefalse.com', 'test2password')
        self.test_user_2.first_name = 'Rob'
        self.test_user_2.last_name = 'Tester'
        self.test_user_2.save()

        self.location = Location.objects.create(name='Kitchener',
                                                latitude=43.4516395,
                                                longitude=-80.49253369999997)

        self.create_url = reverse('game-list')

    def test_create_with_same_user(self):
        data = {
            'user': 1,
            'skill_level': 3,
            'location': self.location.id,
            'game_time': '2018-12-25T14:30:00Z',
            'two_goalies_needed': True,
        }

        view = GameList.as_view()
        request = factory.post(self.create_url, json.dumps(data), content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(response.data['location'], data['location'])
        self.assertEqual(response.data['game_time'], data['game_time'])
        self.assertEqual(response.data['two_goalies_needed'], data['two_goalies_needed'])


class GameDelete(APITestCase):
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

        self.delete_url = reverse('game-list')

        self.game = Game.objects.create(user=self.test_user_1,
                                        skill_level=3,
                                        location=self.location,
                                        game_time='2018-12-25T14:30:00Z',
                                        two_goalies_needed=True)

    def test_delete(self):
        view = GameDetail.as_view()
        request = factory.delete(self.delete_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        self.assertEqual(Game.objects.count(), 1)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Game.objects.count(), 0)

    def test_delete_bad_url(self):
        view = GameDetail.as_view()
        request = factory.delete(self.delete_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        response = view(request, pk=115)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GameUpdate(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('tester_one', 'test1@fakefalse.com', 'test1password')
        self.test_user_1.first_name = 'Hannah'
        self.test_user_1.last_name = 'Test'

        self.location = Location.objects.create(name='Kitchener',
                                                latitude=43.4516395,
                                                longitude=-80.49253369999997)

        self.update_url = reverse('game-list')

        self.game = Game.objects.create(user=self.test_user_1,
                                        skill_level=3,
                                        location=self.location,
                                        game_time='2018-12-25T14:30:00Z',
                                        two_goalies_needed=True)

    def test_update(self):
        data = {'skill_level': 1}

        view = GameDetail.as_view()
        request = factory.patch(self.update_url, json.dumps(data), content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['skill_level'], data['skill_level'])
        self.assertEqual(response.data['location'], 1)

# TODO: Game GET


class LocationCreate(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        self.create_url = reverse('location-list')

    def test_create(self):
        data = {
            'name': 'Kitchener',
            'latitude': 43.45164,
            'longitude': -80.492534,
        }

        view = LocationList.as_view()
        request = factory.post(self.create_url, json.dumps(data), content_type='application/json')
        force_authenticate(request, user=self.test_user)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['latitude'], data['latitude'])
        self.assertEqual(response.data['longitude'], data['longitude'])


class LocationDelete(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.delete_url = reverse('location-list')
        new_location = Location.objects.create()
        new_location.name = 'Kitchener'
        new_location.latitude = 43.45164
        new_location.longitude = -80.492534

    def test_delete(self):
        view = LocationDetail.as_view()
        request = factory.delete(self.delete_url, content_type='application/json')
        force_authenticate(request, user=self.test_user)
        self.assertEqual(Location.objects.count(), 1)
        response = view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 0)

    def test_delete_bad_url(self):
        view = LocationDetail.as_view()
        request = factory.delete(self.delete_url, content_type='application/json')
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=115)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class LocationUpdate(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.update_url = reverse('location-list')
        new_location = Location.objects.create()
        new_location.name = 'Kitchener'
        new_location.latitude = 43.45164
        new_location.longitude = -80.492534

    def test_update(self):
        data = {'longitude': 46}

        view = LocationDetail.as_view()
        request = factory.patch(self.update_url, json.dumps(data), content_type='application/json')
        force_authenticate(request, user=self.test_user)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['longitude'], data['longitude'])


class MessageCreate(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('tester_one', 'test1@gmail.com', 'test1password')
        self.test_user_2 = User.objects.create_user('tester_two', 'test2@gmail.com', 'test2password')

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

        view = MessageList.as_view()
        request = factory.post(self.create_url, json.dumps(data), content_type='application/json', user=self.test_user_1)
        force_authenticate(request, user=self.test_user_1)
        response = view(request)

        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(response.data['game'], data['game'])
        self.assertEqual(response.data['body'], data['body'])
        self.assertEqual(response.data['game_user'], data['game_user'])
        self.assertEqual(response.data['goalie_user'], data['goalie_user'])
        self.assertEqual(response.data['sender_is_goalie'], data['sender_is_goalie'])


class MessageGet(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('tester_one', 'test1@gmailfake.com', 'test1password')
        self.test_user_2 = User.objects.create_user('tester_two', 'test2@gmailfake.com', 'test2password')
        self.test_user_3 = User.objects.create_user('tester_three', 'test3@gmailfake.com', 'test3password')
        self.test_user_super = User.objects.create_user('tester_four', 'test4@gmailfake.com', 'test4password')
        self.test_user_super.is_superuser = True
        self.location = Location.objects.create()
        self.game = Game.objects.create(location=self.location)
        self.message = Message.objects.create(game=self.game,
                                              body='Foobar',
                                              game_user=self.test_user_1,
                                              goalie_user=self.test_user_2)
        self.get_url = reverse('message-list')

    def test_get_list_user_is_renter_in_message(self):
        view = MessageList.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_user_is_goalie_in_message(self):
        view = MessageList.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_2)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_user_not_in_message(self):
        view = MessageList.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_3)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_list_user_is_superuser(self):
        view = MessageList.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_super)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_detail_user_is_renter_in_message(self):
        view = MessageDetail.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)

    def test_get_detail_user_is_goalie_in_message(self):
        view = MessageDetail.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_2)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)

    def test_get_detail_user_not_in_message(self):
        view = MessageDetail.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_3)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 1)

    def test_get_detail_user_is_superuser(self):
        view = MessageDetail.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_super)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)


class UserCreate(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_user.first_name = 'Hannah'
        self.test_user.last_name = 'Test'

        # URL for creating an account.
        self.create_url = reverse('user-list')

        self.view = UserList.as_view()

    def test_create_user(self):
        # Ensure we can create a new user and a valid token is created with it.
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword',
            'first_name': 'Jonny',
            'last_name': 'Tester',
        }

        request = factory.post(self.create_url, json.dumps(data), content_type='application/json')
        response = self.view(request)

        # Check that status code is 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that there are two users in the database
        self.assertEqual(User.objects.count(), 2)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])

        # Check that a profile was created as well
        self.assertEqual(Profile.objects.count(), 2)

    def test_create_user_with_no_username(self):
        data = {
                'username': '',
                'email': 'foobarbaz@example.com',
                'password': 'foobar'
                }

        request = factory.post(self.create_url, json.dumps(data), content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['username'][0], 'This field may not be blank.')

    def test_create_user_with_preexisting_username(self):
        data = {
                'username': 'testuser',
                'email': 'user@example.com',
                'password': 'testuser'
                }

        request = factory.post(self.create_url, json.dumps(data), content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['username'][0], 'A user with that username already exists.')

    def test_create_user_with_invalid_email(self):
        data = {
            'username': 'foobarbaz',
            'email': 'invalid.email',
            'passsword': 'foobarbaz'
        }

        request = factory.post(self.create_url, json.dumps(data), content_type='application/json')
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['email'][0], 'Enter a valid email address.')


class UserGet(APITestCase):
    def setUp(self):
        self.test_user_1 = User.objects.create_user('tester_one', 'test1@gmailfake.com', 'test1password')
        self.test_user_2 = User.objects.create_user('tester_two', 'test2@gmailfake.com', 'test2password')
        self.test_user_3 = User.objects.create_user('tester_three', 'test3@gmailfake.com', 'test3password')
        self.test_user_super = User.objects.create_user('tester_four', 'test4@gmailfake.com', 'test4password')
        self.test_user_super.is_superuser = True

        self.get_url = reverse('user-list')

    # Normal user can only see self
    def test_get_list_as_normal_user(self):
        view = UserList.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        response = view(request)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'tester_one')

    # Superuser can see all users
    def test_get_list_as_superuser(self):
        view = UserList.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_super)
        response = view(request)

        self.assertEqual(len(response.data), 4)

    # Normal user can get detail of self
    def test_get_detail_of_normal_user_as_same_user(self):
        view = UserDetail.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        response = view(request, pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(response.data['username'], 'tester_one')

    # Normal user cannot get detail of another user
    def test_get_detail_of_normal_user_as_different_user(self):
        view = UserDetail.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_1)
        response = view(request, pk=2)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(response.data), 1)

    # Superuser can get detail of any user
    def test_get_detail_of_normal_user_as_superuser(self):
        view = UserDetail.as_view()
        request = factory.get(self.get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user_super)
        response = view(request, pk=2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)
        self.assertEqual(response.data['username'], 'tester_two')

# TODO: User delete tests

# TODO: User update tests


# TODO: Fix up permissions and write more test cases here
class ProfileCreate(APITestCase):
    def setUp(self):
        self.profile_get_url = reverse('profile-list')
        self.view = ProfileDetail.as_view()
        self.test_user = User.objects.create_user('tester_one', 'test1@fakefalse.com', 'test1password')

    def test_create_profile_on_user_create(self):
        request = factory.get(self.profile_get_url, content_type='application/json')
        force_authenticate(request, user=self.test_user)
        response = self.view(request, pk=1)
        # response = self.client.get(self.profile_get_url + '1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserAuthenticate(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')
        self.test_user.first_name = 'Hannah'
        self.test_user.last_name = 'Test'
        self.test_user.is_active = True

        # URL for creating an account.
        self.token_url = reverse('token-get')

    def test_user_get_token(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['token']), 40)
