from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('quotes:add_category')


class Profile(models.Model):
    profile_pic = models.ImageField(default="profile.png", upload_to='images/', blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250, default="I am")
    date_of_birth = models.DateField(blank=True, null=True)
    facebook_url = models.CharField(max_length=250, null=True, blank=True)
    youtube_url = models.CharField(max_length=250, null=True, blank=True)
    twitter_url = models.CharField(max_length=250, null=True, blank=True)
    linkedin_url = models.CharField(max_length=250, null=True, blank=True)
    instagram_url = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('profile_page', args=[self.pk])

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


class Quote(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quotes')
    title = models.CharField(max_length=250)
    body = models.TextField()
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Quotes_liked', blank=True)
    time = models.DateTimeField(auto_now_add=True, db_index=True)
    category = models.CharField(max_length=250, default='Popular Quote')

    def __str__(self):
        return str(self.title) + '|' + str(self.author)

    def total_likes(self):
        return self.users_like.count()

    def get_absolute_url(self):
        return reverse('quotes:quote_detail', args=[self.pk, self.title])


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('Comment', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    body = models.CharField(max_length=250)
    date_added = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('quotes:home')

    def __str__(self):
        return str(self.user) + '|' + str(self.date_added)
