from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Sum, F
class Cart(models.Model):
    # make cart user-associated
    user = models.ForeignKey('user.CustomUser', null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField('accounts.gamePost', blank=True)
    total = MoneyField(max_digits=19, decimal_places=4, default_currency='USD', blank=True, default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_on = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    
    
    def __str__(self):
        return "Cart for %s" %(self.user)
    def __unicode__(self):
        return "Cart id: %s" %(self.id)

    # calculate total value of cart 
    @property
    def total_price(self):
        return self.products.aggregate(total_price=Sum(F('price')))