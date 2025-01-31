from django.db import models
from django.utils.text import slugify


class DateMixin(models.Model):
    """
    Добавляет поля "Дата создания" и "Дата обновления"
    """

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        abstract = True


class SlugifyMixin(models.Model):
    """
    Миксин для автоматической генерации slug на основе указанного поля.
    """

    slug = models.SlugField(unique=True, blank=True, null=True)
    slug_source_field = "title"  # Поле, на основе которого генерируется slug

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            source_field = getattr(self, self.slug_source_field)
            self.slug = slugify(source_field)
        super().save(*args, **kwargs)
