from django.db import models
from .category import Category


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="parent_category"
    )
    subcategory_name = models.SlugField(
        max_length=45,
        null=False,
        unique=True,
        blank=False,
        allow_unicode=True,

    )

    def __str__(self) -> str:
        return self.subcategory_name
