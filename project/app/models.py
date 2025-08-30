from django.contrib.auth.models import User, AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey,GenericRelation
from django.core.validators import *
from django.db import models
from django.core.exceptions import *
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver

#Кастомная модель пользователя v1
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=20,blank=True,null=True)
    website=models.URLField(blank=True,null=True)

    class Meta:
        verbose_name="Профиль пользователя"
        verbose_name_plural="Профили пользователей"

    def __str__(self):
        return f"{self.user.username}"

@receiver(post_save,sender=User,dispatch_uid="create_user_profile_signal")
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        print("Профиль пользователя создан")

#Кастомная модель пользователя v2
# class CustomUser(AbstractUser):
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     website = models.URLField(blank=True, null=True)
#
#     class Meta:
#         verbose_name = "Пользователь"
#         verbose_name_plural = "Пользователи"
#
#     def __str__(self):
#         return f"{self.username}"

#Кастомная модель пользователя v3
# class UserProxy(User):
#     class Meta:
#         proxy = True
#         ordering = ["username"]
#         verbose_name = "Прокси пользователь"
#         verbose_name_plural = "Прокси пользователи"
#
#     def get_full_name(self):
#         return f"{self.first_name} {self.last_name}"
#
#     def __str__(self):
#         return f"{self.username} - {self.email}"








#Базовое наследование
class Message(models.Model):
    content=models.TextField()

class PrivateMessage(Message):
    # content уже есть
    user=models.ForeignKey(User,on_delete=models.CASCADE)


#Абстрактное наследование
class Base(models.Model):
    created=models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract=True
        ordering=["-created"]

class Order(Base):
    price=models.FloatField()

    class Meta(Base.Meta):
        verbose_name="Заказ"




#Полиморфные связи
class Note(models.Model):
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey("content_type","object_id")
    text=models.TextField()




class Kind(models.IntegerChoices):
    Buy=1,'Куплю'
    Sell=2,'Продам'
    Change=3,'Обмен'

#select_related
#prefetch_related
#defer
#only
from django.db.models import Count

# class RubricManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().order_by('-name')
#
#     def order_by_bb_count(self):
#         return (
#             self.get_queryset().annotate(bb_count=Count('bb'))
#             .order_by("-bb_count")
#         )

class RubricQuerySet(models.QuerySet):
    def order_by_bb_count(self):
        return (
            self.annotate(bb_count=Count('bb'))
            .order_by("-bb_count")
        )
    def get_first_special(self):
        return self.order_by("name").last()

class Rubric(models.Model):
    notes = GenericRelation(Note)
    name = models.CharField(max_length=100)
    objects = RubricQuerySet.as_manager()
    # objects = models.Manager()
    # bbs= RubricManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/app/rubric/{self.pk}/"

#Proxy наследование
class RevRubric(Rubric):
    class Meta:
        proxy=True
        ordering=["-name"]



def validate_even(value):
    if value % 2 == 0:
        raise ValidationError(f"Число четное")

class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value):
        if value <= self.min_value or value >= self.max_value:
            raise ValidationError("Ваша цена вышла за диапазон")

    def deconstruct(self):
        return (
            f"{self.__class__.__module__}.{self.__class__.__name__}",
            (),
            {"min_value": self.min_value, "max_value": self.max_value},
        )

class BbManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('price')



bb_custom_signal=Signal()
class Bb(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE)
    title = models.CharField(max_length=100,verbose_name="Заголовок",validators=[RegexValidator("^.{4,}$")])
    price = models.FloatField(blank=True,null=True,verbose_name="Цена",validators=[MinMaxValueValidator(0,1000)])
    content = models.TextField(blank=True,null=True,verbose_name="Контент",validators=[MaxLengthValidator(100)])
    # published=models.DateTimeField(auto_now_add=True,verbose_name="Дата")
    published=models.DateTimeField(null=True,blank=True,verbose_name="Дата")
    objects = BbManager()

    def get_absolute_url(self):
        return f"/app/bb/{self.pk}/"

    def save(self,*args,**kwargs):
        if self.title=="Оружие":
            raise ValidationError('Нельзя оружие')
        super().save(*args,**kwargs)
        bb_custom_signal.send(sender=self.__class__,instance=self)


    def delete(self,*args,**kwargs):
        if self.title=="Мяч":
            raise ValidationError('Нельзя удалять')
        super().delete(*args,**kwargs)


    def title_and_price(self):
        if self.price:
            return f"Title: {self.title}, Price: {self.price}$"
        else:
            return f"Title: {self.title}$"






    # KINDS=(
    #     ('Куплю-продам',
    #         ('b','Куплю'),
    #         ('s', 'Продам'),
    #      ),
    #     ('Обмен',
    #     ('c', 'Обменяю'),)
    # )
    # kind=models.CharField(max_length=1,default='s',choices=KINDS)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural="Объявления"
        verbose_name="Объявление"
        ordering=["-published"]
        # index_together = ['title','published']
        # constraints = (
        #     models.CheckConstraint(
        #     check=models.Q(price__gt=0) & models.Q(price__lte=1000),
        #     name='bboard_price_check',
        #     )
        # )


class Passport(models.Model):
    country=models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE)


class Spare(models.Model):
    name=models.CharField(max_length=30)
    notes=GenericRelation(Note)
    def __str__(self):
        return self.name

class Machine(models.Model):
    name=models.CharField(max_length=30)
    spares=models.ManyToManyField(Spare)
    def __str__(self):
        return self.name

class Kit(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    spare=models.ForeignKey(Spare,on_delete=models.CASCADE)
    count=models.IntegerField()
    def __str__(self):
        return f"{self.machine} - {self.spare} - {self.count}"



class Quiz(models.Model):
    title=models.CharField(max_length=100)
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    def __str__(self):
        return self.text





import time
from uuid import uuid4
from pathlib import Path
from django.db import models

def photo_path(instance, filename: str) -> str:
    ts = int(time.time())
    ext = filename.split(".")[-1].lower()
    return f'uploads/{time.strftime("%Y/%m/%d")}/{uuid4().hex}_{ts}.{ext}'

class Document(models.Model):
    file = models.FileField(upload_to="docs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name or f"Document #{self.pk}"

class Photo(models.Model):
    image = models.ImageField(upload_to=photo_path, width_field="width", height_field="height")
    caption = models.CharField("Подпись", max_length=200, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True, editable=False)
    height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Photo #{self.pk}"

    def delete(self, *args, **kwargs):
        storage = self.image.storage
        name = self.image.name
        super().delete(*args, **kwargs)
        if name:
            storage.delete(name)

BASE_MEDIA = Path(__file__).resolve().parents[2] / "media"

def media_root_path():
    return str(BASE_MEDIA)

class StaticPick(models.Model):
    pick = models.FilePathField(
        path=media_root_path,
        match=r".*\.txt$",
        recursive=False,
        allow_files=True,
        allow_folders=False,
    )

    def __str__(self):
        return self.pick

from easy_thumbnails.fields import ThumbnailerImageField

class PhotoResized(models.Model):
    picture = ThumbnailerImageField(
        upload_to="photos_resized/",
        resize_source={"size": (1280, 1280), "crop": "scale"},  # сохранится уменьшенная копия
    )
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f"Resized #{self.pk}"
