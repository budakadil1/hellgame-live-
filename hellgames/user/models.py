from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser
)
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from shoppingcart.models import Cart

# Custom User Model with merchant_status.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, username, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('Email is required.'))
        if not username:
            raise ValueError(_('Username is required.'))
        email = self.normalize_email(email)
        username = username
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    # consider case insensitive usernames for validation
    username = models.CharField(max_length=24, blank=False, unique=True)
    merchant_status = models.BooleanField(default=False, blank=False)

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."))
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique=True) # validators should be a list

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

# profile model
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, related_name='profile', on_delete=models.CASCADE)
    user_description = models.TextField(max_length=500, blank=True)
    bad_review_count = models.IntegerField(default=0)
    good_review_count = models.IntegerField(default=0)
    reviewscore = models.IntegerField(default=0)
    
    # calculate and save reviewscore to the database for easy view retrieval.
    def save(self, *args, **kwargs):
        try:
            self.reviewscore = int((self.good_review_count / (self.good_review_count + self.bad_review_count) * 100))
        except ZeroDivisionError:
            self.reviewscore = int(0)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.email
    


############ REVIEW MODEL ###########################
class Reviews(models.Model):

    '''
    No need for slug because reviews are not on seperate page.
    '''
    review_title = models.CharField(max_length=48)
    REVIEW_TYPES = (
        ('Negative', 'Negative'),
        ('Positive', 'Positive'),
    )
    review_text = models.TextField(max_length=500)
    review_type = models.CharField(choices=REVIEW_TYPES, max_length=72)
    review_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="toReview")
    review_from = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="fromReview")
    review_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.review_title
    

# ADD IN REPORT SYSTEM LATER!

############## RECEIVERS FOR PROFILE ######################
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=CustomUser)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(post_save, sender=Reviews)
def add_review_to_profile(sender, instance, **kwargs):
    if instance.review_type == 'Positive':
        instance.review_to.profile.good_review_count += 1
    elif instance.review_type == 'Negative':
        instance.review_to.profile.bad_review_count -= 1

    instance.review_to.profile.save()