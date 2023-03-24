from django.db import models
from django.core.validators import RegexValidator
import uuid
from django.utils import timezone


class Users(models.Model):
    Firstname = models.CharField(max_length=50, null=False)
    Lastname = models.CharField(max_length=50, null=False)
    Email = models.TextField(max_length=50, null=False,
                             unique=True, blank=False)
    Password = models.CharField(max_length=50, null=False)
    RepeatPassword = models.CharField(
        max_length=50, null=False)
    mobile_phone = models.CharField(max_length=11, unique=True, validators=[
                                    RegexValidator(r'^01[0125][0-9]{8}$', 'Invalid mobile phone number.')], default='0123456789')
    image = models.ImageField(
        upload_to='images/%y/%m/%d', null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)
    BirthDate = models.DateTimeField(max_length=12, null=True, blank=True)
    Facebook = models.CharField(max_length=100, null=True, blank=True)
    Country = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.Firstname

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_username(self):
        pass
    # class methods are methods that are preformed on the class itself not the instace of the class

    @classmethod
    def get_specific_info(cls, id):
        return cls.objects.get(pk=id)


class Activation(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    # checking if the token is expired or not

    def is_expired(self):
        return self.expires_at <= timezone.now()

    def __str__(self):
        return f"Activation for {self.user.Firstname}"
