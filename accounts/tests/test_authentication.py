from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.authentication import PasswordlessAuthenticationBackend
from accounts.models import Token

User = get_user_model()
EMAIL = 'jozinzbazin@example.com'


class AuthenticationTest(TestCase):

    def test_return_None_if_token_doesnt_exist(self):
        result = PasswordlessAuthenticationBackend().authenticate('nonexistent')
        self.assertIsNone(result)

    def test_return_existing_user_that_has_token_if_token_exists(self):
        email = EMAIL
        token = Token.objects.create(email=email)
        existing_user = User.objects.create(email=email)

        user_found_by_token = PasswordlessAuthenticationBackend().authenticate(
            token.uid)
        self.assertEqual(user_found_by_token, existing_user)

    def test_create_user_if_token_exists(self):
        email = EMAIL
        token = Token.objects.create(email=email)

        user_found_by_token = PasswordlessAuthenticationBackend().authenticate(
            token.uid)
        print(user_found_by_token.email, token.email)
        new_user = User.objects.get(email=token.email)
        self.assertEqual(user_found_by_token, new_user)


class GetUserTest(TestCase):

    def test_get_user_by_email(self):
        User.objects.create(email='whomever@example.com')
        our_user = User.objects.create(email=EMAIL)
        found_user = PasswordlessAuthenticationBackend().get_user(EMAIL)
        self.assertEqual(found_user, our_user)

    def test_return_None_if_no_user_with_given_mail(self):
        found_user = PasswordlessAuthenticationBackend().get_user(EMAIL)
        self.assertIsNone(found_user)

