from typing import Any
from django.db import models
from shortuuid.django_fields import ShortUUIDField
import timeago, datetime
from user.models import ProfileEmployeur
from django.utils.timesince import timesince
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
# Create your models here.
now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=6, max_length=20 , alphabet='1234567890' , editable=False,  prefix='cat-')
    title = models.CharField(max_length=50)
    image = models.ImageField(max_length=250, default='default.jpg')

    add_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    def __str__(self):
        return self.title

class Experience(models.Model):
    title = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
class TagTaggedItem(TaggedItemBase):
    content_object = models.ForeignKey('Job', on_delete=models.CASCADE)

class ConpetenceTaggedItem(TaggedItemBase):
    content_object = models.ForeignKey('Job', on_delete=models.CASCADE)

class Job(models.Model):
    jid = ShortUUIDField(unique=True, length=6, max_length=20 , alphabet='1234567890' , editable=False,  prefix='job-')
    title = models.CharField(max_length=50)
    image = models.ImageField(max_length=250, default='default.jpg')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default='', related_name='category')
    author = models.ForeignKey(ProfileEmployeur,on_delete=models.CASCADE, default='', related_name='author')
    description = models.TextField()
    requierements = models.TextField(default='')
    responsability = models.TextField(default='')
    experience  = models.CharField(max_length=50)
    salary = models.CharField(max_length=100, default='A en discuter')
    type  = models.CharField(max_length=50)
    competence = TaggableManager(through=ConpetenceTaggedItem, related_name='conpetence')
    tag = TaggableManager(through=TagTaggedItem, related_name='tag')
    qualification = models.CharField(max_length=150, default='aucun diplome requis')
    locality = models.CharField(max_length=50)
    genre =  models.CharField(max_length=50, default='')
    expire_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, null=True)
    publication_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    facebook_link =  models.URLField(max_length=250, blank=True, null=True, default='')
    instagram_link =  models.URLField(max_length=250, blank=True, null=True, default='')
    twetter_link =  models.URLField(max_length=250, blank=True, null=True, default='')
    youtube_link =  models.URLField(max_length=250, blank=True, null=True, default='')

    mail = models.EmailField(max_length=150, default='' , blank=True, null=True)
    phone = models.CharField(max_length=150, default='' , blank=True, null=True)
    whatsapp = models.CharField(max_length=150, default='' , blank=True, null=True)


    active = models.BooleanField(default=True)

   

    def timeago(self):
        if timezone.is_naive(self.publication_date):
            publication_date = timezone.make_aware(self.publication_date, timezone.get_current_timezone())
        else:
            publication_date = self.publication_date

        now = timezone.now()
        return timesince(publication_date, now)

    def is_salary_alpha(self):
        return self.salary.isdigit()

    def __str__(self):
        return self.title

class Locality(models.Model):
    position = models.CharField(max_length=50)
    job = models.ForeignKey(Job, related_name='job', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.job}- {self.position}'
 