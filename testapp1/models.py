from django.db import models
from django.utils import timezone

# Create your models here.
class File(models.Model):
    file_path = models.FileField(upload_to='files/')
    file_name = models.CharField(max_length=200)

class Temp_File_Path(models.Model):
    existingPath = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    eof = models.BooleanField()

class User(models.Model):
    user_id = models.CharField(max_length=20,unique=True)
    user_email = models.EmailField(unique=True)
    user_password = models.CharField(max_length=20)
    user_nickname = models.CharField(max_length=20,unique=True)
    user_score = models.IntegerField(default=0)
    user_favorite = models.CharField(default="None",max_length=20)
    user_validate = models.BooleanField(default=True)
    user_img = models.FileField(upload_to='user_info/', default='user_info/default_file.jpg')


class Post(models.Model):
    user_id = models.CharField(max_length=20)
    user_nickname = models.CharField(max_length=20)
    vote = models.IntegerField(default=0)
    visited = models.IntegerField(default=0)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=200)
    post_img = models.FileField(upload_to='post/', default='post/default_file.jpg')
    category = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    product_name=  models.CharField(max_length=20)
    sold_out = models.BooleanField(default=False)