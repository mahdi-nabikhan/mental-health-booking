from django.db import models
from accounts.models import Therapist
# Create your models here.




class Blog(models.Model):
    
    class Status (models.TextChoices):
        DRAFT = "draft", "پیش‌نویس"
        PUBLISHED = "published", "منتشر شده"
        ARCHIVED = "archived", "آرشیو شده"
        
        
    
    title = models.CharField(max_length=255)
    description = models.TextField() = models.TextField()
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.DRAFT,)
    
    image =  models.ImageField(null=True,blank=True)
    
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
