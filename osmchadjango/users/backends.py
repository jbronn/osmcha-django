from xml.dom import minidom

from django.conf import settings
from social_core.backends.openstreetmap import (
    OpenStreetMapOAuth as BaseOpenStreetMapOAuth,
)


class OpenStreetMapOAuth(BaseOpenStreetMapOAuth):
    """OpenStreetMap OAuth1 authentication backend"""

    AUTHORIZATION_URL = f"{settings.OAUTH_BASE_URL}/authorize"
    REQUEST_TOKEN_URL = f"{settings.OAUTH_BASE_URL}/request_token"
    ACCESS_TOKEN_URL = f"{settings.OAUTH_BASE_URL}/access_token"

    def user_data(self, access_token, *args, **kwargs):
        """Return user data provided"""
        response = self.oauth_request(
            access_token, f"{settings.OAUTH_API_URL}/api/0.6/user/details"
        )
        try:
            dom = minidom.parseString(response.content)
        except ValueError:
            return None
        user = dom.getElementsByTagName("user")[0]
        try:
            avatar = dom.getElementsByTagName("img")[0].getAttribute("href")
        except IndexError:
            avatar = None
        return {
            "id": user.getAttribute("id"),
            "username": user.getAttribute("display_name"),
            "account_created": user.getAttribute("account_created"),
            "avatar": avatar,
        }
