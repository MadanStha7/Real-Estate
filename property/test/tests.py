
from django.test import TestCase
from property.models import City, Location


class CityModelTest(TestCase):

    def setUp(self):

        City.objects.create(name='city name')
        City.objects.create(name='city name2')
        City.objects.create(name='city name3')

    def create_city(self, name = 'city_name'):
        return City.objects.create(name=name)

    def test_city_name(self):

        city1 = City.objects.get(name='city name')
        city2 = City.objects.get(name='city name2')
        city3 = City.objects.get(name='city name3')
        self.assertEqual(city1.name,'city name')
        self.assertEqual(city2.name,'city name2')
        self.assertEqual(city3.name,'city name3')

    def test_city_qs(self):
        name = 'city name'
        city1 = self.create_city(name=name)
        city2 = self.create_city(name=name)
        city3 = self.create_city(name=name)
        qs = City.objects.filter(name=name)
        self.assertEqual(qs.count(), 4)

class LocationTestCae(TestCase):

    def setup(self):

        Location.objects.create(city=city, locality='Biratnagar', street = '1234 BRT road', listing="", property_info=PropertyInfo,)

    def 

