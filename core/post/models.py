from typing import Any
from urllib import request
from django.db import models
from django.core.exceptions import ValidationError
from shortuuid.django_fields import ShortUUIDField
import timeago, datetime
from user.models import ProfileEmployeur
from django.utils.timesince import timesince
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
import requests
# Create your models here.
now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)
class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=6,max_length=255, alphabet='1234567890' , editable=False,  prefix='cat-')
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
    jid = ShortUUIDField(unique=True, length=6 ,max_length=255, alphabet='1234567890' , editable=False,  prefix='job-')
    title = models.CharField(max_length=50)
    image = models.ImageField(max_length=250, default='default.jpg')
    category = models.ForeignKey(Category,on_delete=models.CASCADE, default='', related_name='category')
    author = models.ForeignKey(ProfileEmployeur,on_delete=models.CASCADE,related_name='author')
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
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=1024, blank=True, null=True)
    job = models.ForeignKey(Job, related_name='localities', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.job} - {self.latitude}, {self.longitude}'

    def save(self, *args, **kwargs):
        if not (self.latitude and self.longitude):
            raise ValidationError("Latitude and Longitude must be provided")
        super().save(*args, **kwargs)
        self.update_address()

    def update_address(self):
        """Update address and geographical details using reverse geocoding."""
        try:
            response = requests.get(f'https://nominatim.openstreetmap.org/reverse?lat={self.latitude}&lon={self.longitude}&format=json&addressdetails=1')
            data = response.json()

            self.address = data.get('display_name', 'No address found')
            self.country = data.get('address', {}).get('country', '')
            self.region = data.get('address', {}).get('state', '') or data.get('address', {}).get('region', '')
            self.city = data.get('address', {}).get('city', '') or data.get('address', {}).get('town', '') or data.get('address', {}).get('village', '')
            self.neighborhood = data.get('address', {}).get('suburb', '')

            super().save(update_fields=['address', 'country', 'region', 'city', 'neighborhood'])

        except Exception as e:
            print(f'Error in update_address: {e}')
            # Log the error or handle it as needed

    class Meta:
        verbose_name = 'Locality'
        verbose_name_plural = 'Localities'
        ordering = ['job', 'latitude', 'longitude']