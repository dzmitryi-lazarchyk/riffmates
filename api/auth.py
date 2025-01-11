from typing import Optional, Any

from django.http import HttpRequest
from django.contrib.auth.hashers import check_password
from ninja.security import APIKeyHeader

from .models import ApiKey

class AuthAPIKeyHeader(APIKeyHeader):
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

api_key = ApiKey()


