from django.db import models
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    
    def create_user(self, name, email, password, confirmpassword, **other_fields):
        if not email:
            return ValueError(gettext_lazy('Provide an email'))
        if not name:
            return ValueError(gettext_lazy('Provide an name'))
        if not password:
            return ValueError(gettext_lazy('Provide an password'))
        if password!=confirmpassword:
            return ValueError(gettext_lazy('Password and Confirm password fields do not match'))
        
        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(confirmpassword)
        user.save()
        return user
    
    def create_superuser(self, name, email, password, **other_fields):
        
        user = self.create_user(name, email, password, **other_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    photo = models.ImageField(upload_to='avatar/')
    name = models.CharField(max_length=70, null=False)
    email = models.EmailField(max_length=70, null=False, unique=True)
    password = models.CharField(max_length=70, null=False)
    confirmpassword = models.CharField(max_length=70, null=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)   
     
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password', 'confirmpassword']
    
    def __str__(self) -> str:
        return self.name