from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class cutomerUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_checker = models.BooleanField(default=False)
    is_maker = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_groups'  # Unique related_name for groups
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions'  # Unique related_name for user_permissions
    )

class Checker(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    is_checker = models.BooleanField(default=False)
    user = models.OneToOneField(cutomerUser, on_delete=models.CASCADE,default=None)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    emailid = models.CharField(max_length=255, null=True, blank=True)
    joined_date = models.DateField(max_length=255, null=True, blank=True)
    username=models.CharField(max_length=255,null=True,blank=True)
    password=models.CharField(max_length=255,null=True,blank=True)

class Maker(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    is_maker = models.BooleanField(default=False, null=True, blank=True)
    checker=models.ForeignKey(Checker, on_delete=models.CASCADE,null=True,blank=True)
    user = models.OneToOneField(cutomerUser, on_delete=models.CASCADE,default=None)
    fname = models.CharField(max_length=255, null=True, blank=True)
    lname = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    email_id = models.CharField(max_length=255, null=True, blank=True)
    joined_date = models.DateField(max_length=255, null=True, blank=True)
    username=models.CharField(max_length=255,null=True,blank=True)
    password=models.CharField(max_length=255,null=True,blank=True)

class CustomerProfile(models.Model):
    GENDER_CHOICES = [
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Other', 'Other'),
    ]
    maker=models.ForeignKey(Maker,on_delete=models.CASCADE,null=True,blank=True)
    checker=models.ForeignKey(Checker,on_delete=models.CASCADE,null=True,blank=True)

    username = models.CharField(max_length=64)
    email = models.EmailField(max_length=64)
    qualification = models.CharField(max_length=256)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    age = models.DateField()
    resume = models.FileField(upload_to='resumes/')
    image = models.ImageField(upload_to='images/')  # Use ImageField for image files
    status = models.CharField(max_length=10, default='pending')
