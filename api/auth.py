from typing import Optional, Any

from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
from ninja.security import APIKeyHeader, APIKeyQuery

from .models import ApiKey

class AuthCheck():
    param_name = "X-API-KEY"

    def authenticate(self, request: HttpRequest, key: Optional[str]) -> Optional[Any]:
        if key:
            if "." in key:
                prefix, key = key.split(".")
                try:
                    persistent_key = ApiKey.objects.get(prefix=prefix)
                except ApiKey.DoesNotExist:
                    return False

                if persistent_key:
                    if check_password(key, persistent_key.hashed_key):
                        if persistent_key.is_valid:
                            user = persistent_key.user

                            if not user or not user.is_active:
                                return False

                            request.user = user
                            return user

        return False

class QueryKey(AuthCheck, APIKeyQuery):
    pass

class HeaderKey(AuthCheck, APIKeyQuery):
    pass

api_key_querry = QueryKey()
api_key_header = HeaderKey()


