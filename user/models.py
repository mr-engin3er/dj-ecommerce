from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
# Create your models here.
GENDER_CHOICES = (('MALE', 'MALE'),
                  ('FEMALE', 'FEMALE'))


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    is_customer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    payment_id = models.CharField(max_length=124, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self) -> str:
        return self.user.email


class Address(models.Model):
    TYPE_CHOICES = ((1, 'Home'),
                    (2, 'Office'))
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    mobile_number = models.IntegerField()
    house_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=50)
    colony = models.CharField(max_length=50)
    landmark = models.CharField(max_length=50)
    state = models.ForeignKey(
        'State',  on_delete=models.CASCADE)
    city = models.ForeignKey(
        'City', related_name='city', on_delete=models.CASCADE)
    pin_code = models.IntegerField()
    address_type = models.PositiveSmallIntegerField(
        choices=TYPE_CHOICES)
    default_address = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Addresses'

        def __str__(self):
            return self.user


class State(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(
        'State', related_name='state', related_query_name='state', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name
