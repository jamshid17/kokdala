from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
# Create your models here.

# class User(AbstractUser):
#     image = models.ImageField(upload_to="users/", null=True, blank=True)
    

class User(AbstractUser):
    class UserRoles(models.TextChoices):
        HUKUMAT = "Hukumat", "Hukumat"
        ORGANISH = "Organish", "Organish"

    role = models.CharField(choices=UserRoles.choices, default=UserRoles.HUKUMAT, max_length=50)
    phone_number = PhoneNumberField(region='UZ', null=True, blank=True)
    image = models.ImageField(upload_to="users/", null=True, blank=True)
    # only user with "Organish" role
    organish_guruh = models.ForeignKey(
        to='organish.OrganishGuruh', related_name='worker', 
        on_delete=models.SET_NULL, null=True, blank=True
    )


    def clean(self) -> None:
        if self.role == 'Organish' and self.organish_guruh == None:
            raise ValidationError("If role is 'Organish', you need fill organish guruh!")
        if self.role != 'Organish' and self.organish_guruh != None:
            raise ValidationError("If role is not 'Organish', organish guruh must be null!")