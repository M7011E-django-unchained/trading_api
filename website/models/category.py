from django.db import models


class Category(models.Model):
    name = models.SlugField(
        primary_key=True, max_length=45, null=False, unique=True, blank=False,
        allow_unicode=True
    )

    def __str__(self) -> str:
        return self.name
