from __future__ import unicode_literals
import re
import bcrypt
from datetime import datetime
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def regis_validator(self, post):
        name = post['name']
        alias = post['alias']
        email = post['email'].lower()
        password = post['password']
        confirm = post['confirm']
        date = post['date']
        errors=[]

        if len(name)<1 or len(alias)<1 or len(email)<1 or len(password)<1 or len(confirm)<1 or len(date)<1 :
            errors.append("All fields are required!")
        else:
            if not EMAIL_REGEX.match(email):
                errors.append("Invalid email!")
            else:
                if len(User.objects.filter(email=email)) > 0 :
                    errors.append('Email is already registered!')

            if not name.isalpha() or not alias.isalpha():
                errors.append("Name and alias are characters only")

            if len(password) < 3 :
                errors.append('Password is at least 8 characters')
            elif password != confirm:
                errors.append('Password is not match with comfirm password, please try again')

            if len(date) < 1 :
                errors.append("Birthday can not be empty!")
            else:
                date_object = datetime.strptime(date, '%Y-%m-%d')
                if date_object > datetime.now():
                    errors.append("Your date of birth should not be in the future!")
            
        if not errors:
            hashed = bcrypt.hashpw((password.encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=name,
                alias=alias,
                email=email,
                password=hashed
            )
            return new_user                

        return errors

    def login_validator(self, post):
        email = post['email'].lower()
        password = post['password']

        try:
            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return user
        except:
            pass

        return False

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Quote(models.Model):
    content = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    uploader = models.ForeignKey(User, related_name="uploaded_quotes")
    liked_by = models.ManyToManyField(User, related_name="favorite")
