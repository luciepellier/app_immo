from django.test import TestCase

# Create your tests here.

class ApartmentTest(TestCase):
    def test_add_apartment(self):
        # Test in TDD, we check there's no apartment created
        self.assertEqual(Apartment.objects.count(), 1)