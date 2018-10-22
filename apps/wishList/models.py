from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
import re
import bcrypt
from ..usersLogin.models import *
class WishManager(models.Manager):
    def wishVal(self, postData):
        errors = {}
        if len(postData['wish']) < 1:
            errors['reg'] = "Wish cannot be less than 1 characters"
        if len(postData['wish']) > 100:
            errors['reg'] = "Wish cannot be more than 100 characters"
        if len(postData['desc']) < 1:
            errors['reg'] = "Description cannot be less than 1 characters"
        if len(postData['desc']) > 100:
            errors['reg'] = "Description cannot be more than 100 characters"
        return errors

    def insertWish(self, postData):
        self.create(item=postData['wish'], desc=postData['desc'], status="pending", user=User.objects.get(id=int(postData['id'])))
        return

class Wish(models.Model):
    item = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="user_wish")
    status = models.CharField(max_length=255,  default='pending')
    likes = models.ManyToManyField(User, related_name="liked")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = WishManager()
    def __repr__(self):
        return "<Wish {}>".format(self.item)

    


