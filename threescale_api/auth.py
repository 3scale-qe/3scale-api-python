# pylint: disable=R0903
"""Implementation of custom 3scale specific authentication method(s) for requests (api clients"""
from abc import ABC, abstractmethod

import requests
import requests.auth


class ThreescaleBaseClientAuth(ABC):
    """Abstract class for Auth client"""

    def __init__(self, app, location=None):
        self.app = app
        self.location = location
        self.credentials = {}

    @abstractmethod
    def update_credentials(self, app):
        """Updates the application of the auth object"""
        self.app = app


class BaseClientAuth(ThreescaleBaseClientAuth, requests.auth.AuthBase):
    """Abstract class for authentication of api client"""

    def update_credentials(self, app):
        super().update_credentials(app)
        if self.location is None:
            self.location = app.service.proxy.list().entity["credentials_location"]

    def __call__(self, request):

        if self.location == "authorization":
            credentials = self.credentials.values()
            auth = requests.auth.HTTPBasicAuth(*credentials)
            return auth(request)

        if self.location == "headers":
            request.prepare_headers(self.credentials)
        elif self.location == "query":
            request.prepare_url(request.url, self.credentials)
        else:
            raise ValueError("Unknown credentials location '%s'" % self.location)

        return request


class UserKeyAuth(BaseClientAuth):
    """Provides user_key authentication for api client calls"""

    def __init__(self, app, location=None):
        super(UserKeyAuth, self).__init__(app, location)

    def update_credentials(self, app):
        super(UserKeyAuth, self).update_credentials(app)
        self.credentials = {
            self.app.service.proxy.list()["auth_user_key"]: self.app["user_key"]
        }

    def __call__(self, request):
        if self.location == "authorization":
            auth = requests.auth.HTTPBasicAuth(next(iter(self.credentials.values())), "")
            return auth(request)
        return super().__call__(request)


class AppIdKeyAuth(BaseClientAuth):
    """Provides app_id/app_key pair based authentication for api client calls"""

    def __init__(self, app, location=None):
        super(AppIdKeyAuth, self).__init__(app, location)

    def update_credentials(self, app):
        super(AppIdKeyAuth, self).update_credentials(app)
        proxy = self.app.service.proxy.list()
        self.credentials = {
            proxy["auth_app_id"]: self.app["application_id"],
            proxy["auth_app_key"]: self.app.keys.list()["keys"][0]["key"]["value"]
        }

    def __call__(self, request):
        return super().__call__(request)
