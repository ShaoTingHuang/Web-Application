from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User


# Create your models here.
# Data model for a network item
class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None)
    time = models.CharField(max_length=50, default = None, null = True)

    def __unicode__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'

class Profile(models.Model):
    user = models.ForeignKey(User, default=None)
    Firstname = models.CharField(max_length=20, blank=False)
    Lastname = models.CharField(max_length=20, blank=False)
    Age = models.CharField(max_length=3, blank=True, null=True)
    Short_bio = models.CharField(max_length=430, blank=True)
    photo = models.FileField(upload_to="images", blank=True, default="empty.jpg")
    content_type = models.CharField(max_length=50)
    Follows = models.ManyToManyField("self", related_name='follow_list', symmetrical=False)

    def __unicode__(self):
        return 'Profile(id=' + str(self.id) + ')'
