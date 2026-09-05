from rest_framework.throttling import AnonRateThrottle


class CustomAnonThrottle(AnonRateThrottle):
    scope = "anon"


class AuthTokenThrottle(AnonRateThrottle):
    scope = "auth_token"
