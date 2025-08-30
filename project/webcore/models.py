from django.db import models
from django.conf import settings
from django.urls import reverse


class Rubric(models.Model):
    name = models.CharField(verbose_name="Название",max_length=100,unique=True)
    slug = models.SlugField(verbose_name="Слаг",max_length=100,unique=True)
    class Meta:
        verbose_name = "Рубрика"
        verbose_name_plural = "Рубрики"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("rubric_detail", kwargs={"slug": self.slug})

class Ad(models.Model):
    rubric=models.ForeignKey(Rubric,on_delete=models.CASCADE,verbose_name="Рубрика")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Продавец")
    title = models.CharField(verbose_name="Заголовок", max_length=100)
    slug= models.SlugField(verbose_name="Слаг", max_length=100, unique=True)
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2, blank=True, null=True)
    content = models.TextField(verbose_name="Контент", blank=True, null=True)
    is_published = models.BooleanField(verbose_name="Опубликовано", default=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    image = models.ImageField(verbose_name="Изображение", upload_to='ads/', blank=True, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return f" {self.title} - {self.price}"


class Comment(models.Model):
    ad=models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='comments', verbose_name="Объявление")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
    text= models.TextField(verbose_name="Текст комментария")
    is_approved = models.BooleanField(verbose_name="Одобрен", default=False)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f" {self.text} - {self.author.username}"





