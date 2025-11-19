from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
# Create your models here.


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    full_name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=200)


