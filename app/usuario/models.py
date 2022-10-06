from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    cedula = models.CharField(max_length=10, unique=True)
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
