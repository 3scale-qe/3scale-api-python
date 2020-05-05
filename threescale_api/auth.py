# pylint: disable=R0903
"""Implementation of custom 3scale specific authentication method(s) for requests (api clients"""

import requests
import requests.auth


class BaseClientAuth(requests.auth.AuthBase):
    """Abstract class for authentication of api client"""

    def __init__(self, app, location=None):
        self.app = app
        self.location = location
        if location is None:
            self.location = app.service.proxy.list().entity["credentials_location"]

    def __call__(self, request):
        credentials = self.credentials

        if self.location == "authorization":
            credentials = credentials.values()
            auth = requests.auth.HTTPBasicAuth(*credentials)
            return auth(request)

        if self.location == "headers":
            request.prepare_headers(credentials)
        elif self.location == "query":
            request.prepare_url(request.url, credentials)
        else:
            raise ValueError("Unknown credentials location '%s'" % self.location)

        return request


class UserKeyAuth(BaseClientAuth):
    """Provides user_key authentication for api client calls"""

    def __init__(self, app, location=None):
        super(UserKeyAuth, self).__init__(app, location)
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
        proxy = self.app.service.proxy.list()
        self.credentials = {
            proxy["auth_app_id"]: self.app["application_id"],
            proxy["auth_app_key"]: self.app.keys.list()["keys"][0]["key"]["value"]
        }

    def __call__(self, request):
        return super().__call__(request)
