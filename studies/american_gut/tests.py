from provider.oauth2.models import AccessToken

from rest_framework import status
from rest_framework.test import APITestCase

class UserDataTests(APITestCase):
    fixtures = ['open_humans/fixtures/test-data.json']

    def verify_request(self, url, status_code):
        response = self.client.get('/api/american-gut' + url)

        self.assertEqual(response.status_code, status_code)

    def verify_request_200(self, url):
        self.verify_request(url, status.HTTP_200_OK)

    def verify_request_403(self, url):
        self.verify_request(url, status.HTTP_403_FORBIDDEN)

    def test_get_user_data(self):
        """
        Ensure we can get a UserData object with credentials.
        """
        access_token = AccessToken.objects.get(pk=1)

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + access_token.token)

        self.verify_request_200('/user-data/2/')
        self.verify_request_200('/user-data/current/')

    def test_get_user_data_no_credentials(self):
        """
        Ensure we can't get a UserData object with no credentials.
        """
        self.client.credentials()

        self.verify_request_403('/user-data/1/')
        self.verify_request_403('/user-data/2/')
        self.verify_request_403('/user-data/current/')