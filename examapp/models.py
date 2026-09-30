from django.db import models
import bcrypt
import re
from datetime import date
# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 charcters"

        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 charcters"

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Wrong email address"

        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 charcters"

        if postData['password'] != postData['confirm_pw']:
            errors['password'] = "Password dont match"

        if User.objects.filter(email=postData['email']):
            errors['email_exists'] = "Email already exists"

        return errors



class ShowManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['title']) < 3:
            errors['title'] = "Title must be at least 3 charcters"

        if len(postData['network']) < 3:
            errors['network'] = "Network must be at least 3 charcters"

        if len(postData['comments']) < 3:
            errors['comments'] = "Comments must be at least 3 charcters"

        return errors



    
class User(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Tv_show(models.Model):
    title = models.CharField(max_length=40, unique = True)
    network = models.CharField(max_length=40)
    user = models.ForeignKey(User, related_name="user",on_delete=models.DO_NOTHING)
    release_date = models.DateField(null=True)
    comments = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

def add_user(data):
    hashed = bcrypt.hashpw(data['password'].encode(),bcrypt.gensalt()).decode()
    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    password = hashed

    User.objects.create(first_name = first_name, last_name = last_name, email= email,password = hashed )


def get_user():
    return User.objects.all

def get_show():
    return Tv_show.objects.all

def get_user_by_id(user_id):
    return User.objects.get(id=user_id)

def add_show(data, user_id):
    user = User.objects.get(id=user_id)
    title = data['title']
    network = data['network']
    release_date = data['release_date']
    comments = data['comments']

    Tv_show.objects.create(title = title, network = network,release_date = release_date,comments=comments,user=user)

def delete_show_by_id(show_id):
    show = Tv_show.objects.get(id=show_id)
    show.delete()

def edit_show_by_id(show_id):
    return Tv_show.objects.get(id=show_id)


def update_show(show_id, data):
    show = Tv_show.objects.get(id=show_id)

    show.title = data['title']
    show.network = data['network']
    show.release_date = data['release_date']
    show.comments = data['comments']
    
    show.save()

def get_show_by_id(show_id):
    return Tv_show.objects.get(id=show_id)