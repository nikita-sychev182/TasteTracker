from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название категории",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Item(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, "1"
        TWO = 2, "2"
        THREE = 3, "3"
        FOUR = 4, "4"
        FIVE = 5, "5"

    class StatusChoices(models.TextChoices):
        WANT = "want", "Хочу"
        DONE = "done", "Сделано"
        FAVORITE = "favorite", "В избранном"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Пользователь",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="items",
        null=True,
        blank=True,
        verbose_name="Категория",
    )
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    image = models.ImageField(upload_to="items/", verbose_name="Изображение")
    rating = models.PositiveSmallIntegerField(
        choices=RatingChoices.choices,
        verbose_name="Оценка",
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        verbose_name="Статус",
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name="Публичное",
        help_text="Если отмечено, впечатление видно всем пользователям. Если нет — только вам.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Элемент коллекции"
        verbose_name_plural = "Элементы коллекции"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title