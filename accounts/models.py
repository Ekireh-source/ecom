from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """creates and saves a new user """
        if not email:
            raise ValueError('User must have an Email')
        # if not phone_number:
        #     raise ValueError('User must have a phone_number')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name = last_name,
            # phone_number = phone_number,
            **extra_fields

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,   first_name, last_name, password):
        """creates and saves a new superuser"""
        if password is None:
            raise TypeError('Password should not been None')
        user = self.create_user(email, first_name, last_name, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    # phone_number = models.IntegerField(default=False, unique=True)
    first_name = models.CharField(max_length=240)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'password']

    def __str__(self):
        return self.email


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'