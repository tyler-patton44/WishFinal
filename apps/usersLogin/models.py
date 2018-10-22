from __future__ import unicode_literals
from django.db import models
from django.db.models import Q
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if postData['first_name'].isalpha() != True:
            errors['reg'] = "Invalid  first name"
        if len(postData['first_name']) < 1:
            errors['reg'] = "First name cannot be more than 100 characters"
        if len(postData['first_name']) > 100:
            errors['reg'] = "First name cannot be more than 100 characters"
        if postData['last_name'].isalpha() != True:
            errors['reg'] = "Invalid  last name"
        if len(postData['last_name']) < 1:
            errors['reg'] = "First name cannot be more than 100 characters"
        if len(postData['last_name']) > 100:
            errors['reg'] = " Last name cannot be more than 100 characters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['reg'] = "Invalid email"
        if len(postData['email']) > 250:
            errors['reg'] = "Email cannot be more than 250 characters"
        email_val = self.filter(email=postData['email'])
        if email_val:
            errors['reg'] = "Email is already in use"
        if len(postData['password']) < 8:
            errors['reg'] = "Password cannot be less than 8 characters"
        if len(postData['password']) > 100:
            errors['reg'] = "Password cannot be more than 100 characters"
        if postData['password'] != postData['confirm_password']: 
            errors['reg'] = "Password and confirm password do not match"
        return errors

    def insertUser(self, postData):
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        hash2 = bcrypt.hashpw(postData['email'].encode(), bcrypt.gensalt())
        self.create(first_name=postData['first_name'], last_name=postData['last_name'], password=hash1, email = postData['email'], email_hash = hash2)
        return

    def login_validator(self, postData):
        wrong = {}
        if len(self.filter(email=postData['email2'])) < 1:
            wrong['login'] = "Email not in database"
            return wrong
        else:
            user = self.get(email=postData['email2'])
            if bcrypt.checkpw(postData['password2'].encode(), user.password.encode()):
                return wrong
            else:
                wrong['login'] = "Wrong password"
                return wrong
        return wrong


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    email_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
    def __repr__(self):
        return "<Users {} {} {} {}>".format(self.first_name,self.last_name, self.email, self.password)

    


