from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    """
    Custom user manager
    """
    def create_user(self, username, password):
        if not username or not password:
            raise ValueError("We need username and password here...")
        user = self.model(username=username)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, password):
        if not username or not password:
            raise ValueError("We need username and password here...")
        user = self.create_user(username=username,password=password)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser):
    """
    Custom user class
    """
    username = models.CharField(max_length=64, unique=True, db_index=True)
    joined = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username