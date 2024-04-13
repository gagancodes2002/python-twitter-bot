from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Account(models.Model):
    accounts = models.TextField(blank=True, null=True)
    filtered_accounts = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=244)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
            
    def __str__(self):
        return self.name



# create Client and under client we need a images field which can store multiple images we can create a different model for images and link it to the client model each client will have a field called images which will store multiple images at path {client_name}/images/{image_name}
class Client(models.Model):
    name = models.CharField(max_length=244)
    commentable_accounts = models.TextField(blank=True, null=True)
    commentable_tweet_ids = models.TextField(blank=True, null=True)
    tweet_links = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    # field to link image to a client
    images = models.ManyToManyField('Image', related_name='clients', blank=True, null=True)
    
    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
    
    def __str__(self):
        return self.name
class Image(models.Model):
    name = models.CharField(max_length=244, auto_created=True, default='image')
    image = models.ImageField(upload_to='images/')
    client_link = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_images')



class Todo(models.Model):
    task = models.CharField(max_length=244)
    completed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"

    def __str__(self):
        return self.task
