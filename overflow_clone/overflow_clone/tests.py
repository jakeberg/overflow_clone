from django.test import TestCase
from API.views import OverflowUserViewSet
from rest_framework.test import APIRequestFactory


class TestOverflowUserViewSet(TestCase):

    def test_overflow_user(self):
        factory = APIRequestFactory()
        request = factory.post('/overflow-user/overflow_user/', json.dumps(
            {'author': 'jake'}), content_type='application/json')
        response = OverflowUserViewSet.overflow_user(request)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
