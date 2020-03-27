from django.test import TestCase


class FirstTest(TestCase):

    def test_miserable_failing(self):
        self.assertEqual(2 + 2, 5)  # Orwell would be proud
