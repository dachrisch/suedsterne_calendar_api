from flask_dance.contrib.google import google


class GoogleAuthProvider(object):
    auth_service = google

    @property
    def authorized(self):
        return GoogleAuthProvider.auth_service.authorized


class UnauthorizedException(Exception):
    pass
