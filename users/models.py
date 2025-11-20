from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import uuid
# Create your models here.



class UserManager(BaseUserManager):
    def create_user(self,email,first_name,last_name,password=None,**kwargs):
        if not email:
            raise ValueError("Email required")
        
        email = self.normalize_email(email)
        user =self.model(email=email,first_name=first_name,last_name=last_name,**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    

    def create_superuser(self,email,first_name,last_name,password=None,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_active',True)
        kwargs.setdefault('is_superuser',True)
        return self.create_user(email,first_name,last_name,password,**kwargs)
    
 
class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=256,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
        
