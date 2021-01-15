from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Image(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
    )
    is_private = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250, blank=True)
    storage_id = models.CharField(max_length=36)
    height = models.FloatField()
    width = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ('user', 'title')
