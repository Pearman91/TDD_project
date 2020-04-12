from unittest.mock import patch

from django.test import TestCase

from accounts.models import Token


EMAIL = 'jozinzbazin@example.com'


class SendLoginEmailViewTest(TestCase):

    def test_redirects_to_homepage(self):
        response = self.client.post('/accounts/login?token=123456vgjkaf')
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_address_from_post(self, mock_send_mail):
        self.client.post('/accounts/send_login_email',
                         data={'email': EMAIL})

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Hi, you can log in to Superlists')
        self.assertEqual(from_email, 'noreply@superlists')
        self.assertEqual(to_list, [EMAIL])

    def test_show_success_message_after_sending_login(self):
        response = self.client.post('/accounts/send_login_email',
                                    data={'email': EMAIL},
                                    follow=True)  # client gets page after redirect

        message = list(response.context['messages'])[0]
        self.assertEqual(message.message,
                         'Check out your email for message with a link to log '
                         'in there!')
        self.assertEqual(message.tags, 'success')

    def test_creates_token_for_mail_address(self):
        self.client.post('/accounts/send_login_email', data={'email': EMAIL})
        token = Token.objects.first()
        self.assertEqual(token.email, EMAIL)

    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        self.client.post('/accounts/send_login_email', data={'email': EMAIL})

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)
