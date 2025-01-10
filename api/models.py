from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.crypto import get_random_string


class ApiKeyManger(models.Manager):
    def create(self, **obj_data):
        while True:
            prefix = get_random_string(8)
            if not self.filter(prefix=prefix).exists():
                obj_data['prefix'] = prefix
                break
        key = get_random_string(56)
        full_key = prefix + "." + key
        obj_data['hashed_key'] = make_password(key)
        return full_key, super().create(**obj_data)
class ApiKey(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="api_keys")
    prefix = models.CharField(max_length=8, unique=True)
    hashed_key = models.CharField(max_length=100)
    revoked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    objects = ApiKeyManger()
    class Meta:
        ordering = ["-created"]

    # def save(self, *args, **kwargs):
    #     self.prefix = get_random_string(8)
    #     while True:
    #         prefix = get_random_string(8)
    #         if not ApiKey.objects.filter(prefix=prefix).exists():
    #             self.prefix = prefix
    #             break
    #     key = get_random_string(56)
    #     full_key = prefix + "." + key
    #     self.hashed_key = make_password(key)
    #
    #     super().save(*args, **kwargs)

    @property
    def is_valid(self):
        if self.revoked:
            return False
        if not self.expires_at:
            return True

        return self.expires_at >= timezone.now()

    def __str__(self):
        return f"{self.prefix}"
