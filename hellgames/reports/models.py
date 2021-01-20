from django.db import models
import uuid
# Create your models here.

class Report(models.Model):
    # use uuid to generate random unique tracking numbers for reports. 
    report_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post_title = models.CharField(max_length=32)
    post_text = models.TextField()
    STATUS_CHOICES = (
        ('O', 'Open'),
        ('C', 'Closed'),
        ('W', 'Waiting'),
    )
    post_status = models.CharField(choices=STATUS_CHOICES, default='W', max_length=72)
    posted_by = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)



    
