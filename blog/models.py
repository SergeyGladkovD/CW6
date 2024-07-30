from django.db import models

NULLABLE = {"blank": "True", "null": "True"}


class Material(models.Model):
    title = models.CharField(max_length=50, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Содержание")
    image = models.ImageField(upload_to="blog/", verbose_name="Изображение", **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name="Просмотры")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "материал"
        verbose_name_plural = "материалы"
