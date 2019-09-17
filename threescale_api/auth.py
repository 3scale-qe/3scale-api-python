# pylint: disable=R0903
"Implementation of custom 3scale specific authentication method(s) for requests (api clients"
import abc

import requests

class BaseClientAuth(requests.auth.AuthBase):
    "Abstract class for authentication of api client"
    def __init__(self, app, location):
        self.app = app
        self.location = location

    @property
    @abc.abstractmethod
    def credentials(self):
        "returns credentials pair as tuple"

    def __call__(self, r):
        credentials = self.credentials

        if self.location == "authorization":
            credentials = credentials.values()
            auth = requests.auth.HTTPBasicAuth(*credentials)
            return auth(r)

        if self.location == "headers":
            r.prepare_headers(credentials)
        elif self.location == "query":
            r.prepare_url(r.url, credentials)
        else:
            raise ValueError("Unknown credentials location '%s'" % self.location)

        return r

class UserKeyAuth(BaseClientAuth):
    "Provides user_key authentication for api client calls"
    @property
    def credentials(self):
        return {
            self.app.service.proxy.list()["auth_user_key"]: self.app["user_key"]}

    def __call__(self, r):
        if self.location == "authorization":
            auth = requests.auth.HTTPBasicAuth(next(iter(self.credentials.values())), "")
            return auth(r)
        return super().__call__(r)


class AppIdKeyAuth(BaseClientAuth):
    "Provides app_id/app_key pair based authentication for api client calls"
    @property
    def credentials(self):
        return {
            "app_id": self.app["application_id"],
            "app_key": self.app.keys.list()["keys"][0]["key"]["value"]}

    def __call__(self, r):
        if self.location == "authorization":
            credentials = self.credentials
            auth = requests.auth.HTTPBasicAuth(
                credentials["app_id"], credentials["app_key"])
            return auth(r)
        return super().__call__(r)
