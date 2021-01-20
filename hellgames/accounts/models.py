from django.db import models
from PIL import Image, ImageOps
from djmoney.models.fields import MoneyField
from django.utils import timezone
import os
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from user.models import CustomUser
from accounts.utils import generate_unique_slug


class gameIdentifier(models.Model):
    game_name = models.CharField(max_length=48)
    GAME_CATEGORIES = (
        ('default', 'NO CATEGORY'),
        ('MOBA', 'MOBA'),
        ('FPS', 'FPS'),
        ('MMORPG', 'MMORPG'),
        ('Adventure','Adventure'),
        ('TPS','TPS'),
        ('MMO','MMO'),
        ('2D','2D'),
        ('KRAL','KRAL')
    )
    game_choice = models.CharField(choices=GAME_CATEGORIES, default='default', max_length=72)
    game_slug = models.SlugField(max_length=48, unique=True)
    def __str__(self):
        return self.game_name
    # Resize image on save to 200,200 or specified.


class gamePost(models.Model):
    post_title = models.CharField(max_length=32)
    # not used 
    SERVER_CATEGORIES = (
        ('NA', 'NA'),
        ('EUW', 'EUW'),
        ('EUNE', 'EUNE'),
        ('TR', 'TR'),
        ('OCE','OCE'),
        ('PBE','PBE'),
    )
    #add in server choice for league and other accounts later :)
    post_text = models.TextField()
    post_category = models.ForeignKey(gameIdentifier, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=32, unique=True)
    post_id = models.AutoField(primary_key=True)
    price = MoneyField(max_digits=19, decimal_places=2, default_currency='USD')
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    # Add Checkout to reduce one quantity if a purchase is validated.
    quantity = models.IntegerField(default=1)


    def __str__(self):
        # change with better admin list view?
        return str('id:' + str(self.post_id) + ' ' + str(self.post_title))
    
    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if self.post_title != self.slug:
                self.slug = generate_unique_slug(gamePost, self.post_title)
        else:  # create
            self.slug = generate_unique_slug(gamePost, self.post_title)
        super(gamePost, self).save(*args, **kwargs)