from xml.dom import minidom

from django.conf import settings
from social_core.backends.oauth import BaseOAuth1


class OpenStreetMapOAuth(BaseOAuth1):
    """OpenStreetMap OAuth authentication backend"""
    name = 'openstreetmap'

    AUTHORIZATION_URL = '{}/authorize'.format(settings.OAUTH_BASE_URL)
    REQUEST_TOKEN_URL = '{}/request_token'.format(settings.OAUTH_BASE_URL)
    ACCESS_TOKEN_URL = '{}/access_token'.format(settings.OAUTH_BASE_URL)
    EXTRA_DATA = [
        ('id', 'id'),
        ('avatar', 'avatar'),
        ('account_created', 'account_created')
    ]

    def get_user_details(self, response):
        """Return user details from OpenStreetMap account"""
        return {
            'username': response['username'],
            'email': '',
            'fullname': '',
            'first_name': '',
            'last_name': ''
        }

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        response = self.oauth_request(
            access_token, '{}/api/0.6/user/details'.format(settings.OSM_API_URL)
        )
        try:
            dom = minidom.parseString(response.content)
        except ValueError:
            return None
        user = dom.getElementsByTagName('user')[0]
        try:
            avatar = dom.getElementsByTagName('img')[0].getAttribute('href')
        except IndexError:
            avatar = None
        return {
            'id': user.getAttribute('id'),
            'username': user.getAttribute('display_name'),
            'account_created': user.getAttribute('account_created'),
            'avatar': avatar
        }
