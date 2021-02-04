from django.db import models


class Rule(models.Model):

    url = models.CharField(
        max_length=2048,
        default='',
        null=False,
        blank=False
    )

    short_url = models.CharField(
        max_length=32,
        default='',
        null=False,
        blank=False
    )

    active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    def __str__(self):
        return self.url


class User(models.Model):

    session_id = models.CharField(
        max_length=32,
        default='',
        null=False,
        blank=False
    )

    rules = models.ManyToManyField(
        Rule,
        blank=True
    )

    active = models.BooleanField(
        default=True,
        null=False,
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.session_id
