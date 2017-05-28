from django.db import models

# User class for built-in authentication module
from django.contrib.auth.models import User

# Data model for a todo-list item
class Item(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None)
    ip_addr = models.GenericIPAddressField()

    def __unicode__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'
