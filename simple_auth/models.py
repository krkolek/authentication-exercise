from django.utils.functional import cached_property
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class UserManager(models.Manager):
    use_in_migrations = True

    def _create_user(self, username, password):
        """
        Creates and saves a User with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=150, unique=True, validators=[ASCIIUsernameValidator()],
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        error_messages={'unique': "A user with that username already exists."},
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('password',)

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @cached_property
    def last_login(self):
        """
        Override model field from AbstractBaseUser
        :return: datetime of last login
        """
        details = self.login_details.last()
        return details.login_datetime if details is not None else None


class LoginDetails(models.Model):
    user = models.ForeignKey(User, related_name='login_details')
    ip = models.GenericIPAddressField(unpack_ipv4=True)
    login_datetime = models.DateTimeField(auto_now_add=True)
