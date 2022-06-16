from ast import BinOp
from fileinput import filename
from operator import mod
from re import T
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, fullname, filename, password=None, bio=None):
        if not username:
            raise ValueError('Please provide a username')
        if not email:
            raise ValueError('Please provide an email address')
        if not fullname:
            raise ValueError('Please provide a fullname')
        if not filename:
            raise ValueError('Please provide a filename')
        
        user = self.model(
                username=username, 
                email= self.normalize_email(email),
                fullname=fullname,
                filename=filename,
                bio=bio,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, fullname, filename, password, bio=None):
        user = self.create_user(
                username=username, 
                email= self.normalize_email(email),
                fullname=fullname,
                filename=filename,
                password = password,
                bio = bio,
        )

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email                   = models.EmailField(max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)
    fullname                = models.CharField(max_length=40)
    filename                = models.CharField(max_length=64)
    bio                     = models.TextField(null=False, blank=True)
    date_joined             = models.DateTimeField(auto_now_add=True)
    last_login              = models.DateTimeField(auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullname', 'filename',]


    objects = MyAccountManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True