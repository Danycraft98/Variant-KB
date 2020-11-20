from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, username, password, email=None):
        """
        Creates and saves a User with the given email and password.
        """
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username,
            password,
            email=email,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_specialist(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password,
            email=email
        )
        user.staff = True
        user.specialist = True
        user.save(using=self._db)
        return user

    def create_counselor(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password,
            email=email
        )
        user.staff = True
        user.specialist = True
        user.counselor = True
        user.save(using=self._db)
        return user

    def create_scientist(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password,
            email=email
        )
        user.staff = True
        user.specialist = True
        user.counselor = True
        user.scientist = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username,
            password,
            email=email
        )
        user.staff = True
        user.specialist = True
        user.counselor = True
        user.scientist = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    specialist = models.BooleanField(default=False)
    counselor = models.BooleanField(default=False)
    scientist = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)  # a superuser
    objects = UserManager()
    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_scientist(self):
        """Is the user a member of staff?"""
        return self.scientist

    @property
    def is_counselor(self):
        """Is the user a member of staff?"""
        return self.counselor

    @property
    def is_specialist(self):
        """Is the user a member of staff?"""
        return self.specialist

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active
